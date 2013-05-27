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

class CandidatosEstrellitas(TestCase):
	def setUp(self):
		self.colectivo1 = Colectivo.objects.create(sigla='C1', nombre='Colectivo 1')
		self.eleccion = Eleccion.objects.create(nombre=u"La eleccion", slug="la-eleccion")
		self.candidato = Candidato.objects.create(nombre=u"Un candidato mala onda", 
													partido=u"RN", 
													eleccion=self.eleccion, 
													colectivo=self.colectivo1)


	def test_candidato_tres_estrellitas(self):
		#No hay contactos
		self.assertEquals(self.candidato.estrellitas, 3)

	def test_candidato_dos_estrellitas(self):
		contacto_personal = Contacto.objects.create(candidato=self.candidato, valor=u"secretaria@rn.cl",tipo=2)

		self.assertEquals(self.candidato.estrellitas, 2)


	def test_candidato_una_estrella(self):
		contacto_personal = Contacto.objects.create(candidato=self.candidato, valor=u"yo-soy-un-weon-malo@rn.cl",tipo=1)

		self.assertEquals(self.candidato.estrellitas, 1)

	def test_candidato_una_estrella_con_dos_contactos(self):
		contacto_personal = Contacto.objects.create(candidato=self.candidato, valor=u"secretaria@rn.cl",tipo=2)
		contacto_personal = Contacto.objects.create(candidato=self.candidato, valor=u"yo-soy-un-weon-malo@rn.cl",tipo=1)

		self.assertEquals(self.candidato.estrellitas, 1)
