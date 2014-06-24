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
    #for school in schools:
	#organisation = Organisation_Schools.objects.get(school_schoolid=school).organisation_organisationid
	#organisation_schools.append(organisation)

    data = {}
    data['object_list'] = schools
    #data['object_list'] = zip(schools, organisation_schools)
    data['orgschools_list'] = organisation_schools
    return render(request, template_name, data)

@login_required(login_url='/login/')
def school_table(request, template_name='school/school_table.html'):
    schools = School.objects.all()
    organisation_schools = []
    #for school in schools:
        #organisation = Organisation_Schools.objects.get(school_schoolid=school).organisation_organisationid
        #organisation_schools.append(organisation)

    data = {}
    data['object_list'] = schools
    #data['object_list'] = zip(schools, organisation_schools)
    data['orgschools_list'] = organisation_schools
    schools_as_json = serializers.serialize('json', schools)
    schools_as_json =json.loads(schools_as_json)

    return render(request, template_name, {'data':data, 'schools_as_json':schools_as_json})

@login_required(login_url='/login/')
def school_exists(name):
    print("Checking..")
    school_count = School.objects.filter(school_name=name).count()
    if school_count == 0:
        return False
    return True

@login_required(login_url='/login/')
def create_school(school_name, school_desc, organisationid):
    print("Creating school object")
    print("Creating organisation school mapping..")
    organisation = Organisation.objects.get(pk=organisationid)

    school = School(school_name=school_name, school_desc=school_desc, organisation=organisation)
    school.save()

    print("Organisation School mapping success.")
    return school




@login_required(login_url='/login/')
def school_create(request, template_name='school/school_create.html'):
    form = SchoolForm(request.POST or None)
    organisations = Organisation.objects.all()
    data = {}
    data['object_list'] = organisations

    if request.method == 'POST':
        post = request.POST;
        #try:
	if 1 > 0:
		name = post['school_name']
		print(name)
		school_count = School.objects.filter(school_name=name).count()
        	#if not school_exists(post['school_name']):
		print("school_count:")
		print(school_count)
		if school_count == 0:
                	print("Creating the School..")
			print("Creating school object")
			school_name = post['school_name']
			school_desc = post['school_desc']
			organisationid = post['organisationid']
			currentorganisation=Organisation.objects.get(pk=organisationid)
    			school = School(school_name=school_name, school_desc=school_desc, organisation=currentorganisation)
    			school.save()
    
    			print("Creating organisation school mapping..")
    
    			print("Organisation School mapping success.")

                	#school = create_school(school_name=post['school_name'], school_desc=post['school_desc'], organisationid=post['organisationid'])
                	return redirect('school_list')
        	else:
                	#Show message that the school name already exists in our database.
                	return redirect('school_list')
	#except:
	else:
		#pass
		print('Something went wrong')
	#return('school_list')
	

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

# Create your views here.
