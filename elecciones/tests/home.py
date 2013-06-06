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


class HomeTestCase(TestCase):
	def test_get_the_home_page(self):
		url = reverse('home')
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')

	
	def test_trae_los_nombres_de_las_elecciones_buscables(self):
		eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", slug=u"la-eleccion1")
		eleccion2 = Eleccion.objects.create(nombre=u"La eleccion2", slug=u"la-eleccion2")
		eleccion3 = Eleccion.objects.create(nombre=u"La eleccion3", slug=u"la-eleccion3",searchable=False)
		url = reverse('home')
		response = self.client.get(url)

		self.assertTrue('elecciones_buscables' in response.context)
		self.assertTrue(eleccion1 in response.context["elecciones_buscables"])
		self.assertTrue(eleccion2 in response.context["elecciones_buscables"])
		self.assertFalse(eleccion3 in response.context["elecciones_buscables"])
	
	def test_trae_los_nombres_de_las_elecciones_destacadas(self):
		eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", slug=u"la-eleccion1")
		eleccion2 = Eleccion.objects.create(nombre=u"La eleccion2", slug=u"la-eleccion2")
		eleccion3 = Eleccion.objects.create(nombre=u"La eleccion3", slug=u"la-eleccion3",featured=True)
		url = reverse('home')
		response = self.client.get(url)

		self.assertTrue('elecciones_destacadas' in response.context)
		self.assertFalse(eleccion1 in response.context["elecciones_destacadas"])
		self.assertFalse(eleccion2 in response.context["elecciones_destacadas"])
		self.assertTrue(eleccion3 in response.context["elecciones_destacadas"])

	def test_last_questions(self):

		eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", slug=u"la-eleccion1")
		eleccion2 = Eleccion.objects.create(nombre=u"La eleccion2", slug=u"la-eleccion2")
		colectivo1 = Colectivo.objects.create(sigla='C1', nombre = 'Colectivo 1')
		colectivo2 = Colectivo.objects.create(sigla='C2', nombre = 'Colectivo 2')
		data_candidato = [\
		{'nombre': 'candidato1', 'mail': 'candidato1@test.com', 'mail2' : 'candidato1@test2.com', 'mail3' : 'candidato1@test3.com', 'eleccion': eleccion1, 'partido':colectivo1, 'web': 'web1'},\
		{'nombre': 'candidato2', 'mail': 'candidato2@test.com', 'eleccion': eleccion2, 'partido': colectivo1},\
		{'nombre': 'candidato3', 'mail': 'candidato3@test.com', 'eleccion': eleccion2, 'partido':colectivo2}]
		self.popit_api_instance = PopitApiInstance.objects.create(url='http://popit.org/api/v1')
		candidato1 = Candidato.objects.create(api_instance=self.popit_api_instance, nombre=data_candidato[0]['nombre'], eleccion = eleccion1, colectivo = data_candidato[0]['partido'], web = data_candidato[0]['web'])
		candidato2 = Candidato.objects.create(api_instance=self.popit_api_instance, nombre=data_candidato[1]['nombre'], eleccion = eleccion1, colectivo = data_candidato[1]['partido'])
		#crea muchas preguntas y respuestas
		for i in range(7):
			texto_pregunta='texto pregunta '+ str(i)
			texto_respuesta='texto respuesta '+ str(i)
			remitente='Remitente ' + str(i)
			pregunta = Pregunta.objects.create(texto_pregunta=texto_pregunta, remitente=remitente)
			Respuesta.objects.create(texto_respuesta = texto_pregunta, pregunta=pregunta, candidato=candidato1)

		url = reverse('home')
		response = self.client.get(url)

		self.assertEquals(Pregunta.objects.all().count(), 7)
		self.assertEquals(Respuesta.objects.all().count(), 7)
		self.assertEquals(response.context['ultimas_preguntas'].count(),5)
		self.assertEquals(response.context['ultimas_respuestas'].count(),5)
