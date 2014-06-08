
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
    data = {}
    data['object_list'] = organisations
    return render(request, template_name, data)

def organisation_create(request, template_name='organisation/organisation_form.html'):
    form = OrganisationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('organisation_list')
    return render(request, template_name, {'form':form})

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
