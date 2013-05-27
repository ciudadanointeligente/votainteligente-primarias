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


class DatoTestCase(TestCase):
	def test_create_dato(self):
		dato, created = Dato.objects.get_or_create(nombre=u"Pobreza", imagen="chanchito.png")

		self.assertTrue(created)
		self.assertEquals(dato.nombre, u"Pobreza")
		self.assertEquals(dato.imagen, u"chanchito.png")


	def test_unicode(self):
		dato = Dato.objects.create(nombre=u"Pobreza", imagen="chanchito.png")


		self.assertEquals(dato.__unicode__(), u"Pobreza")