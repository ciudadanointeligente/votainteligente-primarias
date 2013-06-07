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


class CandidatoTestCase(TestCase):
	def setUp(self):
		self.popit_api_instance = ApiInstance.objects.create(url='http://popit.org/api/v1')
		self.eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", popit_api_instance=self.popit_api_instance, slug=u"la-eleccion1")
		self.person = Person.objects.create(api_instance =  self.popit_api_instance, name='person_name')

	def test_create_candidato(self):
		candidato, created = Candidato.objects.get_or_create(person=self.person,
															 eleccion=self.eleccion1,\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",\
															 twitter=u"candidato")

		self.assertTrue(created)
		self.assertEquals(candidato.eleccion, self.eleccion1)
		self.assertEquals(candidato.nombre, self.person.name)
		self.assertEquals(candidato.partido, u"API")
		self.assertEquals(candidato.web, u"http://votainteURLligente.cl")
		self.assertEquals(candidato.twitter, "candidato")

	def test_create_candidato_with_a_person(self):
		candidato, created = Candidato.objects.get_or_create(person=self.person,
															 eleccion=self.eleccion1,\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",\
															 twitter=u"candidato")

		self.assertTrue(created)
		self.assertEquals(candidato.person, self.person)


	def test_get_name_from_person(self):
		candidato, created = Candidato.objects.get_or_create(person=self.person,
															 eleccion=self.eleccion1,\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",\
															 twitter=u"candidato")

		self.assertEquals(candidato.nombre, self.person.name)



	def test_create_candidato_without_twitter(self):
		candidato, created = Candidato.objects.get_or_create(person=self.person,
															 eleccion=self.eleccion1,\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl")

		self.assertTrue(created)
		self.assertFalse(candidato.twitter)

	def test_create_candidato_with_empty_twitter(self):
		candidato,created = Candidato.objects.get_or_create(person=self.person,
															 eleccion=self.eleccion1,\
															 partido=u"API",\
															 web=u"http://votainteURLligente.cl",
															 twitter=u"")
		self.assertTrue(created)
		self.assertFalse(candidato.twitter)




	def test_preguntas_del_candidato(self):
		candidato = Candidato.objects.create(person=self.person,
											 eleccion=self.eleccion1,\
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
		candidato = Candidato.objects.create(person=self.person,
											 eleccion=self.eleccion1,\
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

	#@skip("Elections must be created before")
	def test_create_candidate_from_person(self):
		
		fiera = Person.objects.create(api_instance=self.popit_api_instance, name='Fiera')
		candidato = Candidato.objects.get(person=fiera)

		self.assertTrue(candidato)
		self.assertEquals(candidato.eleccion, self.eleccion1)

	def test_create_candidate_only_once_from_person(self):
		fiera = Person.objects.create(api_instance=self.popit_api_instance, name='Fiera')
		fiera.save()

		self.assertEquals(Candidato.objects.filter(person=fiera).count(),1)
