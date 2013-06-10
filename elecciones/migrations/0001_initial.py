# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Eleccion'
        db.create_table('elecciones_eleccion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('popit_api_instance', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['popit.ApiInstance'], unique=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('main_embedded', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('messaging_extra_app_url', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('mapping_extra_app_url', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('searchable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('featured_caption', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('extra_info_title', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('extra_info_content', self.gf('django.db.models.fields.TextField')(max_length=3000, null=True, blank=True)),
        ))
        db.send_create_signal('elecciones', ['Eleccion'])

        # Adding model 'Area'
        db.create_table('elecciones_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('clase_en_carrusel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('segunda_clase', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('elecciones', ['Area'])

        # Adding model 'Dato'
        db.create_table('elecciones_dato', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('imagen', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('link_metodologia', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('elecciones', ['Dato'])

        # Adding model 'Indice'
        db.create_table('elecciones_indice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eleccion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elecciones.Eleccion'])),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elecciones.Area'])),
            ('dato', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elecciones.Dato'])),
            ('encabezado', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('numero_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('texto_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('numero_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('texto_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('texto_pie_pagina_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('numero_pie_pagina_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('texto_pie_pagina_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('numero_pie_pagina_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('texto_pie_pagina_3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('numero_pie_pagina_3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('en_carrusel', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('elecciones', ['Indice'])

        # Adding model 'Colectivo'
        db.create_table('elecciones_colectivo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sigla', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('elecciones', ['Colectivo'])

        # Adding model 'Candidato'
        db.create_table('elecciones_candidato', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eleccion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elecciones.Eleccion'])),
            ('colectivo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elecciones.Colectivo'], null=True, blank=True)),
            ('partido', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('web', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['popit.Person'], null=True)),
        ))
        db.send_create_signal('elecciones', ['Candidato'])

        # Adding model 'Contacto'
        db.create_table('elecciones_contacto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('valor', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('candidato', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elecciones.Candidato'])),
        ))
        db.send_create_signal('elecciones', ['Contacto'])

        # Adding model 'Pregunta'
        db.create_table('elecciones_pregunta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remitente', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email_sender', self.gf('django.db.models.fields.EmailField')(max_length=100, null=True, blank=True)),
            ('texto_pregunta', self.gf('django.db.models.fields.TextField')()),
            ('aprobada', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('procesada', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('elecciones', ['Pregunta'])

        # Adding model 'Respuesta'
        db.create_table('elecciones_respuesta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pregunta', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elecciones.Pregunta'])),
            ('candidato', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elecciones.Candidato'])),
            ('texto_respuesta', self.gf('django.db.models.fields.TextField')(default=u'No pasa naipe a\xfan loco')),
        ))
        db.send_create_signal('elecciones', ['Respuesta'])


    def backwards(self, orm):
        # Deleting model 'Eleccion'
        db.delete_table('elecciones_eleccion')

        # Deleting model 'Area'
        db.delete_table('elecciones_area')

        # Deleting model 'Dato'
        db.delete_table('elecciones_dato')

        # Deleting model 'Indice'
        db.delete_table('elecciones_indice')

        # Deleting model 'Colectivo'
        db.delete_table('elecciones_colectivo')

        # Deleting model 'Candidato'
        db.delete_table('elecciones_candidato')

        # Deleting model 'Contacto'
        db.delete_table('elecciones_contacto')

        # Deleting model 'Pregunta'
        db.delete_table('elecciones_pregunta')

        # Deleting model 'Respuesta'
        db.delete_table('elecciones_respuesta')


    models = {
        'elecciones.area': {
            'Meta': {'object_name': 'Area'},
            'clase_en_carrusel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'segunda_clase': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'elecciones.candidato': {
            'Meta': {'object_name': 'Candidato'},
            'colectivo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elecciones.Colectivo']", 'null': 'True', 'blank': 'True'}),
            'eleccion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elecciones.Eleccion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partido': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['popit.Person']", 'null': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'web': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'elecciones.colectivo': {
            'Meta': {'object_name': 'Colectivo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sigla': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'elecciones.contacto': {
            'Meta': {'object_name': 'Contacto'},
            'candidato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elecciones.Candidato']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'valor': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'elecciones.dato': {
            'Meta': {'object_name': 'Dato'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'link_metodologia': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'elecciones.eleccion': {
            'Meta': {'object_name': 'Eleccion'},
            'extra_info_content': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'extra_info_title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'featured_caption': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_embedded': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'mapping_extra_app_url': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'messaging_extra_app_url': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'popit_api_instance': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['popit.ApiInstance']", 'unique': 'True'}),
            'searchable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'elecciones.indice': {
            'Meta': {'object_name': 'Indice'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elecciones.Area']"}),
            'dato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elecciones.Dato']"}),
            'eleccion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elecciones.Eleccion']"}),
            'en_carrusel': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'encabezado': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'numero_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'numero_pie_pagina_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'numero_pie_pagina_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'numero_pie_pagina_3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'texto_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'texto_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'texto_pie_pagina_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'texto_pie_pagina_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'texto_pie_pagina_3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'elecciones.pregunta': {
            'Meta': {'object_name': 'Pregunta'},
            'aprobada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'candidato': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pregunta'", 'symmetrical': 'False', 'through': "orm['elecciones.Respuesta']", 'to': "orm['elecciones.Candidato']"}),
            'email_sender': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'procesada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'remitente': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'texto_pregunta': ('django.db.models.fields.TextField', [], {})
        },
        'elecciones.respuesta': {
            'Meta': {'object_name': 'Respuesta'},
            'candidato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elecciones.Candidato']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pregunta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elecciones.Pregunta']"}),
            'texto_respuesta': ('django.db.models.fields.TextField', [], {'default': "u'No pasa naipe a\\xfan loco'"})
        },
        'popit.apiinstance': {
            'Meta': {'object_name': 'ApiInstance'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('popit.fields.ApiInstanceURLField', [], {'unique': 'True', 'max_length': '200'})
        },
        'popit.person': {
            'Meta': {'object_name': 'Person'},
            'api_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['popit.ApiInstance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'popit_url': ('popit.fields.PopItURLField', [], {'default': "''", 'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['elecciones']