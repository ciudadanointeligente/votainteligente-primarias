# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from elecciones.models import Eleccion, Area, Indice, Dato, Candidato, Pregunta, Respuesta, Contacto, Colectivo, preguntas_por_partido
from elecciones.management.commands.elecciones_importer import *
from elecciones.management.commands.contactos_importer import *
from elecciones.management.commands.candidatos_importer import *
from mailer.models import Message
from django.test.client import Client
from django.utils.unittest import skip
from django.template import Template, Context
from urllib2 import quote
from popit.models import Person, ApiInstance


class SinDatosManager(TestCase):
	def setUp(self):
		self.eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", slug=u"la-eleccion1")
		self.popit_api_instance = ApiInstance.objects.create(url='http://popit.org/api/v1')
		self.person = Person.objects.create(api_instance =  self.popit_api_instance, name='person_name')
		self.candidato_con_todo = Candidato.objects.create(person=self.person,
															 eleccion=self.eleccion1,\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"candidato_con_todo")
		self.contacto_personal_con_todo = Contacto.objects.create(candidato=self.candidato_con_todo, \
															valor=u"personal@campana.cl",tipo=1)


	def test_sin_twitter_con_mail(self):
		person = Person.objects.create(api_instance =  self.popit_api_instance, name='another_person_name')
		candidato_sin_twitter = Candidato.objects.create(person=person,
															 eleccion=self.eleccion1,\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"")
		contacto_personal = Contacto.objects.create(candidato=candidato_sin_twitter, valor=u"personal@campana.cl",tipo=1)

		candidatos = Candidato.sin_datos.all()
		self.assertEquals(candidatos.count(), 1)
		self.assertEquals(candidatos[0], candidato_sin_twitter)


	def test_con_twitter_sin_mail(self):
		person = Person.objects.create(api_instance =  self.popit_api_instance, name='another_person_name')
		candidato_con_twitter = Candidato.objects.create(eleccion=self.eleccion1,\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"el_twitter")


		candidatos = Candidato.sin_datos.all()
		self.assertEquals(candidatos.count(), 1)
		self.assertEquals(candidatos[0], candidato_con_twitter)

	def test_sin_mail_ni_twitter(self):
		person = Person.objects.create(api_instance =  self.popit_api_instance, name='another_person_name')
		candidato_sin_contacto = Candidato.objects.create(eleccion=self.eleccion1,\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"")

		candidatos = Candidato.sin_datos.all()
		self.assertEquals(candidatos.count(), 1)
		self.assertEquals(candidatos[0], candidato_sin_contacto)

	def test_get_has_twitter_false(self):
		person = Person.objects.create(api_instance =  self.popit_api_instance, name='another_person_name')
		candidato_sin_contacto = Candidato.objects.create(eleccion=self.eleccion1,\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"")

		self.assertFalse(candidato_sin_contacto.has_twitter)
		self.assertFalse(candidato_sin_contacto.has_contacto)

class NosFaltanDatosViewTestCase(TestCase):
	def setUp(self):
		self.eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", slug=u"la-eleccion1")
		self.popit_api_instance = ApiInstance.objects.create(url='http://popit.org/api/v1')
		self.person1 = Person.objects.create(api_instance =  self.popit_api_instance, name='another_person_name')
		self.candidato_con_todo = Candidato.objects.create(person=self.person1,
															 eleccion=self.eleccion1,\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"candidato_con_todo")
		self.contacto_personal_con_todo = Contacto.objects.create(candidato=self.candidato_con_todo, \
															valor=u"personal@campana.cl",tipo=1)

		self.person2 = Person.objects.create(api_instance =  self.popit_api_instance, name='a_nother_person_name')
		self.candidato_sin_contacto = Candidato.objects.create(person=self.person2,
															 eleccion=self.eleccion1,\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"")

	def test_get_page(self):
		url = reverse('nos_faltan_datos')
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'elecciones/nos_faltan_datos.html')
		self.assertTrue('candidatos' in response.context)
		self.assertTrue( self.candidato_sin_contacto in response.context['candidatos'] )