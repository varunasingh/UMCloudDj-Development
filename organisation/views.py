
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
from UMCloudDj.views import create_user_more, user_exists
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
# Organisation CRUD

class OrganisationForm(ModelForm):
    class Meta:
        model = Organisation

"""
@login_required(login_url='/login/')
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
"""
def is_superadmin(user, organisation):
    print("testing")
    return None

@login_required(login_url='/login/')
def organisation_table(request, template_name='organisation/organisation_table.html'):
    if (request.user.is_staff==True):
	organisations = Organisation.objects.all()
    	organisation_packages = []

    	data = {}
    	data['object_list'] = organisations
    	#data['object_list'] = zip(organisations,organisation_packages)
    	data['umpackage_list'] = organisation_packages
    	organisations_as_json = serializers.serialize('json', organisations)
    	organisations_as_json =json.loads(organisations_as_json)

    	return render(request, template_name, {'data': data, 'organisations_as_json':organisations_as_json})

        
    else:
        print("Not a staff.")
        state="You do not have permission to see this page."
        return render(request, template_name, {'state':state})

 
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

@login_required(login_url='/login/')
def organisation_create(request, template_name='organisation/organisation_create.html'):
    if (request.user.is_staff==True):
	form = OrganisationForm(request.POST or None)
	organisations=Organisation.objects.all()
    	umpackages = UMCloud_Package.objects.all()
    	data = {}
    	data['object_list'] = umpackages
	data['organisation_list'] = organisations

    	if request.method == 'POST':
        	post = request.POST;
        	password=post['password']
        	passwordagain=post['passwordagain']
        	if password != passwordagain:
                	password=None
                	print("Passwords dont match")
                	state="The two passwords you gave do not match. Please try again."
                	data['state']=state
                	return render(request, template_name, data)

        	if not user_exists(post['username']):
			if not organisation_exists(post['organisation_name']):
                        	print("Creating the organisation..")
				try:
					umpackageid=post['umpackageid']
				except:
					umpackageid=2
                        	organisation = create_organisation(organisation_name=post['organisation_name'], organisation_desc=post['organisation_desc'], umpackageid=post['umpackageid'])
                        	#return redirect('organisation_table')


                		print("Creating the user..")
				org_admin_role_id=Role.objects.get(role_name="Organisational Manager").id
                		user = create_user_more(username=post['username'], email=post['email'], password=post['password'], first_name=post['first_name'], last_name=post['last_name'], roleid=org_admin_role_id, organisationid=organisation.id, date_of_birth=post['dateofbirth'], address=post['address'], gender=post['gender'], phone_number=post['phonenumber'], organisation_request=organisation)
                		if user:
					print("User created..")
                    			current_user_role = User_Roles.objects.get(user_userid=user.id).role_roleid;
                    			student_role = Role.objects.get(pk=6)

		
                    			state="The user " + user.username + " and organisation " + organisation.organisation_name + " has been created."
					return redirect('organisation_table')
                		else:
					print("Something went wrong when creating the user.. ")
					organisation.delete()
                    			state="The Username Creation failed. Contact us."
                    			data['state']=state
                    			return render(request, template_name, data)
			else:
				print("Organisation already exists..")
                                #Show message that the username/email address already exists in our database.
				state="The Organisation already exists.."
                                data['state']=state
                                return render(request, template_name, data)
                                #return redirect('organisation_table')
		else:
			print("Username already exists..")
                        #Show message that the username/email address already exists in our database.
                        state="The Username already exists.."
                        data['state']=state
                        return render(request, template_name, data)
                                #return redirect('organisation_table')

	return render(request, template_name, data)
    else:
        print("Not a staff.")
        state="You do not have permission to see this page."
        return render(request, template_name, {'state':state})


@login_required(login_url='/login/')
def organisation_update(request, pk, template_name='organisation/organisation_form.html'):
    if (request.user.is_staff==True):
	organisation = get_object_or_404(Organisation, pk=pk)
    	form = OrganisationForm(request.POST or None, instance=organisation)
    	if form.is_valid():
        	form.save()
        	return redirect('organisation_table')
    	return render(request, template_name, {'form':form})

    else:
        print("Not a staff.")
        state="You do not have permission to see this page."
        return render(request, template_name, {'state':state})

@login_required(login_url='/login/')
def organisation_delete(request, pk, template_name='organisation/organisation_confirm_delete.html'):
    if (request.user.is_staff==True):
	organisation = get_object_or_404(Organisation, pk=pk)
    	if request.method=='POST':
        	organisation.delete()
        	return redirect('organisation_table')
    	return render(request, template_name, {'object':organisation})
    else:
        print("Not a staff.")
        state="You do not have permission to see this page."
        return render(request, template_name, {'state':state})

####################################

###################################
# UMCloud_Package CRUD

class UMCloud_PackageForm(ModelForm):
    class Meta:
        model = UMCloud_Package
"""
@login_required(login_url='/login/')
def umpackage_list(request, template_name='organisation/umpackage_list.html'):
    umpackages = UMCloud_Package.objects.all()
    data = {}
    data['object_list'] = umpackages
    return render(request, template_name, data)
"""

@login_required(login_url='/login/')
def umpackage_table(request, template_name='organisation/umpackage_table.html'):
    if (request.user.is_staff==True):
    	umpackages = UMCloud_Package.objects.all()
    	data = {}
    	data['object_list'] = umpackages
    	umpackages_as_json = serializers.serialize('json', umpackages)
    	umpackages_as_json =json.loads(umpackages_as_json)
    	return render(request, template_name, {'data':data, 'umpackages_as_json':umpackages_as_json})
    else:
        print("Not a staff.")
        state="You do not have permission to see this page."
        return render(request, template_name, {'state':state})

@login_required(login_url='/login/')
def umpackage_create(request, template_name='organisation/umpackage_form.html'):
    if (request.user.is_staff==True):
	form = UMCloud_PackageForm(request.POST or None)
    	if form.is_valid():
        	form.save()
        	return redirect('umpackage_table')
    	return render(request, template_name, {'form':form})
    else:
        print("Not a staff.")
        state="You do not have permission to see this page."
        return render(request, template_name, {'state':state})

@login_required(login_url='/login/')
def umpackage_update(request, pk, template_name='organisation/umpackage_form.html'):
    if (request.user.is_staff==True):
	umpackage = get_object_or_404(UMCloud_Package, pk=pk)
    	form = UMCloud_PackageForm(request.POST or None, instance=umpackage)
    	if form.is_valid():
        	form.save()
        	return redirect('umpackage_table')
    	return render(request, template_name, {'form':form})
    else:
        print("Not a staff.")
        state="You do not have permission to see this page."
        return render(request, template_name, {'state':state})

@login_required(login_url='/login/')
def umpackage_delete(request, pk, template_name='organisation/umpackage_confirm_delete.html'):
    if (request.user.is_staff==True):
	umpackage = get_object_or_404(UMCloud_Package, pk=pk)
    	if request.method=='POST':
        	umpackage.delete()
        	return redirect('umpackage_table')
    	return render(request, template_name, {'object':umpackage})
    else:
        print("Not a staff.")
        state="You do not have permission to see this page."
        return render(request, template_name, {'state':state})

####################################


# Create your views here.
