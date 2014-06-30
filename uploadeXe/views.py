from django.shortcuts import render
# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response, redirect, get_object_or_404 #Added 404

import os 
#UMCloudDj.uploadeXe
from uploadeXe.models import Document
from uploadeXe.forms import ExeUploadForm
#Testing..
from django.forms import ModelForm
from organisation.models import Organisation
from organisation.models import UMCloud_Package
from organisation.models import User_Organisations
from school.models import School
from allclass.models import Allclass
from uploadeXe.models import Role
from uploadeXe.models import User_Roles
from django.contrib.auth.models import User
from django import forms


from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
import datetime
import time
import os
import urllib
import urllib2, base64, json
import hashlib
from django.conf import settings


def my_view(request):
	current_user = request.user.username
	print("Logged in username: " + current_user)
	return render_to_response(
        	'/base.html',
        	{'current_user': current_user, 'form': form},
        	context_instance=RequestContext(request)
	)

class DocumentForm(ModelForm):
    class Meta:
        model = Document
	fields = ('id','name','url','success','publisher','students')
	


@login_required(login_url='/login/')
def manage(request, template_name='myapp/manage.html'):
    documents = Document.objects.filter(publisher=request.user, success="YES")
    current_user = request.user.username
    courses_as_json = serializers.serialize('json', documents)
    courses_as_json = json.loads(courses_as_json)

    return render(request, template_name, {'courses_as_json':courses_as_json})

@login_required(login_url='/login/')
def edit(request, pk, template_name='myapp/update.html'):
    document = get_object_or_404(Document, pk=pk)
    form = DocumentForm(request.POST or None, instance=document)
    student_role = Role.objects.get(pk=6)
    allstudents=User.objects.filter(pk__in=User_Roles.objects.filter(role_roleid=student_role).values_list('user_userid', flat=True))
    print("All students:")
    print(allstudents)
    assignedstudents=document.students.all();
    print("Assigned Students:")
    print(assignedstudents);
    if form.is_valid():
	form.save()
	print("Going to update the assigned students..")
	studentidspicklist=request.POST.getlist('target')
	document.students.clear()
	assignedclear = document.students.all();
        for everystudentid in studentidspicklist:
                currentstudent=User.objects.get(pk=everystudentid)
                document.students.add(currentstudent)
                document.save()

	return redirect('manage')

    return render(request, template_name, {'form':form, 'all_students':allstudents,'assigned_students':assignedstudents})

@login_required(login_url='/login/')
def new(request, template_name='myapp/new.html'):
    # Handle file upload
    print("Current User logged in is: " + request.user.email)

    teacher_role = Role.objects.get(pk=5)
    student_role = Role.objects.get(pk=6)

    teachers = User.objects.filter(pk__in=User_Roles.objects.filter(role_roleid=teacher_role).values_list('user_userid', flat=True))

    students = User.objects.filter(pk__in=User_Roles.objects.filter(role_roleid=student_role).values_list('user_userid', flat=True))
    data = {}
    data['teacher_list'] = teachers
    data['student_list'] = students

    current_user = request.user.username
    # Render list page with the documents and the form
    return render_to_response(
        template_name,
        {'student_list':data['student_list'],'current_user': current_user},
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login/')
def list(request, template_name='myapp/list.html'):
    # Handle file upload
    print("Current User logged in is: " + request.user.email)

    teacher_role = Role.objects.get(pk=5)
    student_role = Role.objects.get(pk=6)

    teachers = User.objects.filter(pk__in=User_Roles.objects.filter(role_roleid=teacher_role).values_list('user_userid', flat=True))

    students = User.objects.filter(pk__in=User_Roles.objects.filter(role_roleid=student_role).values_list('user_userid', flat=True))
    data = {}
    data['teacher_list'] = teachers
    data['student_list'] = students

    if request.method == 'POST':
	post = request.POST;
        form = ExeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(exefile = request.FILES['exefile'])
            
	    teacher_role = Role.objects.get(pk=5)
    	    student_role = Role.objects.get(pk=6)
    	    teachers = User.objects.filter(pk__in=User_Roles.objects.filter(role_roleid=teacher_role).values_list('user_userid', flat=True))
    	    students = User.objects.filter(pk__in=User_Roles.objects.filter(role_roleid=student_role).values_list('user_userid', flat=True))
    	    data = {}
            data['teacher_list'] = teachers
    	    data['student_list'] = students
	    studentidspicklist=post.getlist('target')
            print("students selected from picklist:")
            print(studentidspicklist)

	    uid = str(getattr(newdoc, 'exefile'))
	    print("File name to upload:")
	    print(uid)
	    appLocation = (os.path.dirname(os.path.realpath(__file__)))
            #Get the file and run eXe command 
  	    #Get url / path
	    setattr (newdoc, 'url', 'bull')
	    setattr (newdoc, 'publisher', request.user)
            newdoc.save()

            for everystudentid in studentidspicklist:
		print("Looping student:")
                print(everystudentid)
                currentstudent=User.objects.get(pk=everystudentid)
                newdoc.students.add(currentstudent)
                newdoc.save() 
 
	    os.system("echo Current location:")
            serverlocation=os.system("pwd")
	    mainappstring = "/UMCloudDj/"
	    uid = str(getattr(newdoc, 'exefile'))
	    print("File saved as: ")
            print(uid)
	    #elphash = hashlib.md5(open(serverlocation + mainappstring + settings.MEDIA_URL + uid).read()).hexdigest()
	    #print("elp hash:")
	    #print(elphash)
	    print(settings.MEDIA_URL)
	    unid = uid.split('.um.')[-2]
	    unid = unid.split('/')[-1]  #Unique id here.
            print("Unique id:")
            print (unid)
	    setattr(newdoc, 'uid', unid)
	    #os.system('tree')
	    print("Possible command: ")
	    print('exe_do -s ustadMobileTestMode=True -x ustadmobile ' + appLocation + '/../UMCloudDj/media/' + uid + ' ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid )
	    if os.system('exe_do -s ustadMobileTestMode=True -x ustadmobile ' + appLocation + '/../UMCloudDj/media/' + uid + ' ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid ) == 0: # If command ran successfully,
	    	uidwe = uid.split('.um.')[-1]
	    	uidwe = uidwe.split('.elp')[-2]
	    	print("Folder name: " + uidwe)
	    	if os.system('cp ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadpkg_html5.xml ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '_ustadpkg_html5.xml' ) == 0: #ie if command got executed in success
            		setattr(newdoc, 'url', "cow")
	    		newdoc.save()
            		setattr(newdoc, 'success', "YES")
	    		courseURL = '/media/eXeExport' + '/' + unid + '/' + uidwe + '/' + 'deviceframe.html'
	    		setattr(newdoc, 'url', courseURL)
 	    		setattr(newdoc, 'name', uidwe)
	    		setattr(newdoc, 'publisher', request.user)
	    		newdoc.save()
			print("Starting grunt process..")
			os.system('mv ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js ' +  appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js.origi')

			os.system('cp ' + appLocation + '/../UMCloudDj/media/gruntConfig/Gruntfile.js ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/')
			os.system('cp ' + appLocation + '/../UMCloudDj/media/gruntConfig/package.json ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/')
			os.system('cp ' + appLocation + '/../UMCloudDj/media/gruntConfig/ustadmobile-settings.js ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js' )
			os.system('cp ' + appLocation + '/../UMCloudDj/media/gruntConfig/umpassword.html ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/umpassword.html')
			os.system('cd ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/')
			print ('Trying this: ' + 'npm install grunt-contrib-qunit --save-dev -g --prefix ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/')
			os.system('npm install grunt-contrib-qunit --save-dev -g --prefix ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/')
			os.system('mv ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/lib/node_modules/ '+ appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/')
			print('Trying this: ' + 'grunt --base ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ --gruntfile ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/Gruntfile.js')
			
			#Not running grunt until eXe changes are made - VarunaSingh 180220141732
			if os.system('grunt --base ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ --gruntfile ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/Gruntfile.js'):
			    os.system('mv ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js.origi ' +  appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js')
			    print("Grunt ran successfully. ")
			else:
			    #Grunt run failed. 
			    print("Unable to run grunt. Test failed. ")
			    os.system('mv ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js.origi ' +  appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js')
			    setattr(newdoc, 'success', "NO")


			#When testing is disabled ( Running until eXe changes are made - VarunaSingh 180220141732 - edit on 250220141323)
			#os.system('mv ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js.origi ' +  appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js') #Comment this when you have eXe changes, etc.

			#If you ever do an if condition for installing grunt on the local course..
			#else:
			#    print("Unable to install grunt for this course.. Fail.")
			#    os.system('mv ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js.origi ' +  appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js')
		    
					
	    	else:
			#Couldn't copy html file xml to main directoy. Something went wrong in the exe export
			setattr(newdoc, 'success', "NO")
	    		newdoc.save()
	        	# Redirect to the document list after POST
                	#return HttpResponseRedirect(reverse('uploadeXe.views.list'))
	    else:
		    #Exe didn't run. exe_do : something went wrong in eXe.
		    setattr(newdoc, 'success', "NO")

	    #Saving to database.
            newdoc.save()
	
	#form is valid (upload file form)
	# Redirect to the document list after POST
        return HttpResponseRedirect(reverse('uploadeXe.views.list'))

    else:
       #Form isn't POST. 
       form = ExeUploadForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.filter(publisher=request.user, success="YES")
    current_user = request.user.username

    # Render list page with the documents and the form
    return render_to_response(
        template_name,
        {'student_list':data['student_list'] ,'documents': documents, 'form': form, 'current_user': current_user},
        context_instance=RequestContext(request)
    )

# Create your views here.
