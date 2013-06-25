# -*- coding: utf-8 -*-

from django.test import TestCase
from django.conf import settings
from django.contrib.sites.models import Site
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
from mock import patch



class RespuestaTestCase(TestCase):
	def setUp(self):
		colectivo1 = Colectivo.objects.create(sigla='C1', nombre='Colectivo 1')
		self.popit_api_instance = ApiInstance.objects.create(url='http://popit.org/api/v1')
		self.eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", popit_api_instance=self.popit_api_instance, slug=u"la-eleccion1")
		self.person = Person.objects.create(api_instance =  self.popit_api_instance, name='person_name')
		self.candidato1 = Candidato.objects.create(person=self.person,
												 eleccion=self.eleccion1,\
												 partido=u"API",\
												 web=u"http://votainteURLligente.cl",\
												 twitter=u"candidato",\
												 colectivo=colectivo1)

		self.pregunta1 = Pregunta.objects.create(
											remitente='remitente1', 
											texto_pregunta='texto_pregunta1')


	def test_create_respuesta(self):
		respuesta, created = Respuesta.objects.get_or_create(candidato = self.candidato1, pregunta = self.pregunta1)

		self.assertTrue(created)
		self.assertEquals(respuesta.candidato, self.candidato1)
		self.assertEquals(respuesta.pregunta, self.pregunta1)
		self.assertEquals(respuesta.texto_respuesta, settings.NO_ANSWER_DEFAULT_MESSAGE)

	def test_get_absolute_url(self):
		respuesta, created = Respuesta.objects.get_or_create(candidato = self.candidato1, pregunta = self.pregunta1)

		url = respuesta.get_absolute_url()
		self.assertTrue(url)
		url_respuesta = reverse('eleccion-respuesta', kwargs={'pk':respuesta.id})
		self.assertTrue(url_respuesta)
		self.assertEquals(url, url_respuesta)

	def test_get_to_respuesta_object_html(self):
		#no se me ocurre otro nombre para este test
		respuesta, created = Respuesta.objects.get_or_create(candidato = self.candidato1, pregunta = self.pregunta1)

		url_respuesta = respuesta.get_absolute_url()

		response = self.client.get(url_respuesta)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('respuesta' in response.context)
		self.assertEquals(response.context["respuesta"], respuesta)

	def test_is_not_answered(self):
		respuesta = Respuesta.objects.create(candidato = self.candidato1, pregunta = self.pregunta1)

		self.assertFalse(respuesta.is_answered())

	def test_is_answered(self):
		respuesta = Respuesta.objects.create(candidato = self.candidato1, pregunta = self.pregunta1)
		respuesta.texto_respuesta = u"Una respuesta maravillosa del candidato"
		self.assertTrue(respuesta.is_answered())


	def test_is_not_answered_with_spaces(self):
		respuesta = Respuesta.objects.create(candidato = self.candidato1, pregunta = self.pregunta1)
		respuesta.texto_respuesta = settings.NO_ANSWER_DEFAULT_MESSAGE+ "                          "#Many spaces at the end

		self.assertFalse(respuesta.is_answered())



class AnswerNotificationTestCase(TestCase):
	def setUp(self):
		colectivo1 = Colectivo.objects.create(sigla='C1', nombre='Colectivo 1')
		self.popit_api_instance = ApiInstance.objects.create(url='http://popit.org/api/v1')
		self.eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", popit_api_instance=self.popit_api_instance, slug=u"la-eleccion1")
		self.person = Person.objects.create(api_instance =  self.popit_api_instance, name='person_name')
		self.candidato1 = Candidato.objects.create(person=self.person,
																		eleccion=self.eleccion1,\
																		partido=u"API",\
																		web=u"http://votainteURLligente.cl",\
																		twitter=u"candidato",\
																		colectivo=colectivo1)

		self.pregunta1 = Pregunta.objects.create(remitente='remitente1', 
                                               texto_pregunta='texto_pregunta1',
                                               email_sender="remitente1@votainteligente.cl")

		self.respuesta1 = Respuesta.objects.create(candidato = self.candidato1, pregunta = self.pregunta1)

		self.pregunta2 = Pregunta.objects.create(
                                                                               remitente='remitente2', 
                                                                               texto_pregunta='texto_pregunta2')
		self.respuesta2 = Respuesta.objects.create(candidato = self.candidato1, pregunta = self.pregunta2)
	def test_notify_when_answer_arrive(self):
		self.respuesta1.texto_respuesta = u"Con Respuesta"
		self.respuesta1.save()
		candidato_responde = self.respuesta1.candidato
		domain_url = Site.objects.get_current().domain
		self.assertEquals(len(mail.outbox), 1)
		self.assertEquals(mail.outbox[0].subject,  candidato_responde.nombre + u' ha respondido a tu pregunta.')
		message = self.respuesta1.pregunta.remitente + u',\rla respuesta la puedes encontrar aquí:\rhttp://' + domain_url + self.respuesta1.get_absolute_url() + u'\r ¡Saludos!'
		self.assertEquals(mail.outbox[0].body, message)
		self.assertEquals(mail.outbox[0].from_email, settings.INFO_CONTACT_MAIL)
		self.assertTrue(mail.outbox[0].to.index(self.pregunta1.email_sender) > -1)

	def test_dont_notify_in_creation(self):
		self.respuesta1.texto_respuesta = settings.NO_ANSWER_DEFAULT_MESSAGE
		self.respuesta1.save()
		self.assertEquals(len(mail.outbox), 0)

	def test_dont_notify_lacking_email_sender(self):
		self.respuesta2.texto_respuesta = u"Con Respuesta"
		self.respuesta2.save()
		self.assertEquals(len(mail.outbox), 0)

	def test_it_handles_errors(self):
		respuesta2 = Respuesta.objects.create(candidato = self.candidato1, pregunta = self.pregunta1)
		with patch('django.core.mail.send_mail')  as send_mail:
			send_mail.side_effect = Exception()
			try:
				respuesta2.texto_respuesta = u"Con Respuesta"
				respuesta2.save()
			except:
				self.fail("Exception")

 
