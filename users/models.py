from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    #user = models.ForeignKey(User, unique=True)
    user = models.OneToOneField(User)
    website = models.URLField("Website", blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
# Create your models here.
