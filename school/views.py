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
from organisation.models import Organisation_Package
from school.models import School
from school.models import Organisation_Schools

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
# School CRUD

class SchoolForm(ModelForm):
    class Meta:
        model = School

@login_required(login_url='/login/')
def school_list(request, template_name='school/school_list.html'):
    schools = School.objects.all()
    organisation_schools = []
    for school in schools:
	organisation = Organisation_Schools.objects.get(school_schoolid=school).organisation_organisationid
	organisation_schools.append(organisation)

    data = {}
    data['object_list'] = schools
    data['object_list'] = zip(schools, organisation_schools)
    data['orgschools_list'] = organisation_schools
    return render(request, template_name, data)

@login_required(login_url='/login/')
def school_create(request, template_name='school/school_create.html'):
    form = SchoolForm(request.POST or None)
    organisations = Organisation.objects.all()
    data = {}
    data['object_list'] = organisations

    if request.method == 'POST':
        post = request.POST;
        if not school_exists(post['school_name']):
                print("Creating the School..")
                school = create_school(school_name=post['school_name'], school_desc=post['school_desc'], organisationid=post['organisationid'])
                return redirect('school_list')
        else:
                #Show message that the school name already exists in our database.
                return redirect('school_list')

    return render(request, template_name, data)

@login_required(login_url='/login/')
def school_update(request, pk, template_name='school/school_form.html'):
    school = get_object_or_404(School, pk=pk)
    form = SchoolForm(request.POST or None, instance=school)
    if form.is_valid():
        form.save()
        return redirect('school_list')
    return render(request, template_name, {'form':form})

@login_required(login_url='/login/')
def school_delete(request, pk, template_name='school/school_confirm_delete.html'):
    school = get_object_or_404(School, pk=pk)
    if request.method=='POST':
        school.delete()
        return redirect('school_list')
    return render(request, template_name, {'object':school})

@login_required(login_url='/login/')
def school_exists(name):
    school_count = School.objects.filter(school_name=name).count()
    if school_count == 0:
        return False
    return True

@login_required(login_url='/login/')
def create_school(school_name, school_desc, organisationid):
    school = School(school_name=school_name, school_desc=school_desc)
    school.save()
    organisation = Organisation.objects.get(pk=organisationid)

    #Create Organisation - School mapping
    organisation_school = Organisation_Schools(school_schoolid=school, organisation_organisationid=organisation)
    organisation_school.save()

    print("Organisation School mapping success.")
    return school


# Create your views here.
