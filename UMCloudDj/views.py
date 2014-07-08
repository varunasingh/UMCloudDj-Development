from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, redirect, get_object_or_404 #Added 404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import auth
from django.template import RequestContext
#from uploadeXe.models import Document
from uploadeXe.models import Package as Document
from uploadeXe.models import Ustadmobiletest

#Testing..
from uploadeXe.models import Role
from uploadeXe.models import User_Roles
from django.forms import ModelForm
from organisation.models import Organisation
from organisation.models import UMCloud_Package
from organisation.models import User_Organisations
from users.models import UserProfile
from django import forms

from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
import datetime
import time
import os
#import urllib, json
import urllib
import urllib2, base64, json
import glob #For file ^VS 130420141454
#from UMCloudDj.models import Ustadmobiletest
from uploadeXe.models import Ustadmobiletest
#from django.utils import simplejson
from django.conf import settings

#UMCloudDj.uploadeXe

###################################
# Role CRUD

class RoleForm(ModelForm):
    class Meta:
        model = Role
@login_required(login_url='/login/')
def role_list(request, template_name='role/role_list.html'):
    roles = Role.objects.all()
    data = {}
    data['object_list'] = roles
    return render(request, template_name, data)

@login_required(login_url='/login/')
def role_table(request, template_name='role/role_table.html'):
    roles = Role.objects.all()
    data = {}
    data['object_list'] = roles
    roles_as_json = serializers.serialize('json', roles)
    roles_as_json =json.loads(roles_as_json)

    return render(request, template_name, {'data':data, 'roles_as_json':roles_as_json})

@login_required(login_url='/login/')
def role_dynatable(request, template_name='table/dynatable.html'):
    roles=Role.objects.all()
    data={}
    data['object_list']=roles;
    data_as_json=serializers.serialize('json', roles)
    data_as_json=json.loads(data_as_json)
    pagetitle="UstadMobile Roles"
    newtypeid="newrole"
    newtypelink="/rolenew/"
    tabletypeid="tblroles"
    table_headers_html=[]
    table_headers_name=[]
    table_headers_html.append("pk")
    table_headers_name.append("ID")
    #table_headers_html.append("model");
    table_headers_html.append("fields.role_name")
    table_headers_name.append("Role Name")
    table_headers_html.append("fields.role_desc")
    table_headers_name.append("Role Desc")
    table_headers_html = zip(table_headers_html, table_headers_name)
    logicpopulation = '{"pk":"{{c.pk}}","model":"{{c.model}}", "role_name":"{{c.fields.role_name}}","role_desc":"{{c.fields.role_desc}}"}{% if not forloop.last %},{% endif %}'

    return render(request, template_name, {'data':data, 'data_as_json':data_as_json, 'table_headers_html':table_headers_html, 'pagetitle':pagetitle, 'newtypeid':newtypeid, 'tabletypeid':tabletypeid, 'newtypelink':newtypelink, 'logicpopulation':logicpopulation}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def role_create(request, template_name='role/role_form.html'):
    form = RoleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('role_table')
    return render(request, template_name, {'form':form})

@login_required(login_url='/login/')
def role_update(request, pk, template_name='role/role_form.html'):
    role = get_object_or_404(Role, pk=pk)
    form = RoleForm(request.POST or None, instance=role)
    if form.is_valid():
        form.save()
        return redirect('role_table')
    return render(request, template_name, {'form':form})

@login_required(login_url='/login/')
def role_delete(request, pk, template_name='role/role_confirm_delete.html'):
    role = get_object_or_404(Role, pk=pk)    
    if request.method=='POST':
        role.delete()
        return redirect('role_table')
    return render(request, template_name, {'object':role})

#@login_required(login_url='/login/')
####################################


###################################
# USER CRUD


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta:
        model = User
	fields = ('username', 'email', 'first_name', 'last_name', 'is_active')
	widgets = {
        #'password': forms.PasswordInput(),
    	}

    def save(self, commit=True):
    	user = super(UserForm, self).save(commit=False)
	newpassword = self.cleaned_data["password"]
	if newpassword:
		print("New password specified")
    		user.set_password(self.cleaned_data["password"])
	else:
		print("password not specified.")
    	if commit:
		print("commit.")
		user.save()
    	return user

@login_required(login_url='/login/')
def user_list(request, template_name='user/user_list.html'):
    users = User.objects.all()
    user_roles = []
    user_organisations = []
    for user in users:
	role = User_Roles.objects.get(user_userid=user).role_roleid
 	print (role)
	organisation = User_Organisations.objects.get(user_userid=user).organisation_organisationid
	print("For " + user.email + "Role: " + role.role_name + " of Organisation: " + organisation.organisation_name)
	user_roles.append(role)
	user_organisations.append(organisation)

    data = {}
    data['object_list'] = zip(users,user_roles, user_organisations)
    data['role_list'] = user_roles
    data['organisation_list'] = user_organisations
    
    return render(request, template_name, data)

@login_required(login_url='/login/')
def user_table(request, template_name='user/user_table.html'):
    users = User.objects.all()
    user_roles = []
    user_organisations = []
    for user in users:
	role = User_Roles.objects.get(user_userid=user).role_roleid
	organisation = User_Organisations.objects.get(user_userid=user).organisation_organisationid
	user_roles.append(role)
	user_organisations.append(organisation)
    data = {}
    data['object_list'] = zip(users,user_roles,user_organisations)
    data['role_list'] = user_roles
    data['organisation_list'] = user_organisations
    users_as_json = serializers.serialize('json', users)

    users_as_json =json.loads(users_as_json)
    return render(request, template_name, {'data':data, 'users_as_json':users_as_json})


@login_required(login_url='/login/')
def user_create(request, template_name='user/user_create.html'):
    form = UserForm(request.POST or None)
    roles = Role.objects.all()
    organisations = Organisation.objects.all()
    data = {}
    data['object_list'] = roles
    data['organisation_list'] = organisations

    if request.method == 'POST':
	post = request.POST;
	if not user_exists(post['email']):
		print("Creating the user..")
        	user = create_user_more(username=post['username'], email=post['email'], password=post['password'], first_name=post['first_name'], last_name=post['last_name'], roleid=post['role'], organisationid=post['organisation'])
		return redirect('user_table')
    	else:
        	#Show message that the username/email address already exists in our database.
        	return redirect('user_table')

    return render(request, template_name, data)

	
@login_required(login_url='/login/')
def user_update(request, pk, template_name='user/user_update.html'):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    form.fields['username'].widget.attrs['readonly']=True

    if form.is_valid():
        form.save()
        return redirect('user_table')
    return render(request, template_name, {'form':form})

@login_required(login_url='/login/')
def user_delete(request, pk, template_name='user/user_confirm_delete.html'):
    user = get_object_or_404(User, pk=pk)
    if request.method=='POST':
        user.delete()
        return redirect('user_table')
    return render(request, template_name, {'object':user})

####################################


@login_required(login_url='/login/')
def get_report_statements(request, onfail='/statementsreports'):
	print("Getting variables..")
        date_since = request.POST['since_1_alt']
        date_until = request.POST['until_1_alt']
        #activity = request.POST['activity']
        print("Got variables. They are: ")
        print(date_since)
        print(date_until)
        #Code for report making here.
	umlrs = settings.UMLRS
        #lrs_endpoint = umlrs + "?" + "&since=" + date_since + "&until=" + date_until + "&activity=" + activity
        lrs_endpoint = umlrs + "?" + "&since=" + date_since + "&until=" + date_until
        #BASIC AUTHENTICATION
        username="testuser"
        #username = request.POST['username']
        password="testpassword"
        #password = request.POST['password']
        #Username and password to be in sync or already known by Django. For now using the only test account on the TinCan LRS.

        req = urllib2.Request(lrs_endpoint)
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        req.add_header("Authorization", "Basic %s" % base64string)
        req.add_header("X-Experience-API-Version", "1.0.1")
        #GETTING JSON String from URL
        jdata_string = urllib2.urlopen(req).read() #gets string..
        jdata_string = jdata_string.replace('en-US', 'en_US')
        jdata = json.dumps(jdata_string) #puts in a JSON string  #JSON encoding
        data = json.loads(jdata_string) #puts in a JSON #JSON decoding # to a python dictionary
        print(data['statements'])
        print("Going one by one..")
        statements_as_json = data['statements']

        return render_to_response("report_statements.html", {'date_since':date_since , 'date_until':date_until , 'data':data , 'lrs_endpoint':lrs_endpoint ,'statements_as_json':statements_as_json }, context_instance=RequestContext(request))





@login_required(login_url='/login/')
def get_report_zambia(request, onfail='/mcqreports'):
    	print("Getting variables..")
    	date_since = request.POST['since_1_alt']
    	date_until = request.POST['until_1_alt']
    	#activity = request.POST['activity']
    	print("Got variables. They are: ")
    	print(date_since)
    	print(date_until)
	#Code for report making here.
	umlrs = settings.UMLRS
	#lrs_endpoint = umlrs + "?" + "&since=" + date_since + "&until=" + date_until + "&activity=" + activity
	lrs_endpoint = umlrs + "?" + "&since=" + date_since + "&until=" + date_until
	#BASIC AUTHENTICATION
        username="testuser"
	#username = request.POST['username']
        password="testpassword"
	#password = request.POST['password']
	#Username and password to be in sync or already known by Django. For now using the only test account on the TinCan LRS.

        req = urllib2.Request(lrs_endpoint)
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        req.add_header("Authorization", "Basic %s" % base64string)
        req.add_header("X-Experience-API-Version", "1.0.1")
	#GETTING JSON String from URL
        jdata_string = urllib2.urlopen(req).read() #gets string..
	jdata_string = jdata_string.replace('en-US', 'en_US')
        jdata = json.dumps(jdata_string) #puts in a JSON string  #JSON encoding
        data = json.loads(jdata_string) #puts in a JSON #JSON decoding # to a python dictionary
	print(data['statements'])
	print("Going one by one..")
	statements_as_json = data['statements']
	##play with the data now.

    	return render_to_response("report_zambia.html", {'date_since':date_since , 'date_until':date_until , 'data':data , 'lrs_endpoint':lrs_endpoint ,'statements_as_json':statements_as_json }, context_instance=RequestContext(request))

def report_selection_view(request):
	c = {}
        c.update(csrf(request))
        #return render_to_response('report_selection.html', c) #Somehow messes with the css and includes of scripts. This is not such sensitive data, so leaving.
	return render(request, "report_selection.html")

def report_statements_view(request):
	c = {}
	c.update(csrf(request))
	return render(request, "report_statements_selection.html")

def elptestresults_selection_view(request):
	c= {}
	c.update(csrf(request))
	return render(request, "elptestresults_selection.html")

def apptestresults_selection_view(request):
	c = {}
	c.update(csrf(request))
	return render(request, "apptestresults_selection.html")


@csrf_exempt
def sendtestlog_view(request):
	print("Receiving the test logs..")
        unittestlogs = 'hiii'

	unittestlogs = request.POST.get('appunittestoutput')
	#print("The unit test logs recieved is: " + unittestlogs)
	
	username = request.POST.get('username');
	password = request.POST.get('password');

	os.system("pwd")

	with open ("umpassword.txt", "r") as myfile:
    		umpassword=myfile.read().replace('\n', '')

	if ( username == "test" and password == umpassword ):
		#process with inserting data into table.	
		print("The username and password matches! The unit test output recieved is: " + unittestlogs)
		unittestlogs = unittestlogs.strip()
	
		for i, phrase in enumerate(unittestlogs.split('new|')):
			if phrase != '':
   				print('phrase #%d: %s' % (i+1,phrase))
				utestfields = phrase.split('|')
				
				
				
				##Code for putting in database goes here.	
				newunittestresult = Ustadmobiletest(name = utestfields[0] )
				setattr (newunittestresult, 'result', utestfields[1] )
				setattr (newunittestresult, 'runtime', utestfields[2] )
  				setattr (newunittestresult, 'dategroup',  utestfields[3])
				setattr (newunittestresult, 'platform', utestfields[4])
				setattr (newunittestresult, 'ustad_version', utestfields[5])
				newunittestresult.save()
			else:
				print('one log is empty: no info. Proceeding.')
	
		context_instance=RequestContext(request)
        	response = render_to_response("sendtestlog.html", {'appunittestoutput': unittestlogs}, context_instance=RequestContext(request))
        	return response

	else:
		#Return a bad signal. 
		print("The username and password is incorrect. Sorry bro..")
		return render_to_response("invalid.html", {'invalid': invalid}, context_instance=RequestContext(request))
	
@csrf_exempt
def checklogin_view(request):
        print("Checking log in details..")

        if request.method == 'POST':
                print 'POST request recieved.'
                print 'Login request coming from outside (eXe)'
                username = request.POST.get('username');
                password = request.POST.get('password');
                print "The username is"
                print username

                #Code for Authenticating the user
	
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user is not None:
			authresponse = HttpResponse(status=200)
			authresponse.write("User: " + username + " authentication a success.")
			return authresponse
		else:
			authresponse = HttpResponse(status=403)
			authresponse.write("User: " + username + " authentication failed.")
			return authresponse

@csrf_exempt
def getassignedcourseids_view(request):
        print("Checking log in details..")

        if request.method == 'POST':
                print 'POST request recieved.'
                print 'Login request coming from outside (eXe)'
                username = request.POST.get('username',False);
                password = request.POST.get('password', False);
                print "The username is"
                print username

                #Code for Authenticating the user

                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user is not None:
			#Check and get list of courses..
			assigned_courses=Document.objects.filter(students=user)
			assigned_course_ids=[]
			if assigned_courses:
				print("assigned_courses:")
				print(assigned_courses)
				for everycourse in assigned_courses:
					assigned_course_ids.append(everycourse.id)
				print("ASSIGNED COURSE IS:")
				print(assigned_course_ids)
                        	authresponse = HttpResponse(status=200)
				authresponse.write("Courses found for user: " + username)
				authresponse['assigned_course_ids']=assigned_course_ids
                        	return authresponse
			else:
				authresponse = HttpResponse(status=404)
				authresponse['assigned_course_ids']=assigned_course_ids
				authresponse.write("No courses found for username: " + username)
				return authresponse
                else:
                        authresponse = HttpResponse(status=403)
                        authresponse.write("User: " + username + " authentication failed.")
                        return authresponse
	else:
		authresponse = HttpResponse(status=500)
		authresponse.write("Not a POST request. Assigned Course IDs retrival failed.")
		return authresponse



@csrf_exempt
def sendelpfile_view(request):
	print("Receiving the elp file..")

	if request.method == 'POST':
		print 'POST request recieved.'
		print 'Login request coming from outside (eXe)'
		username = request.POST.get('username');
		password = request.POST.get('password');
		print "The username is" 
		print username 
		print "The file: " 
		print request.FILES

		#Code for Authenticating the user

		user = authenticate(username=request.POST['username'], password=request.POST['password'])
    		if user is not None:
        		#We Sign the user..
			login(request, user)

			#Try to save the file
			newdoc = Document(exefile = request.FILES['exeuploadelp'])
		        uid = str(getattr(newdoc, 'exefile'))
            		print("File name to upload:")
            		print(uid)
            		appLocation = (os.path.dirname(os.path.realpath(__file__)))
            		#Get the file and run eXe command
            		#Get url / path
            		setattr (newdoc, 'url', 'bull')
			setattr (newdoc, 'publisher', request.user)
            		newdoc.save()
            		os.system("echo Current location:")
            		os.system("pwd")
            		uid = str(getattr(newdoc, 'exefile'))
            		print("File saved as: ")
            		print(uid)
            		unid = uid.split('.um.')[-2]
            		unid = unid.split('/')[-1]  #Unique id here.
            		print("Unique id:")
            		print (unid)

			#Code for elp to ustadmobile export

			setattr(newdoc, 'uid', unid)
			#os.system('tree')
            		print("Possible command: ")
            		print('exe_do -s ustadMobileTestMode=True -x ustadmobile ' + appLocation + '/../UMCloudDj/media/' + uid + ' ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid )

			elpfile=appLocation + '/../UMCloudDj/media/' + uid
			elpfilehandle = open(elpfile, 'rb')
            		elpzipfile = zipfile.ZipFile(elpfilehandle)
            		for name in elpzipfile.namelist():
                		if name.find('contentv3.xml') != -1:
                    			elpxmlfile=elpzipfile.open(name)
                    			elpxmlfilecontents=elpxmlfile.read()
                    			elpxml=minidom.parseString(elpxmlfilecontents)
                    			dictionarylist=elpxml.getElementsByTagName('dictionary')
                    			stringlist=elpxml.getElementsByTagName('string')
                    			print("/////////////////////////////////////////////////")
                    			elpid="replacemewithxmldata"
                    			setattr(newdoc, 'elpid', elpid)
                    			#print(dictionarylist[0].attributes['string'].value)



            		if os.system('exe_do -s ustadMobileTestMode=True -x ustadmobile ' + appLocation + '/../UMCloudDj/media/' + uid + ' ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid ) == 0: # If command ran successfully,
                		uidwe = uid.split('.um.')[-1]
                		uidwe = uidwe.split('.elp')[-2]
                		print("Folder name: " + uidwe)
                		if os.system('cp ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadpkg_html5.xml ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '_ustadpkg_html5.xml' ) == 0: #ie if command got executed in success
                        		setattr(newdoc, 'url', "cow")
                        		newdoc.save()
                        		setattr(newdoc, 'success', "YES") 	#Might need to do this AFTER the course has finished testing..10/04/20141339
                        		courseURL = '/media/eXeExport' + '/' + unid + '/' + uidwe + '/' + 'deviceframe.html'
                        		setattr(newdoc, 'url', courseURL)
                        		setattr(newdoc, 'name', uidwe)
                        		setattr(newdoc, 'publisher', request.user)
                        		newdoc.save()
                        		print("Starting grunt process..")


					#Start..
					#""" Start commenting if Testing doesn' t work with eXe and server's exe_do

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
						
						#Return upload and processing success with Course ID returned
						#uploadresponse = HttpResponse(status=200)
						print "Course ID: "
						print getattr(newdoc, 'id')
						#uploadresponse['courseid'] = getattr(newdoc, 'id')
						#uploadresponse['coursename'] = getattr(newdoc, 'name')
						#return uploadresponse

                        		else:
                            			#Grunt run failed.
                            			print("Unable to run grunt. Test failed. ")
                            			os.system('mv ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js.origi ' +  appLocation + '/../UMCloudDj/media/eXeExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js')
                            			setattr(newdoc, 'success', "NO")

						uploadresponse = HttpResponse(status=500)
						uploadresponse.write("Course testing failed but uploaded")
						uploadresponse['error'] = "Grunt test failed"
						return uploadresponse



					#""" End commenting if Testing doesn' t work with eXe and server's exe_do
					#End.

               			else:
                       			#Couldn't copy html file xml to main directoy. Something went wrong in the exe export
                       			setattr(newdoc, 'success', "NO")
                       			newdoc.save()
				
					uploadresponse = HttpResponse(status=500)
                                        uploadresponse.write("Exe Export failed but uploaded")
                                        uploadresponse['error'] = "Exe export failed"
                                        return uploadresponse

          		else:
                    		#Exe didn't run. exe_do : something went wrong in eXe.
                    		setattr(newdoc, 'success', "NO")
				
				uploadresponse = HttpResponse(status=500)
                                uploadresponse.write("Exe Export faild but uploaded")
                                uploadresponse['error'] = "Exe export failed to start"
                                return uploadresponse


				
			
            		#Saving to database.
            		newdoc.save()
			#Return upload and processing success with Course ID returned
                        uploadresponse = HttpResponse(status=200)
                        print "Course ID: "
                        print getattr(newdoc, 'id')
                        uploadresponse['courseid'] = getattr(newdoc, 'id')
                        uploadresponse['coursename'] = getattr(newdoc, 'name')
                        return uploadresponse



			
			#response = HttpResponse("LOGIN A SUCCESS")
			#return response
    		else:
        		#Show a "incorrect credentials" message
			uploadresponse = HttpResponse(status=403)
			uploadresponse.write("LOGIN FAILED. USERNAME and PASSWORD DO NOT MATCH. AUTHENTICATION FAILURE")
			return uploadresponse

			#response = HttpResponse("LOGIN FAILED")
			#return response


		#If authenticated, code for getting the file uploaded and saving it.

	else:
		print 'Not a POST request';
		
		uploadresponse = HttpResponse(status=500)
		uploadresponse.write("Request is not POST")
		uploadresponse['error'] = "Request is not POST"
		return uploadresponse

		#response2 = HttpResponse("NOT a POST request")
        	#return response2
	
@login_required(login_url='/login/')
def testelpfiles_view(request):
	appLocation = (os.path.dirname(os.path.realpath(__file__)))
	#Log start time here..
	cmdStartTime = datetime.datetime.today()
	print ("The Start time is: " + str(cmdStartTime))
	#Code here..
	print "hello there"
	for dir in os.listdir(appLocation + '/../UMCloudDj/media/eXeTestElp/'):
		print dir
	print "glob"
	print glob.glob(appLocation + '/../UMCloudDj/media/eXeTestElp/*elp');
	testelpfiles = glob.glob(appLocation + '/../UMCloudDj/media/eXeTestElp/*elp');
	for testelp in testelpfiles:
		print ("[testelpfiles]: FOR LOOP BEGINS. FILE: " + testelp);
		#unid = testelp.split('.um.')[-2] #OLD
		unid = testelp.split('.elp')[-2]
		unid = unid.split('/')[-1]
		print("[testelpfiles] unid: " + unid)
		
		#if os.system('exe_do -x ustadmobile ' + appLocation + '/../UMCloudDj/media/eXeTestElp/' + testelp + ' ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid ) == 0: # If command ran successfully,
		elpfile=appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid
		elpfilehandle = open(elpfile, 'rb')
            	elpzipfile = zipfile.ZipFile(elpfilehandle)
            	for name in elpzipfile.namelist():
                	if name.find('contentv3.xml') != -1:
                    		elpxmlfile=elpzipfile.open(name)
                    		elpxmlfilecontents=elpxmlfile.read()
                    		elpxml=minidom.parseString(elpxmlfilecontents)
                    		dictionarylist=elpxml.getElementsByTagName('dictionary')
                    		stringlist=elpxml.getElementsByTagName('string')
                    		print("/////////////////////////////////////////////////////////////")
                    		elpid="replacemewithxmldata"
                    		setattr(newdoc, 'elpid', elpid)
                    		#print(dictionarylist[0].attributes['string'].value)

		if os.system('exe_do -x ustadmobile ' + testelp + ' ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid ) == 0: # If command ran successfully,
			print("[testelpfiles] Exe Exported successfully..")
			uidwe = testelp.split('.um.')[-1]
    			uidwe = uidwe.split('.elp')[-2]
			print("[testelpfiles] uidwe: " + uidwe)
			print("[testelpfiles] Starting grunt process..")
                        os.system('mv ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js ' +  appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js.origi')
                        os.system('cp ' + appLocation + '/../UMCloudDj/media/gruntConfig/Gruntfile.js ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/')
                        os.system('cp ' + appLocation + '/../UMCloudDj/media/gruntConfig/package.json ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/')
                        os.system('cp ' + appLocation + '/../UMCloudDj/media/gruntConfig/ustadmobile-settings.js ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js' )
                        os.system('cp ' + appLocation + '/../UMCloudDj/media/gruntConfig/umpassword.html ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/umpassword.html')
                        os.system('cd ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/')
                        print ('Trying this: ' + 'npm install grunt-contrib-qunit --save-dev -g --prefix ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/')
                        os.system('npm install grunt-contrib-qunit --save-dev -g --prefix ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/')
                        os.system('mv ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/lib/node_modules/ '+ appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/')
                        print('Trying this: ' + 'grunt --base ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/ --gruntfile ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/Gruntfile.js')
			
			#Running grunt..
                        if os.system('grunt --base ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/ --gruntfile ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/Gruntfile.js'):
				os.system('mv ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js.origi ' +  appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js')
		    		print("Grunt ran successfully. ")
			else:
		    		#Grunt run failed. 
		    		print("Unable to run grunt. Test failed. ")
		    		os.system('mv ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js.origi ' +  appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid + '/' + uidwe + '/ustadmobile-settings.js')

		else:
			#Exe didn't run. exe_do : something went wrong in eXe.
			print("[testelpfiles] exe_do did not run.")

	cmdEndTime = datetime.datetime.today()

	matchedCourseTestResults = Ustadmobiletest.objects.filter(dategroup='grunt', pub_date__gte=cmdStartTime, pub_date__lte=cmdEndTime)
	if matchedCourseTestResults:
		print("[testelpfiles] Test results exists")
		#for matchedCourseResult in matchedCourseTestResults:
			#print ("[testelpfiles]: Result: ")
			#print (matchedCourseResult.name)
		
		matchedCourseResultList = list(matchedCourseTestResults)
		#jdata = json.dumps(matchedCourseResultList)
		#jdata = json.dumps(list(matchedCourseTestResults).values())
		#print (jdata)
		success="success"

		#context_instance=RequestContext(request)
                #response = render_to_response("testelpfiles-result.html", {'result': success}, context_instance=RequestContext(request))
                #return response

	else:
		print ("[testelpfiles] No results exists.")
		failed="fail"
		#context_instance=RequestContext(request)
                #response = render_to_response("testelpfiles-result.html", {'result': failed} , context_instance=RequestContext(request))
                #return response
	success="success"
	failed="fail"
	context_instance=RequestContext(request)
        response = render_to_response("testelpfiles-result.html", {'result': success}, context_instance=RequestContext(request))
        return response


def testresults_function(typeofdata, date_from, date_to):
	today = datetime.datetime.today()
	yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
	if typeofdata == "elp":
		matchedCourseTestResults = (Ustadmobiletest.objects.filter(dategroup='grunt', pub_date__gte=date_from, pub_date__lte=date_to).values('id', 'name', 'dategroup', 'pub_date', 'result'))
	if typeofdata == "app":
		matchedCourseTestResults = (Ustadmobiletest.objects.filter(pub_date__gte=date_from, pub_date__lte=date_to).exclude(dategroup='grunt').values('id', 'name', 'dategroup', 'pub_date', 'result','platform','ustad_version','runtime'))
	return matchedCourseTestResults

@login_required(login_url='/login/')
def showappunittestresults_view(request):
	today = datetime.datetime.today()
        yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
	if request.method == 'POST':
		print("POST request to get UstadMobile App unit test results")
		print("Getting variables..")
                date_since = request.POST['since_1_alt']
                date_until = request.POST['until_1_alt']
                print("Got variables. They are: ")
                print(date_since)
                print(date_until)

		#json_object = testresults_function("app", yesterday, today)
		json_object = testresults_function("app", date_since, date_until)

        	response =[]
        	for ja in json_object:
                	jatime = ja['pub_date']
                	jatime=str(jatime)
                	response.append({'id':ja['id'], 'name':ja['name'], 'dategroup':ja['dategroup'],'pub_date':jatime,'result':ja['result'], 'platform':ja['platform'], 'ustad_version':ja['ustad_version'], 'runtime':ja['runtime']})
	        return render_to_response("apptestresults.html", {'data': response, 'date_since':date_since , 'date_until':date_until}, context_instance=RequestContext(request))

        if request.method == 'GET':
                print("Not a POST response")
                return render_to_response("apptestresults.html", {'data': ''}, context_instance=RequestContext(request))



        json_object = testresults_function("app", yesterday, today)

        response =[]    
        for ja in json_object:
                jatime = ja['pub_date']
                jatime=str(jatime)
                response.append({'id':ja['id'], 'name':ja['name'], 'dategroup':ja['dategroup'],'pub_date':jatime,'result':ja['result']})

        return render_to_response("apptestresults.html", {'data': response}, context_instance=RequestContext(request))
	
@login_required(login_url='/login/')
def showelptestresults_view(request):
	today = datetime.datetime.today()
        yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
	if request.method == 'POST':
		print("POST request to get elp test results..")
		print("Getting variables..")
        	date_since = request.POST['since_1_alt']
        	date_until = request.POST['until_1_alt']
        	print("Got variables. They are: ")
        	print(date_since)
        	print(date_until)

		#json_object = testresults_function("elp", yesterday, today)

		json_object = testresults_function("elp", date_since, date_until)

		response =[]	
		for ja in json_object:
			jatime = ja['pub_date']
			jatime=str(jatime)
			response.append({'id':ja['id'], 'name':ja['name'], 'dategroup':ja['dategroup'],'pub_date':jatime,'result':ja['result']})
	
		return render_to_response("elptestresults.html", {'data': response, 'date_since':date_since , 'date_until':date_until}, context_instance=RequestContext(request))

	if request.method == 'GET':
		print("Not a POST response")
		return render_to_response("elptestresults.html", {'data': ''}, context_instance=RequestContext(request))
		

def getcourse_view(request):
	courseid = request.GET.get('id')
	print("External request of public course..")

	try:
		matchedCourse = Document.objects.filter(id=str(courseid)).get(id=str(courseid))
        	if matchedCourse:
                	print("Course exists!")
                	print("The unique folder for course id: " + courseid + " is: " + matchedCourse.uid + "/" + matchedCourse.name)
                	coursefolder = matchedCourse.uid + "/" + matchedCourse.name
                	xmlDownload = coursefolder + "_ustadpkg_html5.xml"
                	data = {
                        	'folder' : coursefolder,
                        	'xmlDownload' : xmlDownload
                	}
                #response =  HttpResponse(status=200)
                	response = HttpResponse("folder:" + coursefolder)
                	response = HttpResponse("xmlDownload:" + xmlDownload)
                	response = render_to_response("getcourse.html", {'coursefolder': coursefolder, 'xmlDownload': xmlDownload}, context_instance=RequestContext(request))
                	response['folder'] = coursefolder
                	response['xmlDownload'] = xmlDownload
                	return response
		else:
                	response2 =  HttpResponse(status=403)
                	print("Sorry, a course of that ID was not found globally")
			response2.write("folder:na")
                	return response2

	except Document.DoesNotExist, e:
                response2 =  HttpResponse(status=403)
                print("Sorry, a course of that ID was not found globally")
                response2 = HttpResponse(status=403)
		response2.write("folder:na")
                return response2
	
	return redirect("/")

def register_view(request, ):
	c = {}
	c.update(csrf(request))
	#return render_to_response('signup.html', c)
	return render_to_response('user/user_create_website.html', c, context_instance=RequestContext(request))

def my_view(request):
        current_user = request.user.username
        print("Logged in username: " + current_user)
        return render_to_response(
                '/base.html',
                {'current_user': current_user, 'form': form},
                context_instance=RequestContext(request)
        )

def loginview(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c, context_instance=RequestContext(request))

#This is the def that will authenticate the user over the umcloud website
def auth_and_login(request, onsuccess='/', onfail='/login'):
    #Returns user object if parameters match the database.
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
	#We Sign the user..
        login(request, user)
        return redirect(onsuccess)
    else:
	#Show a "incorrect credentials" message
	state="Wrong username/password combination"
	return render_to_response('login.html', {'state':state},context_instance=RequestContext(request))
        return redirect(onfail)  

def create_user_website(username, email, password, first_name, last_name, website, job_title, company_name):
    #Usage:
    #user = create_user_website(username=post['email'], email=post['email'], password=post['password'], 
    # first_name=post['first_name'], last_name=post['last_name'], website=post['website'], 
    # job_title=post['job_title'], company_name=post['company_name'])
    try:
    	user = User(username=username, email=email, first_name=first_name, last_name=last_name)
    	user.set_password(password)
    	user.save()
    	print("User object created..")
    	print("Creating profile..")
    
    	user_profile = UserProfile(user=user, website=website, job_title=job_title, company_name=company_name)
    	user_profile.save()
    	print("User profile created..")

    	student_role = Role.objects.get(pk=6)
    	new_role_mapping = User_Roles(name="website", user_userid=user, role_roleid=student_role)
    	new_role_mapping.save()

    	individual_organisation = Organisation.objects.get(pk=1)
    	new_organisation_mapping = User_Organisations(user_userid=user, organisation_organisationid=individual_organisation)
    	new_organisation_mapping.save()

    	#Check if previous were a success.
    	print("User Role mapping (website) success.")
    	return user
    except:
	print("Username  exists")
	return None


def create_user_more(username, email, password, first_name, last_name, roleid, organisationid):
    user = User(username=username, email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.save()
    role=Role.objects.get(pk=roleid)
    organisation = Organisation.objects.get(pk=organisationid)

    #Create role mapping. 
    user_role = User_Roles(name="blah", user_userid=user, role_roleid=role)
    #user_role = User_Roles(user_userid=user)
    user_role.save()

    #Create organisation mapping.
    user_organisation = User_Organisations(user_userid=user, organisation_organisationid=organisation)
    user_organisation.save()

    #Create same user in UM-TinCan LRS

    
    print("User Role mapping success.")
    return user


def user_exists(username):
    user_count = User.objects.filter(username=username).count()
    if user_count == 0:
        return False
    return True

def logout_view(request):
    logout(request)
    return redirect('login')
    #return render_to_response('login.html')

def sign_up_in(request):
    print("Creating new user from website..")
    post = request.POST
    if not user_exists(post['email']): 
	user = create_user_website(username=post['username'], email=post['email'], password=post['password'], first_name=post['first_name'], last_name=post['last_name'], website=post['website'], job_title=post['job_title'], company_name=post['company_name'])
	if user:
        	return auth_and_login(request)
	else:
		state="The Username already exists.."
		return render_to_response('user/user_create_website.html',{'state':state}, context_instance=RequestContext(request))
		#return redirect("/register", {'state':state})
    else:
        #Show message that the username/email address already exists in our database.
        return redirect("/register")

def logout_view(request):
    logout(request)
    return redirect('login')
    #return render_to_response('login.html')


@login_required(login_url='/login/')
def secured(request):
    current_user = request.user.username
    print("secured: logged in username: " + current_user)
    return render_to_response("secure.html", 
	{'current_user': current_user},
	context_instance=RequestContext(request)
    )

@login_required(login_url='/login/')
def upload_view(request):
    current_user = request.user.username
    return render_to_response("upload.html", {'current_user': current_user},
        context_instance=RequestContext(request))

@login_required(login_url='/login/')
def management_view(request):
    current_user = request.user.username
    return render_to_response("manage.html", {'current_user': current_user},
        context_instance=RequestContext(request))

@login_required(login_url='/login/')
def reports_view(request):
    current_user = request.user.username
    return render_to_response("reports.html", {'current_user': current_user},
        context_instance=RequestContext(request))

