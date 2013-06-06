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
from django.conf import settings
from popit.models import ApiInstance as PopitApiInstance, Person

class ContactosLoaderTestCase(TestCase):
	def setUp(self):
		self.colectivo1 = Colectivo.objects.create(sigla='C1', nombre='Colectivo 1')
		self.line1 = ["FIERA FEROZ","Algarrobo","fieripipoo@ciudadanointeligente.cl"]
		self.line2 = ["FIERA FEROZ INTELIGENTE","Algarrobo","este no es el mail de la Fiera"]
		self.line3 = ["FIERA FEROZ INTELIGENTE","Algarrobo",""]
		self.lines = [self.line1, self.line2]

		self.algarrobo = Eleccion.objects.create(nombre=u"Algarrobo", slug=u"algarrobo")
		self.candidateloader = ContactosLoader()
		self.popit_api_instance, created = PopitApiInstance.objects.get_or_create(url=settings.POPIT_API_URL)


	def test_get_popit_api_instance(self):
		api_instance = self.candidateloader.getPopitApiInstance()
		self.assertEquals(api_instance.url, settings.POPIT_API_URL)

		self.assertEquals(self.candidateloader.popit_api_instance.url, settings.POPIT_API_URL)



	def test_create_detect_candidate(self):
		
		candidate = self.candidateloader.detectCandidate(self.line1)

		self.assertEquals(candidate.nombre, u"FIERA FEROZ")
		self.assertEquals(candidate.eleccion, self.algarrobo)

	def test_detect_contacto(self):
		candidate = self.candidateloader.detectCandidate(self.line1)
		contacto = self.candidateloader.detectContacto(self.line1)

		self.assertEquals(contacto.valor, u"fieripipoo@ciudadanointeligente.cl")
		self.assertEquals(contacto.candidato, candidate)


	def test_does_not_create_contacto_if_it_isnt_a_mail(self):
		contacto = self.candidateloader.detectContacto(self.line2)

		self.assertTrue(contacto is None)
		self.assertEquals(len(self.candidateloader.failed),1)
		self.assertEquals(self.candidateloader.failed[0],{u"Algarrobo",u"FIERA FEROZ INTELIGENTE",u"este no es el mail de la Fiera"})

	def test_does_not_create_two_candidates(self):
		previous_candidate = Candidato.objects.create(api_instance=self.popit_api_instance, 
			nombre=u"FIERA FEROZ", 
			eleccion=self.algarrobo, 
			partido=u"Partido Feroz", 
			colectivo=self.colectivo1)
		contacto = self.candidateloader.detectContacto(self.line1)

		self.assertEquals(Candidato.objects.all().count(), 1)

	def test_empty_emails_do_not_belong_to_fail(self):
		contacto = self.candidateloader.detectContacto(self.line3)
		self.assertTrue(contacto is None)

		self.assertEquals(len(self.candidateloader.empty),1)
		self.assertEquals(self.candidateloader.empty[0],{u"Algarrobo",u"FIERA FEROZ INTELIGENTE"})


	def test_it_does_not_create_two_candidates(self):

		contacto = self.candidateloader.detectContacto(self.line2)
		contacto = self.candidateloader.detectContacto(self.line2)

		self.assertEquals(Candidato.objects.all().count(), 1)








	##TODO: Testear la clase command y el metodo handle sin crear conflicto con la otra clase
	##Command del elecciones_importer