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



class AreaTestCase(TestCase):
	def test_create_area(self):
		area, created = Area.objects.get_or_create(
			nombre=u"Caracterización", 
			clase_en_carrusel=u"fondoCeleste") 

		
		self.assertTrue(created)
		self.assertEquals(area.nombre, u'Caracterización')
		self.assertEquals(area.clase_en_carrusel,u"fondoCeleste")

	def test_unicode(self):
		area = Area.objects.create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste")
		self.assertEquals(area.__unicode__(), u"Caracterización")