# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vote'
        db.create_table('faith_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('like', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('faith', ['Vote'])

        # Adding model 'Bar'
        db.create_table('faith_bar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('faith', ['Bar'])

        # Adding M2M table for field votes on 'Bar'
        db.create_table('faith_bar_votes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bar', models.ForeignKey(orm['faith.bar'], null=False)),
            ('vote', models.ForeignKey(orm['faith.vote'], null=False))
        ))
        db.create_unique('faith_bar_votes', ['bar_id', 'vote_id'])


    def backwards(self, orm):
        # Deleting model 'Vote'
        db.delete_table('faith_vote')

        # Deleting model 'Bar'
        db.delete_table('faith_bar')

        # Removing M2M table for field votes on 'Bar'
        db.delete_table('faith_bar_votes')


    models = {
        'faith.bar': {
            'Meta': {'object_name': 'Bar'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'votes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['faith.Vote']", 'symmetrical': 'False'})
        },
        'faith.vote': {
            'Meta': {'object_name': 'Vote'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'like': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['faith']