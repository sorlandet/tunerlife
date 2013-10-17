# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BodyStyle'
        db.create_table(u'auto_bodystyle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
        ))
        db.send_create_signal(u'auto', ['BodyStyle'])

        # Adding model 'CarSegment'
        db.create_table(u'auto_carsegment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
        ))
        db.send_create_signal(u'auto', ['CarSegment'])


    def backwards(self, orm):
        # Deleting model 'BodyStyle'
        db.delete_table(u'auto_bodystyle')

        # Deleting model 'CarSegment'
        db.delete_table(u'auto_carsegment')


    models = {
        u'auto.bodystyle': {
            'Meta': {'ordering': "['name']", 'object_name': 'BodyStyle'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'auto.carsegment': {
            'Meta': {'ordering': "['name']", 'object_name': 'CarSegment'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'tags': ('tagging.fields.TagField', [], {})
        }
    }

    complete_apps = ['auto']