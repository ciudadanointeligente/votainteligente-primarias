# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

class ColectivoAdmin(admin.ModelAdmin):
	model = Colectivo
admin.site.register(Colectivo,ColectivoAdmin)

class IndiceInline(admin.TabularInline):
    model = Indice

class CandidatoInline(admin.TabularInline):
    model = Candidato
    extra = 0

class PreguntaInline(admin.TabularInline):
	model = Pregunta

class RespuestaInline(admin.TabularInline):
	model = Respuesta
	readonly_fields = ['candidato']
	extra = 0
class EleccionAdmin(admin.ModelAdmin):
	search_fields = ['nombre', 'candidato__nombre']
	inlines = [
		CandidatoInline,
        IndiceInline
    ]
admin.site.register(Eleccion, EleccionAdmin)
# action de aprobacion masiva de preguntas
def aprobar_preguntas(modeladmin, request, queryset):
	for obj in queryset:
		obj.enviar()
		obj.procesada=True
		obj.aprobada=True
		obj.save()

aprobar_preguntas.short_description = "Aprobar Preguntas para enviar"

class PreguntaAdmin(admin.ModelAdmin):
	model = Pregunta
	list_display = ['texto_pregunta', 'aprobada', 'procesada']
	ordering = ['aprobada','procesada']
	# readonly_fields = ['procesada']
	actions = [aprobar_preguntas]
	inlines = [RespuestaInline]

	#funcion especial para la aprobación de mail en el admin
	def save_model(self, request, obj, form, change):
	    if obj.aprobada and not obj.procesada:
	    	obj.enviar()
	    	obj.procesada=True

	    obj.save()



		    

admin.site.register(Pregunta, PreguntaAdmin)

class AreaAdmin(admin.ModelAdmin):
	pass

admin.site.register(Area, AreaAdmin)


class DatoAdmin(admin.ModelAdmin):
	pass

admin.site.register(Dato, DatoAdmin)
class ContactoAdmin(admin.ModelAdmin):
	search_fields = ['valor', 'candidato__nombre']

admin.site.register(Contacto, ContactoAdmin)






