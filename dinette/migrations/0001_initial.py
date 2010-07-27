
from south.db import db
from django.db import models
from dinette.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'DinetteUserProfile'
        db.create_table('dinette_dinetteuserprofile', (
            ('id', orm['dinette.DinetteUserProfile:id']),
            ('user', orm['dinette.DinetteUserProfile:user']),
            ('last_activity', orm['dinette.DinetteUserProfile:last_activity']),
            ('userrank', orm['dinette.DinetteUserProfile:userrank']),
            ('last_posttime', orm['dinette.DinetteUserProfile:last_posttime']),
            ('photo', orm['dinette.DinetteUserProfile:photo']),
            ('signature', orm['dinette.DinetteUserProfile:signature']),
        ))
        db.send_create_signal('dinette', ['DinetteUserProfile'])
        
        # Adding model 'Ftopics'
        db.create_table('dinette_ftopics', (
            ('id', orm['dinette.Ftopics:id']),
            ('category', orm['dinette.Ftopics:category']),
            ('subject', orm['dinette.Ftopics:subject']),
            ('slug', orm['dinette.Ftopics:slug']),
            ('message', orm['dinette.Ftopics:message']),
            ('file', orm['dinette.Ftopics:file']),
            ('attachment_type', orm['dinette.Ftopics:attachment_type']),
            ('filename', orm['dinette.Ftopics:filename']),
            ('viewcount', orm['dinette.Ftopics:viewcount']),
            ('replies', orm['dinette.Ftopics:replies']),
            ('created_on', orm['dinette.Ftopics:created_on']),
            ('updated_on', orm['dinette.Ftopics:updated_on']),
            ('posted_by', orm['dinette.Ftopics:posted_by']),
            ('announcement_flag', orm['dinette.Ftopics:announcement_flag']),
            ('is_closed', orm['dinette.Ftopics:is_closed']),
            ('is_sticky', orm['dinette.Ftopics:is_sticky']),
            ('is_hidden', orm['dinette.Ftopics:is_hidden']),
        ))
        db.send_create_signal('dinette', ['Ftopics'])
        
        # Adding model 'SiteConfig'
        db.create_table('dinette_siteconfig', (
            ('id', orm['dinette.SiteConfig:id']),
            ('name', orm['dinette.SiteConfig:name']),
            ('tag_line', orm['dinette.SiteConfig:tag_line']),
        ))
        db.send_create_signal('dinette', ['SiteConfig'])
        
        # Adding model 'Category'
        db.create_table('dinette_category', (
            ('id', orm['dinette.Category:id']),
            ('name', orm['dinette.Category:name']),
            ('slug', orm['dinette.Category:slug']),
            ('description', orm['dinette.Category:description']),
            ('ordering', orm['dinette.Category:ordering']),
            ('super_category', orm['dinette.Category:super_category']),
            ('created_on', orm['dinette.Category:created_on']),
            ('updated_on', orm['dinette.Category:updated_on']),
            ('posted_by', orm['dinette.Category:posted_by']),
        ))
        db.send_create_signal('dinette', ['Category'])
        
        # Adding model 'Reply'
        db.create_table('dinette_reply', (
            ('id', orm['dinette.Reply:id']),
            ('topic', orm['dinette.Reply:topic']),
            ('posted_by', orm['dinette.Reply:posted_by']),
            ('message', orm['dinette.Reply:message']),
            ('file', orm['dinette.Reply:file']),
            ('attachment_type', orm['dinette.Reply:attachment_type']),
            ('filename', orm['dinette.Reply:filename']),
            ('created_on', orm['dinette.Reply:created_on']),
            ('updated_on', orm['dinette.Reply:updated_on']),
        ))
        db.send_create_signal('dinette', ['Reply'])
        
        # Adding model 'SuperCategory'
        db.create_table('dinette_supercategory', (
            ('id', orm['dinette.SuperCategory:id']),
            ('name', orm['dinette.SuperCategory:name']),
            ('description', orm['dinette.SuperCategory:description']),
            ('ordering', orm['dinette.SuperCategory:ordering']),
            ('created_on', orm['dinette.SuperCategory:created_on']),
            ('updated_on', orm['dinette.SuperCategory:updated_on']),
            ('posted_by', orm['dinette.SuperCategory:posted_by']),
        ))
        db.send_create_signal('dinette', ['SuperCategory'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'DinetteUserProfile'
        db.delete_table('dinette_dinetteuserprofile')
        
        # Deleting model 'Ftopics'
        db.delete_table('dinette_ftopics')
        
        # Deleting model 'SiteConfig'
        db.delete_table('dinette_siteconfig')
        
        # Deleting model 'Category'
        db.delete_table('dinette_category')
        
        # Deleting model 'Reply'
        db.delete_table('dinette_reply')
        
        # Deleting model 'SuperCategory'
        db.delete_table('dinette_supercategory')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dinette.category': {
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderated_by': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cposted'", 'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '110', 'db_index': 'True'}),
            'super_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dinette.SuperCategory']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'dinette.dinetteuserprofile': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_activity': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_posttime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'signature': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'userrank': ('django.db.models.fields.CharField', [], {'default': "'Junior Member'", 'max_length': '30'})
        },
        'dinette.ftopics': {
            'announcement_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'attachment_type': ('django.db.models.fields.CharField', [], {'default': "'nofile'", 'max_length': '20'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dinette.Category']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "'dummyname.txt'", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'replies': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '1034', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'viewcount': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'dinette.reply': {
            'attachment_type': ('django.db.models.fields.CharField', [], {'default': "'nofile'", 'max_length': '20'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "'dummyname.txt'", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dinette.Ftopics']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'dinette.siteconfig': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tag_line': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        'dinette.supercategory': {
            'accessgroups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['dinette']
