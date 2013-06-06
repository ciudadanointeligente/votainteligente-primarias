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


class TemplateTagsTesting(TestCase):
	def setUp(self):
		area = Area.objects.create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste")
		pobreza = Dato.objects.create(nombre=u"Pobreza", imagen="chanchito.png")
		self.eleccion = Eleccion.objects.create(nombre=u"La eleccion", 
										slug=u"la-eleccion",
										main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
										)
		self.indice = Indice.objects.create(
			eleccion =self.eleccion,
			area = area,
			dato = pobreza,
			encabezado = u"encabezado",
			numero_1 = u"7%",
			texto_1 = u"de los habitantes de la comuna son pobres",
			numero_2 = u"n2",
			texto_2 = u"t2",
			texto_pie_pagina_1 = u"En el Ranking nacional de pobreza, la comuna está en el lugar",
			numero_pie_pagina_1 = u"1",
			texto_pie_pagina_2 = u"tpp2",
			numero_pie_pagina_2 = u"2",
			texto_pie_pagina_3 = u"tpp3",
			numero_pie_pagina_3 = u"3",
			en_carrusel = True
			)
		self.popit_api_instance = ApiInstance.objects.create(url='http://popit.org/api/v1')
		self.person = Person.objects.create(api_instance =  self.popit_api_instance, name='person_name')
		self.candidato = Candidato.objects.create(person=self.person,
															 eleccion=self.eleccion,\
															 partido=u"API",\
															 web=u"http://unaurl.cl",\
															 twitter=u"candidato")
	@skip('no tenemos domain')
	def test_no_responden_diles_algo(self):
		expected_html = '<a href="https://twitter.com/intent/tweet" data-text="1 preguntas de ciudadanos no han sido respondidas por @candidato, revisalas en {% url index %}/la-eleccion/preguntales" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Tweet to @candidato</a>'
		template = Template("{% load twitter_tags %}{{ malo|no_responde }}")
		context = Context({"malo": {'candidato':self.candidato,'preguntas_no_respondidas':1} })


		self.assertEqual(template.render(context), expected_html)


	@skip('no tenemos domain')
	def test_si_responden_dales_las_gracias(self):
		expected_html = '<a href="https://twitter.com/intent/tweet" data-text="Gracias @candidato por responder a los ciudadanos en {% url index %}/la-eleccion/preguntales" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Tweet to @candidato</a>'
		template = Template("{% load twitter_tags %}{{ bueno|si_responde }}")
		context = Context({"bueno": {'candidato':self.candidato,'preguntas_respondidas':1} })


		self.assertEqual(template.render(context), expected_html)


	def test_trae_todas_las_elecciones_buscables(self):
		eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", 
									slug=u"la-eleccion1",
									main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
									messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
									mapping_extra_app_url=u"")
		eleccion2 = Eleccion.objects.create(nombre=u"La eleccion2", 
									slug=u"la-eleccion2",
									main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
									messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
									mapping_extra_app_url=u"")
		eleccion3 = Eleccion.objects.create(nombre=u"La eleccion3", 
									slug=u"la-eleccion3",
									main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
									messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
									mapping_extra_app_url=u"",
									searchable=False)
		eleccion4 = Eleccion.objects.create(nombre=u"La eleccion4", 
									slug=u"la-eleccion4",
									main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
									messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
									mapping_extra_app_url=u"",
									featured=True)

		expected_html = '{label:"La eleccion",value:"la-eleccion"},{label:"La eleccion1",value:"la-eleccion1"},{label:"La eleccion2",value:"la-eleccion2"},{label:"La eleccion4",value:"la-eleccion4"}'
		template = Template("{% load elecciones_templatetags %}{% elecciones_search %}")

		context = Context({})

		self.assertEqual(template.render(context), expected_html)
	# @skip('calibrando el test')
	def test_trae_todas_las_elecciones_destacadas(self):
		eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", 
									slug=u"la-eleccion1",
									main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
									messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
									mapping_extra_app_url=u"")
		eleccion2 = Eleccion.objects.create(nombre=u"La eleccion2", 
									slug=u"la-eleccion2",
									main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
									messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
									mapping_extra_app_url=u"",
									featured=True)
		eleccion3 = Eleccion.objects.create(nombre=u"La eleccion3", 
									slug=u"la-eleccion3",
									main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
									messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
									mapping_extra_app_url=u"",
									searchable=False)
		eleccion4 = Eleccion.objects.create(nombre=u"La eleccion4", 
									slug=u"la-eleccion4",
									main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
									messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
									mapping_extra_app_url=u"",
									featured=True,
									featured_caption = "Eleccion 4 Destacada")

		expected_html = '{label:"La eleccion2",value:"la-eleccion2"},{label:"La eleccion4",value:"la-eleccion4",text:"Eleccion 4 Destacada"}'
		template = Template("{% load elecciones_templatetags %}{% elecciones_destacadas %}")

		context = Context({})

		self.assertEqual(template.render(context), expected_html)




