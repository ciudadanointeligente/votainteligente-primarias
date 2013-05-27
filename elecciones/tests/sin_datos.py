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


class SinDatosManager(TestCase):
	def setUp(self):
		self.eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", slug=u"la-eleccion1")
		self.candidato_con_todo = Candidato.objects.create(eleccion=self.eleccion1,\
															 nombre=u"el candidato con todo",\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"candidato_con_todo")
		self.contacto_personal_con_todo = Contacto.objects.create(candidato=self.candidato_con_todo, \
															valor=u"personal@campana.cl",tipo=1)


	def test_sin_twitter_con_mail(self):
		candidato_sin_twitter = Candidato.objects.create(eleccion=self.eleccion1,\
															 nombre=u"el candidato",\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"")
		contacto_personal = Contacto.objects.create(candidato=candidato_sin_twitter, valor=u"personal@campana.cl",tipo=1)

		candidatos = Candidato.sin_datos.all()
		self.assertEquals(candidatos.count(), 1)
		self.assertEquals(candidatos[0], candidato_sin_twitter)


	def test_con_twitter_sin_mail(self):
		candidato_con_twitter = Candidato.objects.create(eleccion=self.eleccion1,\
															 nombre=u"el candidato",\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"el_twitter")


		candidatos = Candidato.sin_datos.all()
		self.assertEquals(candidatos.count(), 1)
		self.assertEquals(candidatos[0], candidato_con_twitter)

	def test_sin_mail_ni_twitter(self):
		candidato_sin_contacto = Candidato.objects.create(eleccion=self.eleccion1,\
															 nombre=u"el candidato",\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"")

		candidatos = Candidato.sin_datos.all()
		self.assertEquals(candidatos.count(), 1)
		self.assertEquals(candidatos[0], candidato_sin_contacto)

	def test_get_has_twitter_false(self):
		candidato_sin_contacto = Candidato.objects.create(eleccion=self.eleccion1,\
															 nombre=u"el candidato",\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"")

		self.assertFalse(candidato_sin_contacto.has_twitter)
		self.assertFalse(candidato_sin_contacto.has_contacto)

class NosFaltanDatosViewTestCase(TestCase):
	def setUp(self):
		self.eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", slug=u"la-eleccion1")
		self.candidato_con_todo = Candidato.objects.create(eleccion=self.eleccion1,\
															 nombre=u"el candidato con todo",\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"candidato_con_todo")
		self.contacto_personal_con_todo = Contacto.objects.create(candidato=self.candidato_con_todo, \
															valor=u"personal@campana.cl",tipo=1)

		self.candidato_sin_contacto = Candidato.objects.create(eleccion=self.eleccion1,\
															 nombre=u"el candidato",\
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