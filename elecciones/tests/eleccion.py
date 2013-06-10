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
from django.db import IntegrityError
from popit.models import Person, ApiInstance
from writeit.models import WriteItApiInstance, WriteItInstance

class EleccionModelTestCase(TestCase):
	def test_create_eleccion(self):
		popit_api_instance = ApiInstance.objects.create(url='http://popit.org/api/v1')
		write_it_api_instance = WriteItApiInstance.objects.create(url="http://witeit.ciudadanointeligente.org/api/v1")
		write_it_instance = WriteItInstance.objects.create(api_instance = write_it_api_instance, name="new_instance")
		eleccion, created = Eleccion.objects.get_or_create(nombre=u"La eleccion",
														popit_api_instance=popit_api_instance,
														write_it_instance=write_it_instance,
														slug=u"la-eleccion",
														main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
														messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
														mapping_extra_app_url=u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278",
														featured_caption = u"Texto Destacado",
														extra_info_title = u"ver más",
														extra_info_content=u"Más Información")
		self.assertTrue(created)
		self.assertEquals(eleccion.nombre, u"La eleccion")
		self.assertEquals(eleccion.slug, u"la-eleccion")
		self.assertEquals(eleccion.main_embedded, u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded")
		self.assertEquals(eleccion.messaging_extra_app_url, u"http://napistejim.cz/address=nachod")
		self.assertEquals(eleccion.mapping_extra_app_url, u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		self.assertTrue(eleccion.searchable)
		self.assertFalse(eleccion.featured)
		self.assertEquals(eleccion.featured_caption,u"Texto Destacado")
		self.assertEquals(eleccion.extra_info_title,u"ver más")
		self.assertEquals(eleccion.extra_info_content,u"Más Información")
		self.assertEquals(eleccion.popit_api_instance, popit_api_instance)
		self.assertEquals(eleccion.write_it_instance, write_it_instance)


	def test_eleccion_unicode(self):
		popit_api_instance = ApiInstance.objects.create(url='http://popit.org/api/v1')
		write_it_api_instance = WriteItApiInstance.objects.create(url="http://witeit.ciudadanointeligente.org/api/v1")
		write_it_instance = WriteItInstance.objects.create(api_instance = write_it_api_instance, name="new_instance")
		eleccion = Eleccion.objects.create(nombre=u"La eleccion", popit_api_instance=popit_api_instance, write_it_instance=write_it_instance, slug=u"la-eleccion")

		self.assertEquals(eleccion.__unicode__(), eleccion.nombre)

	def test_eleccion_has_a_unique_popit_api_instance(self):
		popit_api_instance = ApiInstance.objects.create(url='http://popit.org/api/v1')
		write_it_api_instance = WriteItApiInstance.objects.create(url="http://witeit.ciudadanointeligente.org/api/v1")
		write_it_instance = WriteItInstance.objects.create(api_instance = write_it_api_instance, name="new_instance")
		eleccion1 = Eleccion.objects.create(nombre=u"La eleccion", popit_api_instance=popit_api_instance, write_it_instance=write_it_instance, slug=u"la-eleccion")

		with self.assertRaises(IntegrityError):
			eleccion2 = Eleccion.objects.create(nombre=u"La eleccion2", popit_api_instance=popit_api_instance, slug=u"la-eleccion2")