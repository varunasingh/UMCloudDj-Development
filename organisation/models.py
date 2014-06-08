from django.db import models
from django.contrib.auth.models import User

class Organisation(models.Model):
   organisation_name = models.CharField(max_length=300)
   organisation_desc = models.CharField(max_length=1000)
   add_date = models.DateTimeField(auto_now_add=True)

class UMCloud_Package(models.Model):
   package_name = models.CharField(max_length=300)
   package_desc = models.CharField(max_length=2000)
   max_students = models.IntegerField()
   max_publishers = models.IntegerField()
   price_rate_permonth = models.FloatField()

class User_Organisations(models.Model):
   add_date = models.DateTimeField(auto_now_add=True)
   user_userid = models.ForeignKey(User)
   organisation_organisationid = models.ForeignKey(Organisation)
   set_package = models.ForeignKey(UMCloud_Package)



# Create your models here.
