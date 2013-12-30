# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Translation'
        db.create_table(u'translation_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_lang', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('target_lang', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('original', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('translated', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'translation', ['Translation'])


    def backwards(self, orm):
        # Deleting model 'Translation'
        db.delete_table(u'translation_translation')


    models = {
        u'translation.translation': {
            'Meta': {'object_name': 'Translation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'source_lang': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'target_lang': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'translated': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['translation']