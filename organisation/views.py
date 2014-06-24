
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
# Organisation CRUD

class OrganisationForm(ModelForm):
    class Meta:
        model = Organisation

def organisation_list(request, template_name='organisation/organisation_list.html'):
    organisations = Organisation.objects.all()
    organisation_packages = []
    #for organisation in organisations:
	#umpackage = Organisation_Package.objects.get(organisation_organisationid=organisation).set_package
	#organisation_packages.append(umpackage)


    data = {}
    data['object_list'] = organisations
    #data['object_list'] = zip(organisations,organisation_packages)
    data['umpackage_list'] = organisation_packages
    return render(request, template_name, data)

def organisation_table(request, template_name='organisation/organisation_table.html'):
    organisations = Organisation.objects.all()
    organisation_packages = []
    #for organisation in organisations:
        #umpackage = Organisation_Package.objects.get(organisation_organisationid=organisation).set_package
        #organisation_packages.append(umpackage)

    data = {}
    data['object_list'] = organisations
    #data['object_list'] = zip(organisations,organisation_packages)
    data['umpackage_list'] = organisation_packages
    organisations_as_json = serializers.serialize('json', organisations)
    organisations_as_json =json.loads(organisations_as_json)

    return render(request, template_name, {'data': data, 'organisations_as_json':organisations_as_json})

    
def organisation_exists(name):
    organisation_count = Organisation.objects.filter(organisation_name=name).count()
    if organisation_count == 0:
        return False
    return True

def create_organisation(organisation_name, organisation_desc, umpackageid):
    umpackage = UMCloud_Package.objects.get(pk=umpackageid)
    organisation = Organisation(organisation_name=organisation_name, organisation_desc=organisation_desc, set_package=umpackage)
    organisation.save()

    print("Organisation Package mapping success.")
    return organisation


def organisation_create(request, template_name='organisation/organisation_create.html'):
    form = OrganisationForm(request.POST or None)
    umpackages = UMCloud_Package.objects.all()
    data = {}
    data['object_list'] = umpackages
    
    if request.method == 'POST':
        post = request.POST;
        if not organisation_exists(post['organisation_name']):
                print("Creating the organisation..")
		organisation = create_organisation(organisation_name=post['organisation_name'], organisation_desc=post['organisation_desc'], umpackageid=post['umpackageid'])
                return redirect('organisation_table')
		#Set users
        else:
                #Show message that the username/email address already exists in our database.
                return redirect('organisation_table')

    return render(request, template_name, data)




    """
    form = OrganisationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('organisation_list')
    return render(request, template_name, {'form':form})
    """

def organisation_update(request, pk, template_name='organisation/organisation_form.html'):
    organisation = get_object_or_404(Organisation, pk=pk)
    form = OrganisationForm(request.POST or None, instance=organisation)
    if form.is_valid():
        form.save()
        return redirect('organisation_list')
    return render(request, template_name, {'form':form})

def organisation_delete(request, pk, template_name='organisation/organisation_confirm_delete.html'):
    organisation = get_object_or_404(Organisation, pk=pk)
    if request.method=='POST':
        organisation.delete()
        return redirect('organisation_list')
    return render(request, template_name, {'object':organisation})

####################################

###################################
# UMCloud_Package CRUD

class UMCloud_PackageForm(ModelForm):
    class Meta:
        model = UMCloud_Package

def umpackage_list(request, template_name='organisation/umpackage_list.html'):
    umpackages = UMCloud_Package.objects.all()
    data = {}
    data['object_list'] = umpackages
    return render(request, template_name, data)


def umpackage_table(request, template_name='organisation/umpackage_table.html'):
    umpackages = UMCloud_Package.objects.all()
    data = {}
    data['object_list'] = umpackages
    umpackages_as_json = serializers.serialize('json', umpackages)
    umpackages_as_json =json.loads(umpackages_as_json)

    return render(request, template_name, {'data':data, 'umpackages_as_json':umpackages_as_json})

def umpackage_create(request, template_name='organisation/umpackage_form.html'):
    form = UMCloud_PackageForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('umpackage_list')
    return render(request, template_name, {'form':form})

def umpackage_update(request, pk, template_name='organisation/umpackage_form.html'):
    umpackage = get_object_or_404(UMCloud_Package, pk=pk)
    form = UMCloud_PackageForm(request.POST or None, instance=umpackage)
    if form.is_valid():
        form.save()
        return redirect('umpackage_list')
    return render(request, template_name, {'form':form})

def umpackage_delete(request, pk, template_name='organisation/umpackage_confirm_delete.html'):
    umpackage = get_object_or_404(UMCloud_Package, pk=pk)
    if request.method=='POST':
        umpackage.delete()
        return redirect('umpackage_list')
    return render(request, template_name, {'object':umpackage})

####################################


# Create your views here.
