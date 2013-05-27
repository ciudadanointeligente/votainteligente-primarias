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

class IndiceTestCase(TestCase):
	def test_create_indice(self):
		area = Area.objects.create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste")
		pobreza = Dato.objects.create(nombre=u"Pobreza", imagen="chanchito.png")
		eleccion = Eleccion.objects.create(nombre=u"La eleccion", 
										slug=u"la-eleccion",
										main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
										messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
										mapping_extra_app_url=u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		indice, created = Indice.objects.get_or_create(
			eleccion =eleccion,
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


		self.assertTrue(created)
		self.assertEquals(indice.eleccion, eleccion)
		self.assertEquals(indice.area, area)
		self.assertEquals(indice.dato, pobreza)
		self.assertEquals(indice.encabezado, u"encabezado")
		self.assertEquals(indice.numero_1, u"7%")
		self.assertEquals(indice.texto_1, u"de los habitantes de la comuna son pobres")
		self.assertEquals(indice.numero_2, u"n2")
		self.assertEquals(indice.texto_2, u"t2")
		self.assertEquals(indice.texto_pie_pagina_1, u"En el Ranking nacional de pobreza, la comuna está en el lugar")
		self.assertEquals(indice.numero_pie_pagina_1, u"1")
		self.assertEquals(indice.texto_pie_pagina_2,u"tpp2")
		self.assertEquals(indice.numero_pie_pagina_2,u"2")
		self.assertEquals(indice.texto_pie_pagina_3, u"tpp3")
		self.assertEquals(indice.numero_pie_pagina_3, u"3")

	def test_unicode(self):
		area = Area.objects.create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste", segunda_clase=u"colorCeleste")
		ingreso_por_persona = Dato.objects.create(nombre=u"Ingreso por persona", imagen="chanchito.png")
		eleccion = Eleccion.objects.create(nombre=u"La eleccion", 
										slug=u"la-eleccion",
										main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
										messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
										mapping_extra_app_url=u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		indice = Indice.objects.create(	
			eleccion =eleccion,
			area = area,
			dato = ingreso_por_persona,
			encabezado = u"encabezado",
			numero_1 = u"$418.891",
			texto_1 = u"es el promedio de ingreso por persona en la comuna",
			numero_2 = u"n2",
			texto_2 = u"t2",
			texto_pie_pagina_1 = u"En el Ranking nacional de ingreso por persona, la comuna está en el lugar",
			numero_pie_pagina_1 = u"8",
			texto_pie_pagina_2 = u"El promedio nacional de ingreso por persona es",
			numero_pie_pagina_2 = u"X",
			texto_pie_pagina_3 = u"tpp3",
			numero_pie_pagina_3 = u"3",
			en_carrusel = False)

		self.assertEquals(indice.__unicode__(), u"Ingreso por persona - La eleccion")