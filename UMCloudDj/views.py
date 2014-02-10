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
from django.http import HttpResponse
from django.shortcuts import render
import os
#from UMCloudDj.models import Ustadmobiletest
from uploadeXe.models import Ustadmobiletest


#UMCloudDj.uploadeXe

@csrf_exempt
def sendtestlog_view(request):
	print("Up on a melencholy hill..")
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
	

def getcourse_view(request):
	courseid = request.GET.get('id')
	print("The course id requested is: " + courseid)
	#return render_to_response(
	#documents = Document.objects.filter(userid=request.user.id)
	matchedCourse = Document.objects.filter(id=str(courseid)).get(id=str(courseid))
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
