from django.conf.urls import patterns, include, url
from views import HomeTemplateView, EleccionOverview, EleccionIndices, MetodologiaView, QuienesSomosView, EleccionPreguntales, ReportaView,\
QuePuedoHacerHacerView, NosFaltanDatosView, Ranking, EleccionExtraInfo, EnlacesView, VoluntariosView, SenadoresView
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
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
	url(r'^ranking/?$', cache_page(Ranking.as_view(), 60 * settings.CACHE_MINUTES), name="ranking"),

 	url(r'^contact/', include('django_contactme.urls'))	,

	#pages depending on the eleccion
	url(r'^(?P<slug>[-\w]+)/indices/?$', EleccionIndices.as_view(), name='eleccion-index-detail'),
	url(r'^(?P<slug>[-\w]+)/mas-info/?$', EleccionExtraInfo.as_view(), name='eleccion-extra-info'),
	url(r'^(?P<slug>[-\w]+)/?$', EleccionOverview.as_view(), name="eleccion-overview"),
	url(r'^(?P<slug>[-\w]+)/preguntales/?$', EleccionPreguntales.as_view(), name="eleccion-preguntales"),
	
	)
