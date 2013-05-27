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

class TemplatesViewsTestCase(TestCase):
	def setUp(self):
		self.eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", slug=u"la-eleccion1")
		self.eleccion2 = Eleccion.objects.create(nombre=u"La eleccion2", slug=u"la-eleccion2")


	def test_get_metodologia(self):
		url = reverse('metodologia')
		response = self.client.get(url)

		self.assertTrue('elecciones' in response.context)
		self.assertEquals(response.context['elecciones'].count(), 2)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'], u"Metodología")
		self.assertTemplateUsed(response, 'elecciones/metodologia.html')

	def test_get_quienes_somos(self):
		url = reverse('somos')
		response = self.client.get(url)

		self.assertTemplateUsed(response, 'quienesSomos.html')

		self.assertEquals(response.status_code, 200)
		self.assertTrue('elecciones' in response.context)
		self.assertEquals(response.context['elecciones'].count(), 2)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'], u"Quienes somos")

	def test_get_reporta(self):
		url = reverse('reporta')
		response = self.client.get(url)

		self.assertTemplateUsed(response, 'elecciones/reporta.html')

		self.assertEquals(response.status_code, 200)
		self.assertTrue('elecciones' in response.context)
		self.assertEquals(response.context['elecciones'].count(), 2)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'], u"Fiscaliza")


	def test_get_que_puedo_hacer(self):
		url = reverse('que_puedo_hacer')
		response = self.client.get(url)

		self.assertTemplateUsed(response, 'elecciones/que_puedo_hacer.html')
		self.assertEquals(response.status_code, 200)
		self.assertTrue('elecciones' in response.context)
		self.assertEquals(response.context['elecciones'].count(), 2)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'],u"¿Qué puedo hacer?")

	def test_get_extra_info(self):
		url = reverse('eleccion-extra-info',kwargs={'slug':self.eleccion1.slug})
		response = self.client.get(url)

		self.assertTemplateUsed(response, 'elecciones/extra_info.html')
		self.assertEquals(response.status_code, 200)
		self.assertTrue('title' in response.context)
		self.assertTrue('eleccion' in response.context)
		self.assertEquals(response.context['title'],u"Más Información sobre La eleccion1")

	def test_get_voluntarios(self):
		url = reverse('voluntarios')
		response = self.client.get(url)

		self.assertTemplateUsed(response, 'voluntarios.html')
		self.assertEquals(response.status_code, 200)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'],u"Gracias a TODOS")

	def test_get_senadores(self):
		url = reverse('senadores')
		response = self.client.get(url)

		self.assertTemplateUsed(response, 'todos_los_senadores.html')
		self.assertEquals(response.status_code, 200)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'],u"Todos los Senadores")

