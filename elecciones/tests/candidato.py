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

	def test_create_candidato_only_out_of_persons_attributes(self):
		candidato, created = Candidato.objects.get_or_create(
			api_instance=self.popit_api_instance,name='the_candidate')

		self.assertTrue(created)
		self.assertEquals(candidato.nombre,candidato.name)


	def test_create_a_candidato_without_election(self):
		candidato = Candidato.objects.create(
			api_instance=self.popit_api_instance,
															 nombre=u"el candidato",\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",\
															 twitter=u"candidato")
		self.assertTrue(candidato)


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

from popit.tests import instance_helpers
from mock import patch
from django.core.management import call_command


class CandidatoLoaderFromPopitApiCommand(TestCase):
	def test_command(self):

		with patch('popit.models.PopItDocument.fetch_all_from_api') as get:
			get.return_value = 'oli'
			api_instance, created = PopitApiInstance.objects.get_or_create(url=settings.POPIT_API_URL)

			call_command('get_candidatos_from_popit')

			get.assert_called_with(instance=api_instance)



