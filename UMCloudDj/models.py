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

class Ustadmobiletest(models.Model):
   name = models.CharField(max_length=300)
   result = models.CharField(max_length=200)
   runtime = models.CharField(max_length=100)
   dategroup = models.CharField(max_length=100)
   platform = models.CharField(max_length=100)
   ustad_version = models.CharField(max_length=100)
   pub_date = models.DateTimeField(auto_now_add=True)
   upd_date = models.DateTimeField(auto_now=True)
   


# Create your models here.
