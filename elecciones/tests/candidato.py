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
from popit.models import ApiInstance as PopitApiInstance, Person
from unittest import skip


class CandidatoTestCase(TestCase):
	def setUp(self):
		self.eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", slug=u"la-eleccion1")
		self.popit_api_instance = PopitApiInstance.objects.create(url='http://popit.org/api/v1')

	def test_create_candidato(self):
		candidato, created = Candidato.objects.get_or_create(
			api_instance=self.popit_api_instance,
			eleccion=self.eleccion1,\
															 nombre=u"el candidato",\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",\
															 twitter=u"candidato")

		self.assertTrue(created)
		self.assertEquals(candidato.eleccion, self.eleccion1)
		self.assertEquals(candidato.nombre, u"el candidato")
		self.assertEquals(candidato.partido, u"API")
		self.assertEquals(candidato.web, u"http://votainteURLligente.cl")
		self.assertEquals(candidato.twitter, "candidato")

	def test_create_candidato_without_election(self):

		candidato, created = Candidato.objects.get_or_create(
			api_instance=self.popit_api_instance,
															 nombre=u"el candidato",\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",\
															 twitter=u"candidato")

		self.assertTrue(created)
		self.assertEquals(candidato.nombre, u"el candidato")
		self.assertEquals(candidato.partido, u"API")
		self.assertEquals(candidato.web, u"http://votainteURLligente.cl")
		self.assertEquals(candidato.twitter, "candidato")


	@skip("not this aproach")
	def test_when_I_create_a_popit_person_then_it_creates_a_candidato(self):
		popit_api_instance = PopitApiInstance.objects.create(url='http://popit.org/api/v1')
		person1 = Person.objects.create(
            api_instance=popit_api_instance, 
            name= "Felipe", 
            popit_url= 'http://popit.org/api/v1/persons/3')


		self.assertEquals(Candidato.objects.count(), 1)
		el_candidato = Candidato.objects.all()[0]
		self.assertEquals(el_candidato.nombre, person1.name)


	def test_create_candidato_without_twitter(self):
		candidato, created = Candidato.objects.get_or_create(api_instance=self.popit_api_instance,
															eleccion=self.eleccion1,\
															nombre=u"el candidato",\
															partido=u"API",\
															web=u"http://votainteURLligente.cl")

		self.assertTrue(created)
		self.assertFalse(candidato.twitter)

	def test_create_candidato_with_empty_twitter(self):
		candidato,created = Candidato.objects.get_or_create(api_instance=self.popit_api_instance,
															eleccion=self.eleccion1,\
															nombre=u"el candidato",\
															partido=u"API",\
															web=u"http://votainteURLligente.cl",
															twitter=u"")
		self.assertTrue(created)
		self.assertFalse(candidato.twitter)


	def test_preguntas_del_candidato(self):
		candidato = Candidato.objects.create(api_instance=self.popit_api_instance,
											eleccion=self.eleccion1,\
											nombre=u"el candidato",\
											partido=u"API",\
											web=u"http://votainteURLligente.cl",
											twitter=u"")
		pregunta = Pregunta.objects.create(
											remitente='remitente1', 
											texto_pregunta='texto_pregunta1')
		respuesta = Respuesta.objects.create(pregunta=pregunta, candidato=candidato)

		self.assertTrue(candidato.pregunta.count(), 1)
		self.assertTrue(candidato.pregunta.all()[0], pregunta)


	def test_preguntas_respondidas(self):
		candidato = Candidato.objects.create(api_instance=self.popit_api_instance,
											eleccion=self.eleccion1,\
											nombre=u"el candidato",\
											partido=u"API",\
											web=u"http://votainteURLligente.cl",
											twitter=u"")
		pregunta = Pregunta.objects.create(
											remitente='remitente1', 
											texto_pregunta='texto_pregunta1')
		pregunta_no_respondida = Pregunta.objects.create(
											remitente='remitente1', 
											texto_pregunta='es usted mala onda?')

		respuesta = Respuesta.objects.create(pregunta=pregunta, candidato=candidato, texto_respuesta=u"yo opino que guau guau")
		sin_respuesta = Respuesta.objects.create(pregunta=pregunta_no_respondida, candidato=candidato)

		self.assertTrue(candidato.preguntas_respondidas.count(), 1)
		self.assertTrue(candidato.preguntas_respondidas.all()[0], pregunta)