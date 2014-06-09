# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User #Added user.
from django.core.urlresolvers import reverse #Added reverse..
import os
import uuid
import time

def get_file_path(instance, filename):
   ext = filename.split('.')[-1]
   ext = "um."
   filename = "%s.%s" % (uuid.uuid4(), ext) + filename
   return os.path.join('eXeUpload/', filename)

def update_filename(instance, filename):
   path = "eXeUpload/"
   timestamp = str(time.time())
   filename = instance.user + timestamp + ".um." + filename
   return os.path.join(path, filename)

class Document(models.Model):
   #exefile = models.FileField(upload_to='documents/%Y/%m/%d')
   #exefile = models.FileField(upload_to='eXeUpload/') #saves in exeUpload directory
   exefile = models.FileField(upload_to=get_file_path) #saves as a unique id.
   #exefile = models.FileField(upload_to=update_filename) #timestamp+filename
   name = models.CharField(max_length=200)
   pub_date = models.DateTimeField(auto_now_add=True) #added by Varuna Singh
   upd_date = models.DateTimeField(auto_now=True)
   userid = models.CharField(max_length=200)
   url = models.CharField(max_length=200)
   uid = models.CharField(max_length=200)
   success = models.CharField(max_length=10)
   
class Ustadmobiletest(models.Model):
   name = models.CharField(max_length=300)
   result = models.CharField(max_length=200)
   runtime = models.CharField(max_length=100)
   dategroup = models.CharField(max_length=100)
   platform = models.CharField(max_length=100)
   ustad_version = models.CharField(max_length=100)
   pub_date = models.DateTimeField(auto_now_add=True)
   upd_date = models.DateTimeField(auto_now=True)

class Role(models.Model):
   #Assuming Django makes ID auto increment for every model by default
   role_name = models.CharField(max_length=300)
   role_desc = models.CharField(max_length=300)
   def __unicode__(self):
	return self.role_name
   def get_absolute_url(self):
	return reverse('role_edit', kwargs={'pk': self.pk})

class User_Roles(models.Model):
   name = models.CharField(max_length=200)
   user_userid = models.ForeignKey(User)
   role_roleid = models.ForeignKey(Role)
   #role_roleid = models.ManyToManyField(Role)
   add_date = models.DateTimeField(auto_now_add=True)
   def first(self):
	return self[0]
   
# Create your models here.
