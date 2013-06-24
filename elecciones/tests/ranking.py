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
from elecciones.views import Ranking
from django.conf import settings
from django.utils import simplejson as json


class RankingTestCase(TestCase):

	def setUp(self):
		self.popit_api_instance1 = ApiInstance.objects.create(url='http://popit.org/api/v1')
		self.popit_api_instance2 = ApiInstance.objects.create(url='http://popit.org/api/v2')
		self.popit_api_instance3 = ApiInstance.objects.create(url='http://popit.org/api/v3')
		self.eleccion1, created = Eleccion.objects.get_or_create(nombre="eleccion1",
			popit_api_instance=self.popit_api_instance1,
			slug="la-eleccion1",
			main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
			messaging_extra_app_url="http://napistejim.cz/address=nachod",
			mapping_extra_app_url="http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		self.eleccion2, created = Eleccion.objects.get_or_create(nombre="eleccion2", 
			popit_api_instance=self.popit_api_instance2,
			slug="la-eleccion2",
			main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
			messaging_extra_app_url="http://napistejim.cz/address=nachod",
			mapping_extra_app_url="http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		self.eleccion3, created = Eleccion.objects.get_or_create(nombre="eleccion3", 
			popit_api_instance=self.popit_api_instance3	,
			slug="la-eleccion3",
			main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
			messaging_extra_app_url="http://napistejim.cz/address=nachod",
			mapping_extra_app_url="http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		self.colectivo1 = Colectivo.objects.create(sigla='C1', nombre = 'Colectivo 1')
		self.colectivo2 = Colectivo.objects.create(sigla='C2', nombre = 'Colectivo 2')
		self.data_candidato = [\
		{'nombre': 'candidato1', 'mail': 'candidato1@test.com', 'mail2' : 'candidato1@test2.com', 'mail3' : 'candidato1@test3.com', 'eleccion': self.eleccion1, 'partido':self.colectivo1, 'web': 'web1'},\
		{'nombre': 'candidato2', 'mail': 'candidato2@test.com', 'eleccion': self.eleccion2, 'partido': self.colectivo1},\
		{'nombre': 'candidato3', 'mail': 'candidato3@test.com', 'eleccion': self.eleccion3, 'partido':self.colectivo2}]
		person1 = Person.objects.create(api_instance =  self.popit_api_instance1, name="candidato1")
		person2 = Person.objects.create(api_instance =  self.popit_api_instance1, name="candidato2")
		person3 = Person.objects.create(api_instance =  self.popit_api_instance1, name="candidato3")
		person4 = Person.objects.create(api_instance =  self.popit_api_instance1, name="candidato4")
		Candidato.objects.create(person=person1, eleccion = self.eleccion1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(person=person1, eleccion = self.eleccion1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(person=person1, eleccion = self.eleccion1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(person=person1, eleccion = self.eleccion1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(person=person1, eleccion = self.eleccion1, colectivo = self.data_candidato[1]['partido'])
		

		self.candidato1 = Candidato.objects.create(person=person1, eleccion = self.eleccion1, colectivo = self.data_candidato[0]['partido'], web = self.data_candidato[0]['web'])
		self.candidato2 = Candidato.objects.create(person=person2, eleccion = self.eleccion1, colectivo = self.data_candidato[1]['partido'])
		self.candidato3 = Candidato.objects.create(person=person3, eleccion = self.eleccion1, colectivo = self.data_candidato[2]['partido'])
		self.candidato4 = Candidato.objects.create(person=person4, eleccion = self.eleccion1, colectivo = self.data_candidato[2]['partido'])
		
		Candidato.objects.create(person=person1, eleccion = self.eleccion1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(person=person1, eleccion = self.eleccion1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(person=person1, eleccion = self.eleccion1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(person=person1, eleccion = self.eleccion1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(person=person1, eleccion = self.eleccion1, colectivo = self.data_candidato[1]['partido'])

		self.pregunta1 = Pregunta.objects.create(
											remitente='remitente1', 
											texto_pregunta='texto_pregunta1',
											aprobada=True)
		self.respuesta1 = Respuesta.objects.create(pregunta=self.pregunta1, candidato=self.candidato1)
		self.respuesta2 = Respuesta.objects.create(pregunta=self.pregunta1, candidato=self.candidato2)
		self.respuesta3 = Respuesta.objects.create(pregunta=self.pregunta1, candidato=self.candidato3)
		self.respuesta1_c4 = Respuesta.objects.create(pregunta=self.pregunta1, candidato=self.candidato4)

		self.pregunta2 = Pregunta.objects.create(
											remitente='remitente2', 
											texto_pregunta='texto_pregunta2',
											aprobada=True)
		self.respuesta4 = Respuesta.objects.create(pregunta=self.pregunta2, candidato=self.candidato1)
		self.respuesta5 = Respuesta.objects.create(pregunta=self.pregunta2, candidato=self.candidato2)
		self.respuesta6 = Respuesta.objects.create(pregunta=self.pregunta2, candidato=self.candidato3)
		self.respuesta2_c4 = Respuesta.objects.create(pregunta=self.pregunta2, candidato=self.candidato4)

		self.pregunta3 = Pregunta.objects.create(
											remitente='remitente3', 
											texto_pregunta='texto_pregunta3',
											aprobada=True)

		self.respuesta3_1 = Respuesta.objects.create(pregunta=self.pregunta3, candidato=self.candidato1)
		self.respuesta3_2 = Respuesta.objects.create(pregunta=self.pregunta3, candidato=self.candidato2)
		self.respuesta3_3 = Respuesta.objects.create(pregunta=self.pregunta3, candidato=self.candidato3)
		self.respuesta3_4 = Respuesta.objects.create(pregunta=self.pregunta3, candidato=self.candidato4)

		self.pregunta4 = Pregunta.objects.create(
											remitente='remitente4', 
											texto_pregunta='texto_pregunta4')


		self.respuesta4_1 = Respuesta.objects.create(pregunta=self.pregunta4, candidato=self.candidato1)
		self.respuesta4_2 = Respuesta.objects.create(pregunta=self.pregunta4, candidato=self.candidato2)
		self.respuesta4_3 = Respuesta.objects.create(pregunta=self.pregunta4, candidato=self.candidato3)
		self.respuesta4_4 = Respuesta.objects.create(pregunta=self.pregunta4, candidato=self.candidato4)
		#el candidato1 respondiendo

		self.respuesta1.texto_respuesta = u"Yo opino que guau guau"
		self.respuesta1.save()
		self.respuesta4.texto_respuesta = u"GUAAAAAAAAUUUUUUUwra"
		self.respuesta4.save()
		self.respuesta3_1.texto_respuesta = u"yo soy un campeón"
		self.respuesta3_1.save()
		#el candidato2 respondiendo
		self.respuesta5.texto_respuesta = u"miau miau"
		self.respuesta3_2.texto_respuesta = u"asdasdxcvxcvxcvxcv"
		self.respuesta3_2.save()
		self.respuesta5.save()
		#el candidato 4 ha respondido una pregunta
		self.respuesta3_4.texto_respuesta = u"asdasd"
		self.respuesta3_4.save()

		#settings.RANKING_LENGTH = 3
		#el candidato3 es un pajero y no responde niuna cuestion


		




	def test_get_clasificados(self):
		view = Ranking()
		clasificados = view.clasificados()
		self.assertEquals(len(clasificados), 4)


	def test_ranking_tiene_indice_de_premio(self):
		view = Ranking()
		todas_las_preguntas = Respuesta.objects.exclude(texto_respuesta=settings.NO_ANSWER_DEFAULT_MESSAGE).count()
		respuestas_respondidas = Respuesta.objects.count()
		coeficiente_de_premio_esperado = float(respuestas_respondidas)/float(todas_las_preguntas)
		self.assertEquals(view.coeficiente_de_premio, coeficiente_de_premio_esperado)


	def test_los_clasificados_tienen_indice(self):
		view = Ranking()
		clasificados = view.clasificados()

		self.assertTrue("indice" in clasificados[0])
		preg = clasificados[0]["pregunta_count"]
		resp = clasificados[0]["preguntas_respondidas"]
		expected_index = (view.coeficiente_de_premio + 1)*preg*resp - preg*preg
		self.assertEquals(clasificados[0]["indice"], expected_index)

	def test_los_clasificados_no_vienen_ordenaditos_por_indice(self):
		view = Ranking()
		clasificados = view.clasificados()
		self.assertEquals(clasificados[0]['indice'], 24.0)
		self.assertEquals(clasificados[1]['indice'], 13.0)
		self.assertEquals(clasificados[3]['indice'], 2.0)#aquí no están ordenados
		self.assertEquals(clasificados[2]['indice'], -9.0)

	def test_obtiene_ranking_candidatos_que_han_respondido_menos(self):

		view = Ranking()
		clasificados = view.clasificados()
		los_mas_malos = view.malos(clasificados)

		# el orden es :
		# candidato3 -9.0
		# candidato4 2.0
		# candidato2 13.0
		# candidato1 24.0

		self.assertEquals(los_mas_malos[0]["candidato"], self.candidato3)
		self.assertEquals(los_mas_malos[0]["pregunta_count"], 3)
		self.assertEquals(los_mas_malos[0]["preguntas_respondidas"], 0)
		self.assertEquals(los_mas_malos[0]["preguntas_no_respondidas"], 3)

		self.assertEquals(los_mas_malos[1]["candidato"], self.candidato4)
		self.assertEquals(los_mas_malos[1]["pregunta_count"], 3)
		self.assertEquals(los_mas_malos[1]["preguntas_respondidas"], 1)
		self.assertEquals(los_mas_malos[1]["preguntas_no_respondidas"], 2)


		self.assertEquals(los_mas_malos[2]["candidato"], self.candidato2)
		self.assertEquals(los_mas_malos[2]["pregunta_count"], 3)
		self.assertEquals(los_mas_malos[2]["preguntas_respondidas"], 2)
		self.assertEquals(los_mas_malos[2]["preguntas_no_respondidas"], 1)

		self.assertEquals(los_mas_malos[3]["candidato"], self.candidato1)
		self.assertEquals(los_mas_malos[3]["pregunta_count"], 3)
		self.assertEquals(los_mas_malos[3]["preguntas_respondidas"], 3)
		self.assertEquals(los_mas_malos[3]["preguntas_no_respondidas"], 0)


	def test_get_ranking_html(self):
		url = reverse('ranking')
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertTrue('malos' in response.context)
		self.assertTemplateUsed(response, 'elecciones/ranking.html')

		self.assertEquals(len(response.context["malos"]), 4)
		self.assertEquals(response.context["malos"][0]["candidato"], self.candidato3)
		self.assertEquals(response.context["malos"][1]["candidato"], self.candidato4)
		self.assertEquals(response.context["malos"][2]["candidato"], self.candidato2)
		self.assertEquals(response.context["malos"][3]["candidato"], self.candidato1)

		self.assertEquals(len(response.context["buenos"]), 4)
		self.assertEquals(response.context["buenos"][0]["candidato"], self.candidato1)
		self.assertEquals(response.context["buenos"][1]["candidato"], self.candidato2)
		self.assertEquals(response.context["buenos"][2]["candidato"], self.candidato4)



	def test_get_ranking_de_los_buenos(self):
		view = Ranking()
		clasificados = view.clasificados()
		los_mas_buenos = view.buenos(clasificados)

		# el orden es :
		# candidato1 24.0
		# candidato2 13.0
		# candidato4 2.0
		# candidato3 -9.0

		self.assertEquals(len(los_mas_buenos), 4)
		self.assertEquals(los_mas_buenos[0]["candidato"], self.candidato1)
		self.assertEquals(los_mas_buenos[0]["pregunta_count"], 3)
		self.assertEquals(los_mas_buenos[0]["preguntas_respondidas"], 3)
		self.assertEquals(los_mas_buenos[0]["preguntas_no_respondidas"], 0)

		self.assertEquals(los_mas_buenos[1]["candidato"], self.candidato2)
		self.assertEquals(los_mas_buenos[1]["pregunta_count"], 3)
		self.assertEquals(los_mas_buenos[1]["preguntas_respondidas"], 2)
		self.assertEquals(los_mas_buenos[1]["preguntas_no_respondidas"], 1)


		self.assertEquals(los_mas_buenos[2]["candidato"], self.candidato4)
		self.assertEquals(los_mas_buenos[2]["pregunta_count"], 3)
		self.assertEquals(los_mas_buenos[2]["preguntas_respondidas"], 1)
		self.assertEquals(los_mas_buenos[2]["preguntas_no_respondidas"], 2)

		self.assertEquals(los_mas_buenos[3]["candidato"], self.candidato3)


	def test_length_of_buenos_and_malos(self):
		view = Ranking()
		clasificados = view.clasificados()
		previous_length_value = settings.RANKING_LENGTH
		settings.RANKING_LENGTH = 2
		


		los_mas_buenos = view.buenos(clasificados)
		los_mas_malos = view.malos(clasificados)
		self.assertTrue(len(los_mas_buenos) <= settings.RANKING_LENGTH)
		self.assertTrue(len(los_mas_malos) <= settings.RANKING_LENGTH)

		settings.RANKING_LENGTH = previous_length_value


	def test_ranking_as_a_json(self):
		url =  reverse('ranking_json')
		response = self.client.get(url, {'callback': 'callback'})
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response['Content-Type'], "application/json")
		self.assertTrue(response.content.startswith('callback('))
		self.assertTrue(response.content.endswith(');'))


		

		
