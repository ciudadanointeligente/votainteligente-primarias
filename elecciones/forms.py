# -*- coding: utf-8 -*-

from models import Pregunta, Candidato
from django import forms
from captcha.fields import ReCaptchaField

class PreguntaForm(forms.ModelForm):

    captcha = ReCaptchaField(attrs={'theme' : 'clean','lang':'es'})
    class Meta:
        model = Pregunta

    # Representing the many to many related field in Pizza
    # Overriding __init__ here allows us to provide initial
    # data for 'toppings' field
    def __init__(self, *args, **kwargs):
    	eleccion = kwargs['eleccion']
    	del kwargs['eleccion']
    	super(PreguntaForm, self).__init__(*args, **kwargs)
    	candidatos = Candidato.objects.filter (eleccion = eleccion)

        self.fields['candidato'].widget = forms.CheckboxSelectMultiple()
        self.fields['candidato'].queryset = candidatos
	self.fields['candidato'].error_messages['required'] = 'Debes elegir al menos un candidato'
    	self.fields['remitente'].error_messages['required'] = 'Debes identificarte de alguna forma'
	self.fields['remitente'].error_messages['max_length'] = 'El nombre del remitente es demasiado largo'
    	self.fields['texto_pregunta'].error_messages['required'] = 'Debes hacer una pregunta'
	#No está funcionando con 'max_length', hay que buscar el valor apropiado. De todos modos sale en inglés
    	self.fields['texto_pregunta'].error_messages['max_length'] = 'La pregunta es demasiado larga'
    	self.fields['captcha'].error_messages['required'] = 'Debemos asegurarnos que no seas un robot'
    	self.fields['captcha'].error_messages['captcha_invalid'] = 'No ingresaste el valor correcto del captcha'
    	self.fields['captcha'].error_messages['invalid'] = 'El captcha que ingresaste no es válido'
        #self.fields['candidato'].help_text = 'Marca sólo los candidatos a los que quieras preguntar'
        #self.fields['candidato'].label = 'Candidatos'
        #self.fields['remitente'].widget.attrs['class'] = 'itemCandidato'
        #self.fields['remitente'].help_text = 'Identifícate como quieras'
        #self.fields['remitente'].initial = 'Comunero, Profesora, Dirigente, etc.'
        #self.fields['remitente'].label = 'Yo soy'
        #self.fields['texto_pregunta'].initial = 'Escribe una pregunta clara y respetuosa. Así aumentas la posibilidad de que respondan seriamente.'
        #self.fields['texto_pregunta'].label = 'Escribe tu pregunta'

        self.fields['remitente'].widget.attrs['class'] = 'input-xxlarge btn-block remitentePreguntale'
        self.fields['remitente'].widget.attrs['placeholder'] = 'Nombre, Estudiante, Profesora, Empresario, Campesino'
        self.fields['texto_pregunta'].widget.attrs['class'] = 'input-xxlarge btn-block'
        self.fields['texto_pregunta'].widget.attrs['placeholder'] = 'Escribe una pregunta clara y respetuosa. Revisa si otros han preguntado lo que a ti te interesa saber.'
        self.fields['texto_pregunta'].widget.attrs['rows'] = '5'
        self.fields['texto_pregunta'].widget.attrs['maxlength'] = '4095'

'''	
    # Overriding save allows us to process the value of 'toppings' field    
    def save(self, commit=True):
	#Recuperar los datos
	#pregunta = pregunta_form.save(commit = False)
        instance = ModelForm.save(self, False)

	#Crear respuestas
	for candidato_pk in self.cleaned_data['candidato']:
		candidato = Candidato.objects.filter(id=candidato_pk)
		instance.candidato_set.remove(candidato_pk)
		instance.candidato_set.add(candidato)
		
		#Crear respuesta

        # Do we need to save all changes now?
        if commit:
            instance.save()
            #self.save_m2m()

	return instance



        print 'saving'
        # Get the unsave Pizza instance
        instance = ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the pizza with toppings
           instance.candidato_set.clear()
           for candidato in self.cleaned_data['candidato']:

                instance.candidato_set.add(candidato)
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance
'''
