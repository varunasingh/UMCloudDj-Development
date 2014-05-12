from django.shortcuts import render
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

import os 
#UMCloudDj.uploadeXe
from uploadeXe.models import Document
from uploadeXe.forms import ExeUploadForm

def my_view(request):
	current_user = request.user.username
	print("Logged in username: " + current_user)
	return render_to_response(
        	'/base.html',
        	{'current_user': current_user, 'form': form},
        	context_instance=RequestContext(request)
	)

@login_required(login_url='/login/')
def list(request):
    # Handle file upload
    print("Current User logged in is: " + request.user.email)
    if request.method == 'POST':
        form = ExeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(exefile = request.FILES['exefile'])
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
	    		setattr(newdoc, 'userid', request.user.id)
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
    documents = Document.objects.filter(userid=request.user.id, success="YES")
    current_user = request.user.username

    # Render list page with the documents and the form
    return render_to_response(
        'myapp/list.html',
        {'documents': documents, 'form': form, 'current_user': current_user},
        context_instance=RequestContext(request)
    )

# Create your views here.
