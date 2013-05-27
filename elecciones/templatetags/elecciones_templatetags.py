from elecciones.models import Eleccion
from django import template

register = template.Library()

def elecciones_search():
	elecciones_buscables = Eleccion.objects.filter(searchable=True)
	return {'elecciones_buscables':elecciones_buscables}

register.inclusion_tag('elecciones_search.html')(elecciones_search)

def elecciones_destacadas():
	elecciones_destacadas = Eleccion.objects.filter(featured=True)
	return {'elecciones_destacadas':elecciones_destacadas}

register.inclusion_tag('elecciones_destacadas.html')(elecciones_destacadas)