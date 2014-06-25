from django.shortcuts import render

from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, redirect, get_object_or_404 #Added 404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import auth
from django.template import RequestContext

#Testing..
from django.forms import ModelForm
from organisation.models import Organisation
from organisation.models import UMCloud_Package
from organisation.models import User_Organisations
from school.models import School
from allclass.models import Allclass
from uploadeXe.models import Role
from uploadeXe.models import User_Roles

from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
import datetime
import time
import os
import urllib
import urllib2, base64, json
import glob #For file ^VS 130420141454

###################################
# Allclass CRUD

class AllclassForm(ModelForm):
    class Meta:
        model = Allclass

@login_required(login_url='/login/')
def allclass_list(request, template_name='allclass/allclass_list.html'):
    allclasses = Allclass.objects.all()
    school_allclasses = []
    #for allclass in allclasses:
        #school = School_Allclasses.objects.get(allclass_classid=allclass).school_schoolid
        #school_allclasses.append(school)

    data = {}
    data['object_list'] = allclasses
    #data['object_list'] = zip(allclasses, school_allclasses)
    data['school_list'] = school_allclasses
    return render(request, template_name, data)


@login_required(login_url='/login/')
def allclass_table(request, template_name='allclass/allclass_table.html'):
    allclasses = Allclass.objects.all()
    school_allclasses = []
    for allclass in allclasses:
	school_name=allclass.school.school_name
        #school = School_Allclasses.objects.get(allclass_classid=allclass).school_schoolid
        school_allclasses.append(school_name)

    data = {}
    data['object_list'] = allclasses
    data['object_list'] = zip(allclasses, school_allclasses)
    data['school_list'] = school_allclasses
    allclasses_as_json = serializers.serialize('json', allclasses)
    allclasses_as_json =json.loads(allclasses_as_json)

    return render(request, template_name, {'data':data, 'allclasses_as_json':allclasses_as_json})
    #return render(request, template_name, data)


@login_required(login_url='/login/')
def allclass_create(request, template_name='allclass/allclass_create.html'):
    form = AllclassForm(request.POST or None)
    schools = School.objects.all()
    teacher_role = Role.objects.get(pk=5)
    student_role = Role.objects.get(pk=6)
    
    teachers = User.objects.filter(pk__in=User_Roles.objects.filter(role_roleid=teacher_role).values_list('user_userid', flat=True))

    students = User.objects.filter(pk__in=User_Roles.objects.filter(role_roleid=student_role).values_list('user_userid', flat=True))
    data = {}
    data['object_list'] = schools
    data['teacher_list'] = teachers
    data['student_list'] = students

    if request.method == 'POST':
        post = request.POST;
	print("checking..")
	class_name = post['class_name']
	allclass_count = Allclass.objects.filter(allclass_name=class_name).count()
    	if allclass_count == 0:
        #if not allclass_exists(post['class_name']):
                print("Creating the Class..")
		class_name=post['class_name']
		class_desc=post['class_desc']
		class_location=post['class_location']
		schoolid=post['schoolid']
		teacherid=post['teacherid']

		studentidspicklist=post.getlist('target')
		print("students selected from picklist:")
		print(studentidspicklist)

		currentschool = School.objects.get(pk=schoolid)
		
    		allclass = Allclass(allclass_name=class_name, allclass_desc=class_desc, allclass_location=class_location,school=currentschool)
    		allclass.save()
    		school = School.objects.get(pk=schoolid)
		print("Class School mapping success.")


		print("Class Students mapping success.")

		#Create Class - StudentS mapping
		for everystudentid in studentidspicklist:
			print("Looping student:")
			print(everystudentid)
			currentstudent=User.objects.get(pk=everystudentid)
			allclass.students.add(currentstudent)
			allclass.save()

		currentteacher=User.objects.get(pk=teacherid)
		allclass.teachers.add(currentteacher)
		allclass.save()

                #allclass = create_allclass(class_name=post['class_name'], class_desc=post['class_desc'], class_location=post['class_location'], schoolid=post['schoolid'], studentids=post.getlist('studentids'))
                return redirect('allclass_table')
        else:
		print("Class already exists")
                #Show message that the class name already exists in our database. (For the current organisation)
                return redirect('allclass_table')

    return render(request, template_name, data)

@login_required(login_url='/login/')
def allclass_update(request, pk, template_name='allclass/allclass_form.html'):
    allclass = get_object_or_404(Allclass, pk=pk)
    form = AllclassForm(request.POST or None, instance=allclass)
    if form.is_valid():
        form.save()
        return redirect('allclass_table')
    return render(request, template_name, {'form':form})

@login_required(login_url='/login/')
def allclass_delete(request, pk, template_name='allclass/allclass_confirm_delete.html'):
    allclass = get_object_or_404(Allclass, pk=pk)
    if request.method=='POST':
        allclass.delete()
        return redirect('allclass_table')
    return render(request, template_name, {'object':allclass})

@login_required(login_url='/login/')
def allclass_exists(name):
    allclass_count = Allclass.objects.filter(allclass_name=name).count()
    if allclass_count == 0:
        return False
    return True

# Create your views here.
