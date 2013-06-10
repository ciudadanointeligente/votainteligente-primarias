# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Eleccion.write_it_instance'
        db.add_column('elecciones_eleccion', 'write_it_instance',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['writeit.WriteItInstance'], unique=True, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Eleccion.write_it_instance'
        db.delete_column('elecciones_eleccion', 'write_it_instance_id')


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
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'write_it_instance': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['writeit.WriteItInstance']", 'unique': 'True', 'null': 'True'})
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
        },
        'writeit.writeitapiinstance': {
            'Meta': {'object_name': 'WriteItApiInstance'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        'writeit.writeitdocument': {
            'Meta': {'object_name': 'WriteItDocument'},
            'api_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['writeit.WriteItApiInstance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'writeit.writeitinstance': {
            'Meta': {'object_name': 'WriteItInstance', '_ormbases': ['writeit.WriteItDocument']},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'writeitdocument_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['writeit.WriteItDocument']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['elecciones']