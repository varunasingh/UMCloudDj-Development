from django.db import models
from django.contrib.auth.models import User
from organisation.models import Organisation

class School(models.Model):
   school_name = models.CharField(max_length=300)
   school_desc = models.CharField(max_length=1000)

class Organisation_Schools(models.Model):
   school_schoolid = models.ForeignKey(School)
   organisation_organisationid = models.ForeignKey(Organisation)


# Create your models here.
