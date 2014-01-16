# -*- coding: utf-8 -*-
from django.db import models
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
   
# Create your models here.
