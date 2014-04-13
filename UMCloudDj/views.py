from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import auth
from django.template import RequestContext
from uploadeXe.models import Document
from uploadeXe.models import Ustadmobiletest
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
import datetime
import os
#import urllib, json
import urllib
import urllib2, base64, json
import glob #For file ^VS 130420141454
#from UMCloudDj.models import Ustadmobiletest
from uploadeXe.models import Ustadmobiletest
#from django.utils import simplejson

#UMCloudDj.uploadeXe

def get_report_zambia(request, onfail='/reports'):
    	print("Getting variables..")
    	date_since = request.POST['since_1_alt']
    	date_until = request.POST['until_1_alt']
    	activity = request.POST['activity']
    	print("Got variables. They are: ")
    	print(activity)
    	print(date_since)
    	print(date_until)
	#Code for report making here.
	umlrs = "http://svr2.ustadmobile.com:8001/xAPI/statements" #Should be part of 
	lrs_endpoint = umlrs + "?" + "&since=" + date_since + "&until=" + date_until + "&activity=" + activity
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
        jdata = json.dumps(jdata_string) #puts in a JSON string  #JSON encoding
        data = json.loads(jdata_string) #puts in a JSON #JSON decoding # to a python dictionary
	#print(data['statements'])

	response = []
	for ja in data['statements']:
		if ja['object']['id'] == activity:
			#response.append({'timestamp':ja.timestamp, 'user': ja.actor.name, 'response': ja.result.response, 'success': ja.result.success, 'correctResponsePattern': ja.object.correctResponsesPattern})
			response.append({'timestamp':ja['timestamp'], 'user':ja['actor']['name'], 'verb':ja['verb']['display']['en-US'], 'desscription':ja['object']['definition']['description']['en-GB'] })
	#print("The response is:")
	#print(response)

	##play with the data now.

    	return render_to_response("report_zambia.html", {'activity':activity, 'date_since':date_since , 'date_until':date_until , 'data':data , 'lrs_endpoint':lrs_endpoint , 'response':response }, context_instance=RequestContext(request))

def report_selection_view(request):
	c = {}
        c.update(csrf(request))
        #return render_to_response('report_selection.html', c) #Somehow messes with the css and includes of scripts. This is not such sensitive data, so leaving.
	return render(request, "report_selection.html")


def readjsonfromlrs_view(request):
	lrsurl = "http://cloud.scorm.com/ScormEngineInterface/TCAPI/public/statements?limit=25&related_activities=false&related_agents=false"
	lrsurl = "http://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=HOEpcI6e_Zc&format=json"
	lrsurl = "http://gdata.youtube.com/feeds/api/playlists/PLE-68G1RgFNzzgniTuuctub872JuwjJJw?v=2&alt=json"
	lrsurl = "http://cloud.scorm.com/ScormEngineInterface/TCAPI/public/statements?limit=70&related_activities=false&related_agents=false"
	lrsurl = "http://svr2.ustadmobile.com:8001/xAPI/statements?limit=7"
	#Search and Filter like: http://svr2.ustadmobile.com:8001/xAPI/statements?limit=7&activity=http://www.ustadmobile.com/looking_at_things&activity=http://www.ustadmobile.com/looking_at_things&since=2014-02-02&until=2014-02-03

	
	#BASIC AUTHENTICATION
	username="testuser"
	password="testpassword"
	req = urllib2.Request(lrsurl)
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	req.add_header("Authorization", "Basic %s" % base64string)   
	req.add_header("X-Experience-API-Version", "1.0.1")
	
	#GETTING JSON String from URL
	jdata_string = urllib2.urlopen(req).read() #gets string..
	jdata = json.dumps(jdata_string) #puts in a JSON string  #JSON encoding 
	data = json.loads(jdata_string) #puts in a JSON #JSON decoding # to a python dictionary
	
	#Returns the JSON object only to the template. No variables. Such that {{statements}} can be accessed. 
	##return render(request, "json_view.html", data) #Returns jdata so that {{statements}} can be accessed so.
	#More about render: https://docs.djangoproject.com/en/dev/intro/tutorial03/#a-shortcut-render

	#Returns the JSON. No template. Nothing else.
	#return HttpResponse(json.dumps(json_string2, ensure_ascii=False), content_type="application/json; encoding=utf-8")

	#To return JSON as variable to template
	return render_to_response("json_view.html", {'json_dump':data}, context_instance=RequestContext(request))

	#To return only the JSON object
	#resp = HttpResponse(content_type="application/json")
	#json.dump(jdata, resp)
	#return resp	
	
	#If you want to return to the 'login' page.
	#return redirect('login')



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
	#print("The umpasswod is : " + umpassword);

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
	

	

	#context_instance=RequestContext(request)
	#response = render_to_response("sendtestlog.html", {'appunittestoutput': unittestlogs}, context_instance=RequestContext(request))
	#return response

	#c = {}
        #c.update(csrf(request))
	#d = {'appunittestoutput': unittestlogs}
	#context_instance = RequestContext(request, {'appunittestoutput': unittestlogs})
	
	#return render_to_response('sendtestlog.html', c, context_instance=RequestContext(request))
	#return render_to_response('sendtestlog.html', c)
	

	#return redirect("/")
	

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
            		print('exe_do -x ustadmobile ' + appLocation + '/../UMCloudDj/media/' + uid + ' ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid )
            		if os.system('exe_do -x ustadmobile ' + appLocation + '/../UMCloudDj/media/' + uid + ' ' + appLocation + '/../UMCloudDj/media/eXeExport/' + unid ) == 0: # If command ran successfully,
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
                        		setattr(newdoc, 'userid', request.user.id)
                        		newdoc.save()
                        		print("Starting grunt process..")


					#Start..
					"""

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



					"""
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
	

def testelpfiles_view(request):
	appLocation = (os.path.dirname(os.path.realpath(__file__)))
	#Log start time here..
	cmdStartTime = datetime.datetime.today()
	#Code here..
	print "hello there"
	for dir in os.listdir('/home/varuna/umcdj/UMCloudDj/UMCloudDj/media/eXeUpload/'):
		print dir
	print "glob"
	print glob.glob('/home/varuna/umcdj/UMCloudDj/UMCloudDj/media/eXeUpload/*elp');
	"""
	testelpfiles = glob.glob('/home/varuna/umcdj/UMCloudDj/UMCloudDj/media/eXeTestElp/*elp');
	for testelp in testelpfiles:
		print ("[testelpfiles]: FOR LOOP BEGINS. FILE: " + testelp);
		unid = testelp.split('.um.')[-2]
		unid = unid.split('/')[-1]
		print("[testelpfiles] unid: " + unid)
		
		#if os.system('exe_do -x ustadmobile ' + appLocation + '/../UMCloudDj/media/eXeTestElp/' + testelp + ' ' + appLocation + '/../UMCloudDj/media/eXeTestExport/' + unid ) == 0: # If command ran successfully,
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

	#cmdStartTime = datetime.datetime.today()
	"""
	cmdEndTime = datetime.datetime.today()

	#Ustadmobiletest
	#matchedCourse = Document.objects.filter(id=str(courseid)).get(id=str(courseid))
	print datetime.date.today()
	matchedCourseTestResults = Ustadmobiletest.objects.filter(dategroup='grunt', pub_date__gte=cmdStartTime, pub_date__lte=cmdEndTime)
	if matchedCourseTestResults:
		print("[testelpfiles] Test results exists")
		for matchedCourseResult in matchedCourseTestResults:
			print ("[testelpfiles]: Result: ")
			print (matchedCourseResult.name)

		uploadresponse = HttpResponse(status=200)
        	uploadresponse.write("All good.")
        	return uploadresponse

	else:
		print ("[testelpfiles] No results exists.")
		uploadresponse = HttpResponse(status=200)
        	uploadresponse.write("Something went wrong or no tests were run")
        	return uploadresponse

	

def getcourse_view(request):
	courseid = request.GET.get('id')
	print("The course id requested is: " + courseid)
	#return render_to_response(
	#documents = Document.objects.filter(userid=request.user.id)
	matchedCourse = Document.objects.filter(id=str(courseid)).get(id=str(courseid))
	#Use get when you want to get a single object. Use filter when you want to get a list.
	if matchedCourse:
		print("Course exists!")
		#print(matchedCourse.username)
		print("The unique folder for course id: " + courseid + " is: " + matchedCourse.uid + "/" + matchedCourse.name)
		coursefolder = matchedCourse.uid + "/" + matchedCourse.name
		xmlDownload = coursefolder + "_ustadpkg_html5.xml"
		#if request.method == 'POST':
			#print("REQUEST IS POST!!")
		data = { 
			'folder' : coursefolder,
			'xmlDownload' : xmlDownload
		}
		response = HttpResponse("folder:" + coursefolder)
		response = HttpResponse("xmlDownload:" + xmlDownload)
		response = render_to_response("getcourse.html", {'coursefolder': coursefolder, 'xmlDownload': xmlDownload}, context_instance=RequestContext(request))
		response['folder'] = coursefolder
		response['xmlDownload'] = xmlDownload
		#response = HttpResponse("Text only, please.", content_type="text/plain")
		#response.write("<p>Here is the text of the Web page.</p>")
		#response.write("<p>Here is another paragrah.</p>")
		return response

	else:
		print("Sorry, a course of that ID was not found globally")
		response2 = HttpResponse("folder:na")
		return response2
	
	return redirect("/")

def register_view(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('signup.html', c)

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
	return render_to_response('login.html', c)

def auth_and_login(request, onsuccess='/uploadeXe/', onfail='/login'):
    #Returns user object if parameters match the database.
    user = authenticate(username=request.POST['email'], password=request.POST['password'])
    if user is not None:
	#We Sign the user..
        login(request, user)
        return redirect(onsuccess)
    else:
	#Show a "incorrect credentials" message
        return redirect(onfail)  

def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    return user

def user_exists(username):
    user_count = User.objects.filter(username=username).count()
    if user_count == 0:
        return False
    return True

def sign_up_in(request):
    post = request.POST
    if not user_exists(post['email']): 
        user = create_user(username=post['email'], email=post['email'], password=post['password'])
        return auth_and_login(request)
    else:
 	#Show message that the username/email address already exists in our database.
        return redirect("/login/")

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
