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

class CsvReaderTestOneLine(TestCase):
    def setUp(self):
        self.csvreader = CsvReader()
        self.line =["Algarrobo","Caracterización",u"Pobreza",u"encabezado","3,97",
            u"Es el porcentaje de habitantes de la eleccion que viven bajo la línea de la pobreza",u"n2",u"t2",
            u"En el ranking nacional de pobreza, la eleccion se ubica en el lugar",u"326",u" y eso es malo","247" ,"del ranking nacional", "SI"]

        self.line1 =["Algarrobo","Caracterización",u"Desigualdad",u"encabezado","3,97",
            		u"Es el porcentaje de habitantes de la eleccion que viven bajo la línea de la pobreza",
            		u"n2",u"t2",u"En el ranking nacional de pobreza, la eleccion se ubica en el lugar",u"326",
                    u" y eso es malo", "247", "del ranking nacional", "SI"]

        self.line2 =["Algarrobo","Caracterización",u"Pobreza",u"encabezado2","4",
            u"texto2",u"n2",u"t2",
            u"texto nacional 2",u"426",u" y eso es muy malo", "247" , "del ranking nacional", "NO"]
        self.line3 =["Algarrobo  ", "Caracterización ", "Pobreza ","encabezado2","4",
            "texto2","n2","t2",
            "texto nacional 2","426"," y eso es muy malo","247","del ranking nacional", "SI"]


    def test_crea_indice_en_carrusel_y_fuera_de_el(self):
    	indice = self.csvreader.detectIndice(self.line1)
    	self.assertTrue(indice.en_carrusel)

        indice = self.csvreader.detectIndice(self.line2)
        self.assertFalse(indice.en_carrusel)


    def test_actualiza_indice(self):
        indice = self.csvreader.detectIndice(self.line)
        indice = self.csvreader.detectIndice(self.line2)

        self.assertEquals(Indice.objects.count(), 1)
        self.assertEquals(indice.eleccion.nombre, u"Algarrobo")
        self.assertEquals(indice.area.nombre, u"Caracterización")
        self.assertEquals(indice.dato.nombre, u"Pobreza")
        self.assertEquals(indice.encabezado, u"encabezado2")
        self.assertEquals(indice.numero_1, u"4")
        self.assertEquals(indice.texto_1, u"texto2")
        self.assertEquals(indice.numero_2, u"n2")
        self.assertEquals(indice.texto_2, u"t2")
        self.assertEquals(indice.texto_pie_pagina_1, u"texto nacional 2")
        self.assertEquals(indice.numero_pie_pagina_1, u"426")
        self.assertEquals(indice.texto_pie_pagina_2, u"y eso es muy malo")
        self.assertEquals(indice.texto_pie_pagina_3, u"del ranking nacional")
        self.assertEquals(indice.numero_pie_pagina_2 ,u"247")
        
    
    def test_detect_indice(self):
    	indice = self.csvreader.detectIndice(self.line)


        self.assertEquals(indice.eleccion.nombre, u"Algarrobo")
        self.assertEquals(indice.area.nombre, u"Caracterización")
        self.assertEquals(indice.dato.nombre, u"Pobreza")
        self.assertEquals(indice.encabezado, u"encabezado")
        self.assertEquals(indice.numero_1, u"3,97")
        self.assertEquals(indice.texto_1, u"Es el porcentaje de habitantes de la eleccion que viven bajo la línea de la pobreza")
        self.assertEquals(indice.numero_2, u"n2")
        self.assertEquals(indice.texto_2, u"t2")
        self.assertEquals(indice.texto_pie_pagina_1, u"En el ranking nacional de pobreza, la eleccion se ubica en el lugar")
        self.assertEquals(indice.numero_pie_pagina_1, u"326")
        self.assertEquals(indice.texto_pie_pagina_2,u"y eso es malo")


    def test_does_not_create_two_indices_for_the_same_eleccion_with_the_same_dato(self):
    	indice = self.csvreader.detectIndice(self.line)
        indice = self.csvreader.detectIndice(self.line)

        self.assertEquals(Indice.objects.count(), 1)

    def test_but_it_does_when_different_dato(self):
        indice = self.csvreader.detectIndice(self.line)
        indice = self.csvreader.detectIndice(self.line1)

        self.assertEquals(Indice.objects.count(), 2)






    def test_detect_eleccion_out_of_a_line(self):
        eleccion = self.csvreader.detectEleccion(self.line)

        self.assertEquals(Eleccion.objects.count(), 1)
        self.assertEquals(eleccion.nombre, u"Algarrobo")
        self.assertEquals(eleccion.slug, u"algarrobo")

    def test_does_not_create_two_elecciones(self):
    	eleccion = self.csvreader.detectEleccion(self.line)
    	eleccion = self.csvreader.detectEleccion(self.line)

    	self.assertEquals(Eleccion.objects.count(), 1)


    def test_does_not_create_two_elecciones_with_spaces(self):
    	eleccion = self.csvreader.detectEleccion(self.line2)
    	eleccion = self.csvreader.detectEleccion(self.line3)

        self.assertEquals(Eleccion.objects.count(), 1)

    def test_detect_area(self):
        area = self.csvreader.detectArea(self.line)

        self.assertEquals(Area.objects.count(), 1)
        self.assertEquals(area.nombre, u"Caracterización")


    def test_it_does_not_create_two_areas(self):
        area = self.csvreader.detectArea(self.line)
        area = self.csvreader.detectArea(self.line)

        self.assertEquals(Area.objects.count(), 1)

    def test_it_does_not_create_two_areas_even_with_spaces(self):
    	area = self.csvreader.detectArea(self.line2)
    	area = self.csvreader.detectArea(self.line3)

    	self.assertEquals(Area.objects.count(), 1)
    	self.assertEquals(area.nombre, u"Caracterización")


    def test_detect_dato(self):
        dato = self.csvreader.detectDato(self.line)

        self.assertEquals(dato.nombre, u"Pobreza")


    def test_it_does_not_create_twice_the_same_dato(self):
    	dato = self.csvreader.detectDato(self.line2)
    	dato = self.csvreader.detectDato(self.line3)

    	self.assertEquals(Dato.objects.count(), 1)