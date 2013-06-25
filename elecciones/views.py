# -*- coding: utf-8 -*-#
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.views.generic.edit import FormView
from models import Eleccion, Indice, Pregunta, Candidato, Respuesta, Contacto
from django.shortcuts import get_object_or_404
from forms import PreguntaForm
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from operator import itemgetter
from django.db.models import Count
from django.utils import simplejson as json

class HomeTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        elecciones_buscables = Eleccion.objects.filter(searchable=True)
        elecciones_destacadas = Eleccion.objects.filter(featured=True)

        context['elecciones_buscables'] = elecciones_buscables
        context['elecciones_destacadas'] = elecciones_destacadas
        context['ultimas_preguntas']= Pregunta.objects.all().order_by('-id')[:5]
        context['ultimas_respuestas']= Respuesta.objects.exclude(texto_respuesta=settings.NO_ANSWER_DEFAULT_MESSAGE).order_by('-id')[:5]
        return context

class EleccionOverview(DetailView):
    model = Eleccion

    def get_context_data(self, **kwargs):
        context = super(EleccionOverview, self).get_context_data(**kwargs)
        indices = self.object.indice_set.filter(en_carrusel=True)
        elecciones = Eleccion.objects.all()
        context['indices'] = indices
        context['title'] = self.object.nombre
        context['elecciones'] = elecciones
        return context

        
class InteresesView(TemplateView):
    template_name = 'elecciones/perfiles_intereses.html'
    



class EleccionIndices(DetailView):
    model = Eleccion

    def get_template_names(self):
        return ['elecciones/todos_los_indices.html']

    def get_context_data(self, **kwargs):
        context = super(EleccionIndices, self).get_context_data(**kwargs)
        indices = self.object.indice_set.all()
        elecciones = Eleccion.objects.all()
        context['indices'] = indices
        context['title'] = self.object.nombre + u" índices detallados"
        context['elecciones'] = elecciones
        return context

class EleccionExtraInfo(DetailView):
    model = Eleccion

    def get_template_names(self):
        return ['elecciones/extra_info.html']

    def get_context_data(self, **kwargs):
        context = super(EleccionExtraInfo, self).get_context_data(**kwargs)
        context['title'] = u"Más Información sobre " + self.object.nombre
        return context

class NosFaltanDatosView(ListView):
    queryset = Candidato.sin_datos.all()
    context_object_name = "candidatos"

    def get_template_names(self):
        return ['elecciones/nos_faltan_datos.html']

class EleccionPreguntales(CreateView):
    #model = Pregunta
    form_class = PreguntaForm
    #template_name = 'elecciones/preguntales.html'
    success_url = 'preguntales'

    def get_template_names(self):
        if settings.PREGUNTALE_STATUS == 'GOING_ON':
            return ['elecciones/preguntales.html']
        if settings.PREGUNTALE_STATUS == 'COMING_SOON':
            return ['elecciones/preguntales_coming_soon.html']
        if settings.PREGUNTALE_STATUS == 'PASSED':
            return ['elecciones/preguntales_passed.html']

    def get_context_data(self, **kwargs):
        eleccion_slug = self.kwargs['slug']
        eleccion = get_object_or_404(Eleccion, slug = eleccion_slug)
        context = super(EleccionPreguntales, self).get_context_data(**kwargs)
        candidatos_eleccion = Candidato.objects.filter(eleccion = eleccion)
        contactos_candidato = Contacto.objects.filter(candidato__in = candidatos_eleccion)
        candidatos = candidatos_eleccion.filter(contacto__in = contactos_candidato)
        preguntas = Pregunta.objects.filter(candidato__in = candidatos_eleccion).filter(aprobada = True).distinct()
        context['preguntas'] = preguntas
        context['candidatos'] = candidatos
        todas_las_elecciones = Eleccion.objects.all()
        context['elecciones'] = todas_las_elecciones
        context['eleccion'] = eleccion
        
        return context

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.save()
        url = reverse('eleccion-preguntales', kwargs={'slug':self.kwargs['slug']})

        candidatos = form.cleaned_data['candidato']
        for candidato in candidatos:
            Respuesta.objects.create(candidato = candidato, pregunta = self.object)

        messages.success(self.request, '***\nTu pregunta ya está siendo procesada. En algunos minutos estará publicada.\n***') 
            
            
        return HttpResponseRedirect(url)

    def get_form_kwargs(self):
        kwargs = super(EleccionPreguntales, self).get_form_kwargs()
        eleccion_slug = self.kwargs['slug']
        eleccion = get_object_or_404(Eleccion, slug = eleccion_slug)
        kwargs['eleccion'] = eleccion
        return kwargs

class MetodologiaView(TemplateView):
    template_name="elecciones/metodologia.html"

    def get_context_data(self, **kwargs):
        context = super(MetodologiaView, self).get_context_data(**kwargs)
        context['title'] = u"Metodología"
        elecciones = Eleccion.objects.all()
        context['elecciones'] = elecciones
        return context

class ComparadorView(TemplateView):
    template_name="elecciones/comparador.html"

    def get_context_data(self, **kwargs):
        context = super(MetodologiaView, self).get_context_data(**kwargs)
        context['title'] = u"Comparador"
        elecciones = Eleccion.objects.all()
        context['elecciones'] = elecciones
        return context


class QuePuedoHacerHacerView(TemplateView):
    template_name = "elecciones/que_puedo_hacer.html"

    def get_context_data(self, **kwargs):
        context = super(QuePuedoHacerHacerView, self).get_context_data(**kwargs)
        context['title'] = u"¿Qué puedo hacer?"
        elecciones = Eleccion.objects.all()
        context['elecciones'] = elecciones
        return context

class EnlacesView(TemplateView):
    template_name="enlaces.html"

    def get_context_data(self, **kwargs):
        context = super(EnlacesView, self).get_context_data(**kwargs)
        context['title'] = u"Enlaces"
        return context

class VoluntariosView(TemplateView):
    template_name="voluntarios.html"

    def get_context_data(self, **kwargs):
        context = super(VoluntariosView, self).get_context_data(**kwargs)
        context['title'] = u"Gracias a TODOS"
        return context

class SenadoresView(TemplateView):
    template_name="todos_los_senadores.html"

    def get_context_data(self, **kwargs):
        context = super(SenadoresView, self).get_context_data(**kwargs)
        context['title'] = u"Todos los Senadores"
        return context

class QuienesSomosView(TemplateView):
    template_name="quienesSomos.html"

    def get_context_data(self, **kwargs):
        context = super(QuienesSomosView, self).get_context_data(**kwargs)
        context['title'] = u"Quienes somos"
        elecciones = Eleccion.objects.all()
        context['elecciones'] = elecciones
        return context


class ReportaView(TemplateView):
    template_name="elecciones/reporta.html"

    def get_context_data(self, **kwargs):
        context = super(ReportaView, self).get_context_data(**kwargs)
        context['title'] = u"Fiscaliza"
        elecciones = Eleccion.objects.all()
        context['elecciones'] = elecciones
        return context



class Ranking(TemplateView):
    template_name = "elecciones/ranking.html"

    def __init__(self, *args, **kwargs):
        pr = Respuesta.objects.exclude(texto_respuesta=settings.NO_ANSWER_DEFAULT_MESSAGE).count()
        rr = Respuesta.objects.count()
        self.coeficiente_de_premio = float(rr)/float(pr)
        return super(Ranking, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Ranking, self).get_context_data(**kwargs)
        clasificados = self.clasificados()
        context['malos'] = self.malos(clasificados)
        context['buenos'] = self.buenos(clasificados)
        return context

    def malos(self, clasificados):
        return sorted(clasificados,  key=itemgetter('indice'), reverse=False)[:settings.RANKING_LENGTH]

    def buenos(self, clasificados):
        return sorted(clasificados,  key=itemgetter('indice'), reverse=True)[:settings.RANKING_LENGTH]


    def clasificados(self):
        clasificados = []
        candidatos = Candidato.objects.all().annotate(preguntas_count=Count('pregunta')).exclude(preguntas_count=0)
        for candidato in candidatos:
            preg = candidato.numero_preguntas()
            resp = candidato.numero_respuestas()
            element = {
            'candidato':candidato,
            'pregunta_count':preg,
            'preguntas_respondidas':resp,
            'preguntas_no_respondidas':candidato.numero_preguntas() - candidato.numero_respuestas(),
            'indice':(self.coeficiente_de_premio + 1)*preg*resp - preg*preg
            }
            clasificados.append(element)
        return clasificados

class RankingJson(Ranking):
    #Terrible de feo copiar la lógica pero quiero salir rápido
    #luego lo refactorizo
    def dispatch(self, *args, **kwargs):
        return super(RankingJson, self).dispatch(*args, **kwargs)

    def clasificados(self):
        clasificados = super(RankingJson, self).clasificados()
        resultado = []
        for clasificado in clasificados:
            clasificado["candidato"] = clasificado["candidato"].nombre
            resultado.append(clasificado)

        return resultado

    def get(self, request, *args, **kwargs):
        self.callback = request.GET['callback']
        return super(RankingJson, self).get(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_content = self.callback+"("+data+");"
        return HttpResponse(response_content, mimetype="application/json")

