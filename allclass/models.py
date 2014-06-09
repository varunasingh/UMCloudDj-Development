from django.db import models
from school.models import School
from django.contrib.auth.models import User

class Allclass(models.Model):
    allclass_name = models.CharField(max_length=300)
    allclass_desc = models.CharField(max_length=1000)
    allclass_location = models.CharField(max_length=200)

class School_Allclasses(models.Model):
    allclass_classid = models.ForeignKey(Allclass)
    school_schoolid = models.ForeignKey(School)

class Teacher_Allclasses(models.Model):
    allclass_classid = models.ForeignKey(Allclass)
    #because a teacher can be in more than one class(duh)
    teacher_userid = models.ManyToManyField(User)

class Student_Allclasses(models.Model):
    allclass_classid = models.ForeignKey(Allclass)
    #because a student can be in more than one class(duh)
    student_userid = models.ManyToManyField(User)

# Create your models here.
