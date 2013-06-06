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
from django.template import Template, Context, RequestContext
from urllib2 import quote
from django.contrib.sites.models import Site
from popit.models import ApiInstance as PopitApiInstance, Person

class MolestaAUnCandidato(TestCase):
	def setUp(self):
		colectivo1 = Colectivo.objects.create(sigla='C1', nombre='Colectivo 1')
		self.eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", slug=u"la-eleccion1")
		self.popit_api_instance = PopitApiInstance.objects.create(url='http://popit.org/api/v1')
		self.candidato_con_twitter = Candidato.objects.create(api_instance=self.popit_api_instance,
												eleccion=self.eleccion1,\
												nombre=u"el candidato con twitter",\
												partido=u"API",\
												web=u"http://unaurl.cl",\
												twitter=u"candidato",\
												colectivo=colectivo1)

		self.candidato_sin_twitter = Candidato.objects.create(api_instance=self.popit_api_instance,
												eleccion=self.eleccion1,\
												nombre=u"el candidato sin twitter",\
												partido=u"API",\
												web=u"http://votainteURLligente.cl",\
												colectivo=colectivo1)

		self.pregunta1 = Pregunta.objects.create(
											remitente='remitente1', 
											texto_pregunta='texto_pregunta1')

		self.respuesta1 = Respuesta.objects.create(candidato = self.candidato_con_twitter, pregunta = self.pregunta1)
		self.respuesta2 = Respuesta.objects.create(candidato = self.candidato_sin_twitter, pregunta = self.pregunta1)
	
	def test_molesta_a_un_candidato_sin_twitter_por_su_respuesta_via_twitter(self):
		template = Template("{% load twitter_tags %}{{ respuesta|twittrespuesta }}")
		
		context = Context({"respuesta": self.respuesta2 })
		url_respuesta = self.respuesta2.get_absolute_url()
		expected_html = u""

		self.assertEqual(template.render(context), expected_html)

	def test_molesta_a_un_candidato_con_twitter_por_que_no_ha_respondido(self):
		template = Template("{% load twitter_tags %}{{ respuesta|twittrespuesta }}")
		context = Context({"respuesta": self.respuesta1 })
		template2 = Template("{{ request.get_host }}")
		current_site = Site.objects.get_current()
		answer_url = "http://"+current_site.domain+self.respuesta1.get_absolute_url()
		url_respuesta = template2.render(Context())+answer_url
		
		expected_html = u'<a href="https://twitter.com/intent/tweet?screen_name='+self.respuesta1.candidato.twitter + u'&text=Yo%20tambi%C3%A9n%20quiero%20saber%20tu%20opini%C3%B3n%20sobre%20este%20tema&url=' + answer_url + u'" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Insistí con @'+self.respuesta1.candidato.twitter+u'</a>'
		
		self.assertEqual(template.render(context), expected_html)

	def test_dale_las_gracias_a_un_candidato_que_si_respondio_por_twitter(self):
		template = Template("{% load twitter_tags %}{{ respuesta|twittrespuesta }}")
		context = Context({"respuesta": self.respuesta1 })
		template2 = Template("{{ request.get_host }}")
		current_site = Site.objects.get_current()
		answer_url = "http://"+current_site.domain+self.respuesta1.get_absolute_url()
		url_respuesta = template2.render(Context())+answer_url
		self.respuesta1.texto_respuesta = u"A mi me gustan las papas fritas con harto ketchup"
		
		expected_html = u'<a href="https://twitter.com/intent/tweet?screen_name='+self.respuesta1.candidato.twitter + u'&text=Gracias%20por%20responder&url=' + answer_url + u'" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Seguí la conversación con @'+self.respuesta1.candidato.twitter+u'</a>'
		
		self.assertEqual(template.render(context), expected_html)
