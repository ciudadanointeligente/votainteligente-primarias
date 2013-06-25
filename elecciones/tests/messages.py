# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from elecciones.models import Eleccion, Area, Indice, Dato, Candidato, Pregunta, Respuesta, Contacto, Colectivo, preguntas_por_partido
from elecciones.management.commands.elecciones_importer import *
from elecciones.management.commands.contactos_importer import *
from elecciones.management.commands.candidatos_importer import *
from mailer.models import Message
from django.conf import settings
from django.test.client import Client
from django.utils.unittest import skip
from django.template import Template, Context
from urllib2 import quote
from django.contrib import messages
import os
from popit.models import Person, ApiInstance
from writeit.models import WriteItApiInstance, WriteItInstance, Message as WriteItMessage
from mock import patch

class MessageTestCase(TestCase):

#Load candidate mailing data
#Create mail template
#Create question mail
#Send question mail
#Save question mail in db
#Retrieve question mail from db
#Obtain answer mail
#Save answer mail in db
#Retrieve answer mail from db
#Associate quesion and answer mails
#Obtain questions/answers for a given candidate
#Calculate response stats


	def setUp(self):
		self.write_it_api_instance = WriteItApiInstance.objects.create(url="http://witeit.ciudadanointeligente.org/api/v1")
		self.write_it_instance1 = WriteItInstance.objects.create(api_instance = self.write_it_api_instance, name="new_instance")
		self.write_it_instance2 = WriteItInstance.objects.create(api_instance = self.write_it_api_instance, name="new_instance")
		self.write_it_instance3 = WriteItInstance.objects.create(api_instance = self.write_it_api_instance, name="new_instance")
		self.popit_api_instance1 = ApiInstance.objects.create(url='http://popit.org/api/v1')
		self.popit_api_instance2 = ApiInstance.objects.create(url='http://popit.org/api/v2')
		self.popit_api_instance3 = ApiInstance.objects.create(url='http://popit.org/api/v3')
		self.eleccion1, created = Eleccion.objects.get_or_create(nombre="eleccion1", 
			popit_api_instance=self.popit_api_instance1,
			write_it_instance=self.write_it_instance1,
			slug="la-eleccion1",
			main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
			messaging_extra_app_url="http://napistejim.cz/address=nachod",
			mapping_extra_app_url="http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		self.eleccion2, created = Eleccion.objects.get_or_create(nombre="eleccion2", 
			popit_api_instance=self.popit_api_instance2,
			write_it_instance=self.write_it_instance2,
			slug="la-eleccion2",
			main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
			messaging_extra_app_url="http://napistejim.cz/address=nachod",
			mapping_extra_app_url="http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		self.eleccion3, created = Eleccion.objects.get_or_create(nombre="eleccion3", 
			popit_api_instance=self.popit_api_instance3,
			write_it_instance=self.write_it_instance3,
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
		self.person1 = Person.objects.create(api_instance =  self.popit_api_instance1, name=self.data_candidato[0]['nombre'])
		self.person2 = Person.objects.create(api_instance =  self.popit_api_instance1, name=self.data_candidato[1]['nombre'])
		self.person3 = Person.objects.create(api_instance =  self.popit_api_instance1, name=self.data_candidato[2]['nombre'])
		self.candidato1 = Candidato.objects.create(person=self.person1, eleccion = self.eleccion1, colectivo = self.data_candidato[0]['partido'], web = self.data_candidato[0]['web'])
		self.candidato2 = Candidato.objects.create(person=self.person2, eleccion = self.eleccion1, colectivo = self.data_candidato[1]['partido'])
		self.candidato3 = Candidato.objects.create(person=self.person3, eleccion = self.eleccion2, colectivo = self.data_candidato[2]['partido'])
		self.question1 = "Why can't we be friends?"
		self.answer1 = "I'd kinda like to be the President, so I can show you how your money's spent"
		self.question2 = 'Who let the dogs out?'
		self.answer2 = 'woof, woof, woof, woof'
		self.template = '<h3>Hello, this is a test template</h3><br><p>Message goes here</p>'
		self.mail_user = 'mailer@'
		self.mail_pass = ''
		settings.PREGUNTALE_STATUS = 'GOING_ON'
		os.environ['RECAPTCHA_TESTING'] = 'True'

	def tearDown(self):
		os.environ['RECAPTCHA_TESTING'] = 'False'


	def test_create_candidate(self):

		self.assertTrue(self.candidato1)
		self.assertEquals(self.candidato1.nombre, 'candidato1')
		self.assertEquals(self.candidato1.eleccion, self.eleccion1)
		self.assertEquals(self.candidato1.colectivo.sigla, 'C1')
		self.assertEquals(self.candidato1.web, 'web1')
	
	def test_create_contacto(self):
		contacto, created = Contacto.objects.get_or_create(tipo = 1, valor = 'test@test.com', candidato = self.candidato1)
		self.assertTrue(created)
		self.assertEquals(contacto.tipo, 1)
		self.assertEquals(contacto.valor, 'test@test.com')
		self.assertEquals(contacto.candidato, self.candidato1)
		self.assertTrue(contacto)

	def test_create_question_message_without_sender(self):
		#Se crea la pregunta y las respuestas asociadas
		pregunta = Pregunta.objects.create(
											remitente='remitente1', 
											texto_pregunta='texto_pregunta1')
		Respuesta.objects.create(pregunta=pregunta, candidato=self.candidato1)
		Respuesta.objects.create(pregunta=pregunta, candidato=self.candidato2)
		#Se crea la pregunta con su respectivo texto y remitente?
		self.assertTrue(pregunta)
		self.assertEquals(pregunta.aprobada,False)
		self.assertEquals(pregunta.texto_pregunta,'texto_pregunta1')
		self.assertEquals(pregunta.remitente,'remitente1')
		#Se crearon las respuestas asociadas a la pregunta?
		respuesta_no_contestada1 = Respuesta.objects.filter(candidato=self.candidato1).filter(pregunta=pregunta)[0]
		respuesta_no_contestada2 = Respuesta.objects.filter(candidato=self.candidato2).filter(pregunta=pregunta)[0]
		#Se crean las respuestas, y se guardan en la bd con los valores iniciales que corresponden?
		self.assertEquals(respuesta_no_contestada1.texto_respuesta, settings.NO_ANSWER_DEFAULT_MESSAGE)
		self.assertEquals(respuesta_no_contestada2.texto_respuesta, settings.NO_ANSWER_DEFAULT_MESSAGE)
		#Existe la asociación entre preguntas y candidatos?
		self.assertEquals(Candidato.objects.filter(pregunta=pregunta).filter(person__name=self.candidato1.person.name).count(),1)
		self.assertEquals(Candidato.objects.filter(pregunta=pregunta).filter(person__name=self.candidato2.person.name).count(),1)
		#Sólo se agregó la pregunta a 2 candidatos?
		self.assertEquals(Candidato.objects.filter(pregunta=pregunta).count(),2)


	def test_create_question_message_without_sender(self):
		#Se crea la pregunta y las respuestas asociadas
		pregunta = Pregunta.objects.create(remitente='remitente1', 
											texto_pregunta='texto_pregunta1',
											email_sender='mail@mail.er')
		self.assertTrue(pregunta)
		self.assertEquals(pregunta.email_sender,'mail@mail.er')


	def test_pregunta_get_absolute_url(self):
		pregunta = Pregunta.objects.create(remitente='remitente1', 
											texto_pregunta='texto_pregunta1',
											email_sender='mail@mail.er')

		expected_url = reverse('pregunta-detalle', kwargs={'pk':pregunta.id})

		self.assertTrue(expected_url)

		actual_url = pregunta.get_absolute_url()

		self.assertTrue(actual_url, expected_url)


	def test_detalle_pregunta(self):
		pregunta = Pregunta.objects.create(remitente='remitente1', 
											texto_pregunta='texto_pregunta1',
											email_sender='mail@mail.er')
		url = reverse('pregunta-detalle', kwargs={'pk':pregunta.id})
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)#pagina bacán
		self.assertTrue('pregunta' in response.context)#viene la pregunta
		self.assertEquals(response.context['pregunta'], pregunta)


		

	def test_create_answer_message(self):
		#Se crea la pregunta y las respuestas asociadas
		pregunta1 = Pregunta.objects.create(texto_pregunta='texto_pregunta1', remitente='remitente1')
		Respuesta.objects.create(pregunta=pregunta1, candidato=self.candidato1)
		Respuesta.objects.create(pregunta=pregunta1, candidato=self.candidato2)
		pregunta2 = Pregunta.objects.create(texto_pregunta='texto_pregunta2', remitente='remitente2')
		Respuesta.objects.create(pregunta=pregunta2, candidato=self.candidato1)
		Respuesta.objects.create(pregunta=pregunta2, candidato=self.candidato2)
		#Se cambia la respuesta por defecto a la respuesta obtenida?
		respuesta_candidato1_pregunta1 = Respuesta.objects.filter(candidato=self.candidato1).filter(pregunta=pregunta1)[0]
		respuesta_candidato1_pregunta1.texto_respuesta ='texto_candidato1_respuesta1'
		respuesta_candidato1_pregunta1.save()
		respuesta_candidato1_pregunta1_db = Respuesta.objects.filter(candidato=self.candidato1).filter(pregunta=pregunta1)[0]
		self.assertEquals(respuesta_candidato1_pregunta1_db.texto_respuesta,'texto_candidato1_respuesta1')
		#Se cambian accidentalmente otras respuestas?
		respuesta_candidato1_pregunta2 = Respuesta.objects.filter(candidato=self.candidato1).filter(pregunta=pregunta2)[0]
		self.assertEquals(respuesta_candidato1_pregunta2.texto_respuesta, settings.NO_ANSWER_DEFAULT_MESSAGE)
	
	def test_mail_sending(self):

		# Send message.
		mail.send_mail('Subject here', 'Here is the message.','from@example.com', ['to@example.com'],
		    fail_silently=False)

		# Test that one message has been sent.
		self.assertEqual(len(mail.outbox), 1)

		# Verify that the subject of the first message is correct.
		self.assertEqual(mail.outbox[0].subject, 'Subject here')
		#chequear que el mail llega y lo podemos traer


	def test_get_question_page(self):
		url = reverse('eleccion-preguntales', kwargs={'slug':self.eleccion1.slug})
		response = self.client.post(url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'elecciones/preguntales.html')
		self.assertTrue('form' in response.context)
		choices = response.context['form'].fields['candidato'].choices
		self.assertTrue((self.candidato1.pk, self.candidato1.nombre) in choices)
		self.assertTrue((self.candidato2.pk, self.candidato2.nombre) in choices)
		self.assertTrue((self.candidato3.pk, self.candidato3.nombre) not in choices)





	def test_submit_question_message(self):

		
		#hackeamos .virtualenvs/mun12/lib/python2.7/site-packages/captcha/fields.py porque no consideraba settings.debug como true.
		#Post data
		url = reverse('eleccion-preguntales', kwargs={'slug':self.eleccion1.slug})
		response = self.client.post(url, {'candidato': [self.candidato1.pk, self.candidato2.pk],
											'texto_pregunta': 'Texto Pregunta', 
											'remitente': 'Remitente 1',
											'recaptcha_response_field': 'PASSED'}, follow=True)



		self.assertTemplateUsed(response, 'elecciones/preguntales.html')
		self.assertEquals(Pregunta.objects.count(), 1)
		self.assertEquals(Pregunta.objects.all()[0].texto_pregunta, 'Texto Pregunta')
		self.assertEquals(Pregunta.objects.all()[0].remitente, 'Remitente 1')

		self.assertEquals(Respuesta.objects.count(), 2)
		self.assertTrue('elecciones' in response.context)


		#Se crea la pregunta con su respectivo texto y remitente
		pregunta_enviada = Pregunta.objects.filter(candidato=self.candidato1).filter(remitente='Remitente 1')[0]
		self.assertTrue(pregunta_enviada)
		self.assertEquals(pregunta_enviada.texto_pregunta,'Texto Pregunta')
		self.assertEquals(pregunta_enviada.remitente,'Remitente 1')
		#Se crean las respuestas, y se guardan en la bd con los valores iniciales que corresponden
		respuesta_no_contestada1 = Respuesta.objects.filter(candidato=self.candidato1).filter(pregunta=pregunta_enviada)[0]
		respuesta_no_contestada2 = Respuesta.objects.filter(candidato=self.candidato2).filter(pregunta=pregunta_enviada)[0]
		self.assertEquals(respuesta_no_contestada1.texto_respuesta, settings.NO_ANSWER_DEFAULT_MESSAGE)
		self.assertEquals(respuesta_no_contestada2.texto_respuesta, settings.NO_ANSWER_DEFAULT_MESSAGE)
		#Existe la asociación entre preguntas y candidatos
		self.assertEquals(Candidato.objects.filter(pregunta=pregunta_enviada).filter(person__name=self.candidato1.person.name).count(),1)
		self.assertEquals(Candidato.objects.filter(pregunta=pregunta_enviada).filter(person__name=self.candidato2.person.name).count(),1)
		#Sólo se agregó la pregunta a 2 candidatos
		self.assertEquals(Candidato.objects.filter(pregunta=pregunta_enviada).count(),2)

		#

		

		#Viene un mensaje de alerta
		self.assertEquals(len(response.context['messages']),1)

		# self.assertTrue(len(storage), 1)

		# for message in storage:
		# 	print message
		# self.assertTrue("alerta" in response.context)
		# self.assertEquals(response.context["alerta"], "***\nTu pregunta ya está siendo procesada. En algunos minutos estará publicada.\n***")



	
	def test_send_question_message(self):

		
		#hackeamos .virtualenvs/mun12/lib/python2.7/site-packages/captcha/fields.py porque no consideraba settings.debug como true.
		#Post data
		settings.DEFAULT_FROM_EMAIL = 'otromail@votainteligente.org'
		contacto1, created = Contacto.objects.get_or_create(tipo = 1, valor = 'candidato1@candidato1.com', candidato = self.candidato1)
		contacto2, created = Contacto.objects.get_or_create(tipo = 1, valor = 'candidato2@candidato2.com', candidato = self.candidato2)
		url = reverse('eleccion-preguntales', kwargs={'slug':self.eleccion1.slug})
		response = self.client.post(url, {'candidato': [self.candidato1.pk, self.candidato2.pk],
											'texto_pregunta': 'Texto Pregunta', 
											'remitente': 'Remitente 1',
											'recaptcha_response_field': 'PASSED'})


		pregunta_nueva = Pregunta.objects.get(remitente='Remitente 1')

		with patch('writeit.models.Message.push_to_the_api') as push:
			push.return_value = "patito"
			
			pregunta_nueva.enviar()
		# Test that two messages are waiting to be sent.
		self.assertEquals(Message.objects.count(), 2)

		# Verify that the subject of the first message is correct.
		primera_pregunta = Message.objects.all()[0]
		segunda_pregunta = Message.objects.all()[1]
		
		self.assertEquals(primera_pregunta.from_address, settings.DEFAULT_FROM_EMAIL)
		self.assertEquals(segunda_pregunta.from_address, settings.DEFAULT_FROM_EMAIL)
		self.assertTrue(primera_pregunta.subject.startswith(u'Un ciudadano está interesado en más información sobre tu candidatura'))
		self.assertTrue(segunda_pregunta.subject.startswith(u'Un ciudadano está interesado en más información sobre tu candidatura'))
		# self.assertEqual(mail.outbox[0].from, 'municiaples2012@votainteURLligente.cl')
		# self.assertEqual(mail.outbox[1].from, 'municiaples2012@votainteURLligente.cl')
		#chequear que el mail llega y lo podemos traer


	def test_display_conversations(self):
		
		url = reverse('eleccion-preguntales', kwargs={'slug':self.eleccion1.slug})
		response = self.client.get(url)
		
		pregunta1 = Pregunta.objects.create(texto_pregunta='texto_pregunta1', remitente='remitente1')
		respuesta1 = Respuesta.objects.create(pregunta=pregunta1, candidato=self.candidato1)
		respuesta2 = Respuesta.objects.create(pregunta=pregunta1, candidato=self.candidato2)

		self.assertEquals(response.status_code, 200)
		#Check conversaciones
		self.assertFalse('conversaciones' in response.context)

		self.assertTrue('preguntas' in response.context)
		self.assertEquals(response.context['preguntas'].count(),0)


		#Conversaciones aren't displayed if not allowed
		#self.assertEquals(response.context['conversaciones'], {})
		#Conversaciones are displayed if allowed
		pregunta = Pregunta.objects.filter(candidato=self.candidato1).filter(remitente='remitente1')[0]
		pregunta.aprobada = True
		pregunta.save()
		response = self.client.get(url)
		#conversaciones = response.context['conversaciones']
		#Creo que no es necesario hacer esto;Se puede acceder a todas las variables de una Pregunta en el template
		#expected_conversaciones = {u"remitente1":{u"texto_pregunta1":{u"candidato1":respuesta1,u"candidato2":respuesta2}}}
		self.assertEquals(response.context['preguntas'].count(),1)
		self.assertEquals(response.context['preguntas'][0],pregunta1)
		#self.assertEquals(conversaciones, expected_conversaciones)
		#nombre_remitente, pregunta = conversaciones.popitem()
		# texto_pregunta, respuestas = pregunta.popitem()
		# candidato, texto_respuesta = respuestas.popitem()
		# self.assertTrue(nombre_remitente)
		# self.assertTrue(texto_pregunta)
		# self.assertTrue(candidato)
		# self.assertTrue(texto_respuesta)
	
	def test_questions_by_eleccion_count(self):
		pregunta1 = Pregunta.objects.create(texto_pregunta='texto_pregunta1', remitente='remitente1',aprobada=True)
		pregunta2 = Pregunta.objects.create(texto_pregunta='texto_pregunta2', remitente='remitente2',aprobada=True)
		pregunta3 = Pregunta.objects.create(texto_pregunta='texto_pregunta3', remitente='remitente3',aprobada=True)
		Respuesta.objects.create(pregunta=pregunta1, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p1c2', pregunta=pregunta1, candidato=self.candidato2)
		Respuesta.objects.create(pregunta=pregunta2, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta 2', pregunta=pregunta3, candidato=self.candidato3)

		self.assertEqual(self.eleccion1.numero_preguntas(), 2)
		self.assertEqual(self.eleccion2.numero_preguntas(), 1)
		self.assertEqual(self.eleccion3.numero_preguntas(), 0)
	
	def test_answers_by_eleccion_count(self):
		pregunta1 = Pregunta.objects.create(texto_pregunta='texto_pregunta1', remitente='remitente1',aprobada=True)
		pregunta2 = Pregunta.objects.create(texto_pregunta='texto_pregunta2', remitente='remitente2',aprobada=True)
		pregunta3 = Pregunta.objects.create(texto_pregunta='texto_pregunta3', remitente='remitente3',aprobada=True)
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p1c1', pregunta=pregunta1, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p1c2', pregunta=pregunta1, candidato=self.candidato2)
		r2 = Respuesta.objects.create(pregunta=pregunta2, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p3c3', pregunta=pregunta3, candidato=self.candidato3)
		self.assertEqual(self.eleccion1.numero_respuestas(), 2)
		self.assertEqual(self.eleccion2.numero_respuestas(), 1)
		self.assertEqual(self.eleccion3.numero_respuestas(), 0)

	def test_candidate_questions(self):
		pregunta1 = Pregunta.objects.create(texto_pregunta='texto_pregunta1', remitente='remitente1',aprobada=True)
		pregunta2 = Pregunta.objects.create(texto_pregunta='texto_pregunta2', remitente='remitente2',aprobada=True)
		pregunta3 = Pregunta.objects.create(texto_pregunta='texto_pregunta3', remitente='remitente3',aprobada=True)
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p1c1', pregunta=pregunta1, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p1c2', pregunta=pregunta1, candidato=self.candidato2)
		r2= Respuesta.objects.create(pregunta=pregunta2, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p3c3', pregunta=pregunta3, candidato=self.candidato3)
		
		self.assertEqual(self.candidato1.numero_preguntas(), 2)
		self.assertEqual(self.candidato2.numero_preguntas(), 1)
		self.assertEqual(self.candidato3.numero_preguntas(), 1)


	
	def test_candidate_answers(self):
		pregunta1 = Pregunta.objects.create(texto_pregunta='texto_pregunta1', remitente='remitente1',aprobada=True)
		pregunta2 = Pregunta.objects.create(texto_pregunta='texto_pregunta2', remitente='remitente2',aprobada=True)
		pregunta3 = Pregunta.objects.create(texto_pregunta='texto_pregunta3', remitente='remitente3',aprobada=True)
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p1c1', pregunta=pregunta1, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p1c2', pregunta=pregunta1, candidato=self.candidato2)
		Respuesta.objects.create( pregunta=pregunta2, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p3c3', pregunta=pregunta3, candidato=self.candidato3)

		self.assertEqual(self.candidato1.numero_respuestas(), 1)
		self.assertEqual(self.candidato2.numero_respuestas(), 1)
		self.assertEqual(self.candidato3.numero_respuestas(), 1)

	@skip("No construido aún")
	def test_preguntas_por_partido(self):
		pregunta1 = Pregunta.objects.create(texto_pregunta='texto_pregunta1', remitente='remitente1')
		pregunta2 = Pregunta.objects.create(texto_pregunta='texto_pregunta2', remitente='remitente2')
		pregunta3 = Pregunta.objects.create(texto_pregunta='texto_pregunta3', remitente='remitente3')
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p1c1', pregunta=pregunta1, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p1c2', pregunta=pregunta1, candidato=self.candidato2)
		Respuesta.objects.create(pregunta=pregunta2, candidato=self.candidato1)
		preguntas_partido_1 = self.colectivo1.preguntas
		preguntas_partido_2 = self.colectivo2.preguntas
		preguntas_partido_3 = self.colectivo3.preguntas


		self.assertEqual(preguntas_partido_1.count(), 2)
		self.assertEqual(preguntas_partido_2.count(), 1)
		self.assertEqual(preguntas_partido_3.count(), 0)


	@skip("No construido aún")
	def test_party_questions(self):
		pregunta1 = Pregunta.objects.create(texto_pregunta='texto_pregunta1', remitente='remitente1')
		pregunta2 = Pregunta.objects.create(texto_pregunta='texto_pregunta2', remitente='remitente2')
		pregunta3 = Pregunta.objects.create(texto_pregunta='texto_pregunta3', remitente='remitente3')
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p1c1', pregunta=pregunta1, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p1c2', pregunta=pregunta1, candidato=self.candidato2)
		Respuesta.objects.create(pregunta=pregunta2, candidato=self.candidato1)
		# Respuesta.objects.create(texto_respuesta = 'Texto Respuesta p3c3', pregunta=pregunta3, candidato=self.candidato3)



		self.assertEqual(preguntas_por_partidos[0][0], 2)
		self.assertEqual(preguntas_por_partidos[0][1], 'partido1')
		self.assertEqual(preguntas_por_partidos[1][0], 1)
		self.assertEqual(preguntas_por_partidos[1][1], 'partido2')
		self.assertEqual(preguntas_por_partidos[2][0], 0)
		self.assertEqual(preguntas_por_partidos[2][1], 'partido3')

	def test_preguntales_html_going_on(self):
		# decir que esta en modo GOING ON (otros estados: COMING SOON, PASSED)
		# acceder al Preguntales de la eleccion 1
		# asegurarme que lo rendereado es preguntales_html
		settings.PREGUNTALE_STATUS = "GOING_ON"
		url = reverse('eleccion-preguntales', kwargs={'slug':self.eleccion1.slug})
		response = self.client.get(url)
		self.assertTemplateUsed(response, 'elecciones/preguntales.html')

	def test_preguntales_html_coming_soon(self):
		settings.PREGUNTALE_STATUS = "COMING_SOON"
		url = reverse('eleccion-preguntales', kwargs={'slug':self.eleccion1.slug})
		response = self.client.get(url)
		self.assertTemplateUsed(response, 'elecciones/preguntales_coming_soon.html')

	def test_preguntales_html_passed(self):
		settings.PREGUNTALE_STATUS = "PASSED"
		url = reverse('eleccion-preguntales', kwargs={'slug':self.eleccion1.slug})
		response = self.client.get(url)
		self.assertTemplateUsed(response, 'elecciones/preguntales_passed.html')

	def test_create_write_it_message(self):
		#hackeamos .virtualenvs/mun12/lib/python2.7/site-packages/captcha/fields.py porque no consideraba settings.debug como true.
		#Post data
		settings.DEFAULT_FROM_EMAIL = 'otromail@votainteligente.org'
		settings.DEFAULT_WRITEIT_SUBJECT = u'Un ciudadano está interesado en más información sobre tu candidatura'
		url = reverse('eleccion-preguntales', kwargs={'slug':self.eleccion1.slug})
		response = self.client.post(url, {'candidato': [self.candidato1.pk, self.candidato2.pk],
											'texto_pregunta': 'Texto Pregunta', 
											'remitente': 'Remitente 1',
											'recaptcha_response_field': 'PASSED'})


		pregunta_nueva = Pregunta.objects.get(remitente='Remitente 1')

		with patch('writeit.models.Message.push_to_the_api') as push:
			push.return_value = "patito"
			
			pregunta_nueva.enviar()

		# Test that two messages are waiting to be sent.

		self.assertEquals(WriteItMessage.objects.count(), 1)

		# Verify that the subject of the first message is correct.
		primera_pregunta = WriteItMessage.objects.all()[0]

		self.assertEquals(primera_pregunta.author_email, settings.DEFAULT_FROM_EMAIL)
		self.assertEquals(primera_pregunta.author_name, pregunta_nueva.remitente)
		self.assertEquals(primera_pregunta.subject, settings.DEFAULT_WRITEIT_SUBJECT + u" [ID=#" + str(pregunta_nueva.id) + "]" )
		self.assertEquals(primera_pregunta.content, 'Texto Pregunta')
		self.assertEquals(primera_pregunta.writeitinstance, self.write_it_instance1)
		self.assertEquals(primera_pregunta.people.count(), 2)

	
	def test_it_posts_the_message_to_the_api(self):
		settings.DEFAULT_FROM_EMAIL = 'otromail@votainteligente.org'
		settings.DEFAULT_WRITEIT_SUBJECT = u'Un ciudadano está interesado en más información sobre tu candidatura'
		url = reverse('eleccion-preguntales', kwargs={'slug':self.eleccion1.slug})
		response = self.client.post(url, {'candidato': [self.candidato1.pk, self.candidato2.pk],
											'texto_pregunta': 'Texto Pregunta', 
											'remitente': 'Remitente 1',
											'recaptcha_response_field': 'PASSED'})


		pregunta_nueva = Pregunta.objects.get(remitente='Remitente 1')
		with patch('writeit.models.Message.push_to_the_api') as push:
			push.return_value = "patito"
			
			pregunta_nueva.enviar()

			push.assert_called_with()


	def test_it_handles_errors_when_sending_to_the_api(self):
		settings.DEFAULT_FROM_EMAIL = 'otromail@votainteligente.org'
		settings.DEFAULT_WRITEIT_SUBJECT = u'Un ciudadano está interesado en más información sobre tu candidatura'
		url = reverse('eleccion-preguntales', kwargs={'slug':self.eleccion1.slug})
		

		response = self.client.post(url, {'candidato': [self.candidato1.pk, self.candidato2.pk],
											'texto_pregunta': 'Texto Pregunta', 
											'remitente': 'Remitente 1',
											'recaptcha_response_field': 'PASSED'})
		

		with patch('writeit.models.Message.push_to_the_api') as push:
			contacto, created = Contacto.objects.get_or_create(tipo = 1, valor = 'test@test.com', candidato = self.candidato1)
			pregunta_nueva = Pregunta.objects.get(remitente='Remitente 1')
			push.side_effect = Exception()
			try:
				pregunta_nueva.enviar()
			except:
				self.fail('No está manejando errores en la API')





