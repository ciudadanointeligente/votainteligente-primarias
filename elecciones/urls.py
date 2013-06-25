from django.conf.urls import patterns, include, url
from views import HomeTemplateView, EleccionOverview, EleccionIndices, MetodologiaView, QuienesSomosView, ComparadorView, EleccionPreguntales, ReportaView,\
QuePuedoHacerHacerView, NosFaltanDatosView, Ranking, RankingJson, EleccionExtraInfo, EnlacesView, VoluntariosView, SenadoresView, InteresesView,\
RespuestaDetail
from django.views.generic import TemplateView, DetailView
from django.views.decorators.cache import cache_page
from models import Respuesta
from django.conf import settings 

urlpatterns = patterns('',
	url(r'^$', HomeTemplateView.as_view(template_name="home.html"), name="home"),
	

	#static pages
	url(r'^metodologia/?$', MetodologiaView.as_view(), name="metodologia"),
	url(r'^somos/?$', QuienesSomosView.as_view(), name="somos"),
	url(r'^enlaces/?$', EnlacesView.as_view(), name="enlaces"),
	url(r'^voluntarios/?$', VoluntariosView.as_view(), name="voluntarios"),
	url(r'^senadores/?$', SenadoresView.as_view(), name="senadores"),
	url(r'^fiscaliza/?$', ReportaView.as_view(), name="reporta"),
	url(r'^que_puedo_hacer/?$', QuePuedoHacerHacerView.as_view(), name="que_puedo_hacer"),
	url(r'^nos_faltan_datos/?$', NosFaltanDatosView.as_view(), name="nos_faltan_datos"),
	url(r'^todos/?$', TemplateView.as_view(template_name="todos_los_candidatos.html"), name="todos"),
	url(r'^ranking/?$', cache_page(Ranking.as_view(template_name = "elecciones/ranking.html"), 60 * settings.CACHE_MINUTES), name="ranking"),
	url(r'^ranking\.json$', cache_page(RankingJson.as_view(), 60 * settings.CACHE_MINUTES), name="ranking_json"),
	url(r'^mas_info/?$', TemplateView.as_view(template_name='elecciones/mas_info.html'), name="mas_info"),
	url(r'^queremos/?$', TemplateView.as_view(template_name='elecciones/queremos.html'), name="queremos"),
	url(r'^comparador/?$', TemplateView.as_view(template_name='elecciones/comparador.html'), name="comparador"),
	url(r'^intereses/?$', InteresesView.as_view(), name='intereses'),



 	url(r'^contact/', include('django_contactme.urls'))	,
 	url(r'^respuesta/(?P<pk>\d+)/?$', RespuestaDetail.as_view(), name="eleccion-respuesta"),

	#pages depending on the eleccion
	url(r'^(?P<slug>[-\w]+)/indices/?$', EleccionIndices.as_view(), name='eleccion-index-detail'),
	url(r'^(?P<slug>[-\w]+)/mas-info/?$', EleccionExtraInfo.as_view(), name='eleccion-extra-info'),
	url(r'^(?P<slug>[-\w]+)/?$', EleccionOverview.as_view(), name="eleccion-overview"),
	url(r'^(?P<slug>[-\w]+)/preguntales/?$', EleccionPreguntales.as_view(), name="eleccion-preguntales"),
	
	)
