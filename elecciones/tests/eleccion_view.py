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

class EleccionViewTestCase(TestCase):
	def setUp(self):
		self.area = Area.objects.create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste")
		self.eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", slug=u"la-eleccion1", extra_info_title=u"ver más", extra_info_content=u"informacion adicional")
		self.eleccion2 = Eleccion.objects.create(nombre=u"La eleccion2", slug=u"la-eleccion2")
		ingreso_por_persona = Dato.objects.create(nombre=u"Ingreso por persona", imagen="chanchito.png")
		pobreza = Dato.objects.create(nombre=u"Pobreza", imagen="chanchito.png")
		self.indice1 = Indice.objects.create(
			eleccion =self.eleccion1,
			area = self.area,
			dato = pobreza,
			encabezado = u"encabezado",
			numero_1 = u"7%",
			texto_1 = u"de los habitantes de la eleccion son pobres",
			numero_2 = u"n2",
			texto_2 = u"t2",
			texto_pie_pagina_1 = u"En el Ranking nacional de pobreza, la eleccion está en el lugar",
			numero_pie_pagina_1 = u"1",
			texto_pie_pagina_2 = u"tpp2",
			numero_pie_pagina_2 = u"2",
			texto_pie_pagina_3 = u"tpp3",
			numero_pie_pagina_3 = u"3",
			en_carrusel = True
			)

		self.indice2 = Indice.objects.create(	
			eleccion =self.eleccion1,
			area = self.area,
			dato = pobreza,
			encabezado = u"encabezado",
			numero_1 = u"$418.891",
			texto_1 = u"es el promedio de ingreso por persona en la eleccion",
			numero_2 = u"n2",
			texto_2 = u"t2",
			texto_pie_pagina_1 = u"En el Ranking nacional de ingreso por persona, la eleccion está en el lugar",
			numero_pie_pagina_1 = u"8",
			texto_pie_pagina_2 = u"El promedio nacional de ingreso por persona es",
			numero_pie_pagina_2 = u"X",
			texto_pie_pagina_3 = u"tpp3",
			numero_pie_pagina_3 = u"3",
			en_carrusel = False)

		self.indice3 = Indice.objects.create(	
			eleccion =self.eleccion2,
			area = self.area,
			dato = ingreso_por_persona,
			encabezado = u"encabezado",
			numero_1 = u"$418.891",
			texto_1 = u"es el promedio de ingreso por persona en la eleccion",
			numero_2 = u"n2",
			texto_2 = u"t2",
			texto_pie_pagina_1 = u"En el Ranking nacional de ingreso por persona, la eleccion está en el lugar",
			numero_pie_pagina_1 = u"8",
			texto_pie_pagina_2 = u"El promedio nacional de ingreso por persona es",
			numero_pie_pagina_2 = u"X",
			texto_pie_pagina_3 = u"tpp3",
			numero_pie_pagina_3 = u"3",
			en_carrusel = True
			)
		

	def test_get_eleccion_view(self):
		url = reverse('eleccion-overview', kwargs={
			'slug':self.eleccion1.slug
			})
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'elecciones/eleccion_detail.html')
		self.assertTrue('eleccion' in response.context)
		self.assertTrue('elecciones' in response.context)
		self.assertEquals(response.context['elecciones'].count(), 2)
		self.assertEquals(response.context['eleccion'], self.eleccion1)
		self.assertTrue('title' in response.context)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'], self.eleccion1.nombre)


	def test_get_indices_elecciones(self):
		url = reverse('eleccion-overview', kwargs={
			'slug':self.eleccion1.slug
			})
		response = self.client.get(url)

		self.assertTrue('indices' in response.context)
		self.assertEquals(response.context['indices'].count(), 1)
		self.assertEquals(response.context['indices'][0], self.indice1)

	def test_muestra_solo_los_indices_que_estan_en_el_carrusel(self):
		
		url = reverse('eleccion-overview', kwargs={
			'slug':self.eleccion1.slug
			})
		response = self.client.get(url)


		self.assertEquals(response.context['indices'].count(), 1)
		self.assertEquals(response.context['indices'][0], self.indice1) # y no el indice2 que dice False en su campo en_carrusel


	def test_get_todos_los_indices_de_una_eleccion(self):
		url = reverse('eleccion-index-detail', kwargs={
			'slug':self.eleccion1.slug
			})
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertTrue('elecciones' in response.context)
		self.assertEquals(response.context['elecciones'].count(), 2)
		self.assertTrue("eleccion" in response.context)
		self.assertEquals(response.context["eleccion"], self.eleccion1)
		self.assertTrue("indices" in response.context)
		self.assertEquals(response.context["indices"].count(), 2)
		self.assertTrue(self.indice1 in response.context['indices'])
		self.assertTrue(self.indice2 in response.context['indices'])
		self.assertTemplateUsed(response, "elecciones/todos_los_indices.html")
		self.assertTemplateUsed(response, "base_sub_menu.html")
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'], self.eleccion1.nombre + u" índices detallados")

	@skip('not developed yet')
	def test_get_todos_los_indices_de_una_eleccion_como_json(self):
		url = reverse('eleccion-index-detail-json', kwargs={
			'slug':self.eleccion1.slug
			})
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.content_type, u'application/json')