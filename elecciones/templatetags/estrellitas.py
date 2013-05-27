from elecciones.models import Candidato
from django import template

register = template.Library()

@register.filter(name='estrellitas')
def estrellitas(candidato_id):

	candidato = Candidato.objects.get(pk=candidato_id)
	asterisco = '*'
	return asterisco*candidato.estrellitas

@register.filter(name='estrellitas_disabled')
def estrellitas_disabled(candidato_id):
	candidato = Candidato.objects.get(pk=candidato_id)
	if candidato.estrellitas == 3:
		return u'disabled="disabled"'
	return ''


@register.filter(name='estrellitas_tachado')
def estrellitas_tachado(candidato_id):
    candidato = Candidato.objects.get(pk=candidato_id)
    if candidato.estrellitas == 3:
        return u'tachado'
    return ''