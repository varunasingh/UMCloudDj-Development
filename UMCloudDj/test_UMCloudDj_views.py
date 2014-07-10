from django.utils import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpRequest
from django.test.client import Client
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from uploadeXe.models import Role
from uploadeXe.models import User_Roles
from django.forms import ModelForm
from organisation.models import Organisation
from organisation.models import UMCloud_Package
from organisation.models import User_Organisations
from users.models import UserProfile
from django import forms
from uploadeXe.models import Package as Document
import os 
from django.conf import settings

class UMCloudDjViewTestCase(TestCase):
    fixtures = ['uploadeXe/fixtures/initial-model-data.json']
    def setUp(self):
	"""
	Have to manually create users and assign relationships for initial testing.
	"""
	testuser = User.objects.create(username='testuser1', password='12345', is_active=True, is_staff=True, is_superuser=True)
	adminrole=Role.objects.get(pk=1)
	user_role = User_Roles(name="test", user_userid=testuser, role_roleid=adminrole)
	user_role.save()
	testuser2 = User.objects.create(username="testuser2", password="54321", is_active=True, is_staff=True, is_superuser=True)
	user_role2 = User_Roles(name="test", user_userid=testuser2, role_roleid=adminrole)
	user_role2.save()
	mainorganisation = Organisation.objects.get(pk=1)
	user_organisation = User_Organisations(user_userid=testuser, organisation_organisationid=mainorganisation)
	user_organisation.save()
	user_organisation2 = User_Organisations(user_userid=testuser2, organisation_organisationid=mainorganisation)
	user_organisation2.save()

    def test_checklogin_view(self):
	"""
	Tests if user can check login externally
	"""
	post_data={'username':'testuser1','password':'12345'}
	response = self.client.post('/checklogin/', post_data)
	self.assertEquals(response.status_code, 200)

    def test_incorrect_checklogin_view(self):
	"""
	Tests if incorrect login returns false
	"""
	post_data={'username':'testuser1','password':'cowsaysmoo'}
	response=self.client.post('/checklogin/', post_data)
	self.assertEquals(response.status_code, 403)

    def test_getcourse_view(self):
	view_name="getcourse"
	"""
	Tests if external requests return untrue(403) for an invalid public course by id
	"""
	self.c = Client()
	response = self.c.get('/getcourse/', {'id':42})
	self.assertEquals(response.status_code, 403)
	
	"""
	Tests if external requests return true for a valid public course by id
	"""
	testuser1 = User.objects.get(username="testuser1")
	newDocument=Document(name="unittest", url="//this.is.the/linke/to/the/test",uid="123UGOFree", success="Yes", publisher=testuser1)
	newDocument.save()
	self.c = Client()
	response = self.c.get('/getcourse/',{'id':1})
	self.assertEquals(response.status_code, 200)
    
    def test_auth_and_login(self):
	view_url='/auth/'
	"""
	This will test authentication over the django setup from umclouddj web login.
	On success it should redirect (302) to '/' and on fail it should redirect back to '/login'
	UMCloudDj.views.auth_and_login(request, onsuccess="/", onfail="/login")
	"""
	post_data={'username':'testuser1','password':'12345'}
	response = self.client.post(view_url, post_data)
	self.assertEquals(response.status_code, 302)
	self.assertRedirects(response, '/')

	"""
	Test incorrect login with redirect back to login page.
	"""
	post_data_incorrect={'username':'testuser1','password':'incorrectpassword'}
	response = self.client.post(view_url,post_data_incorrect)
	self.assertContains(response,'Wrong username/password combination' , 1, status_code=200)
	

    	"""
	Test login details from ustadmobile.com wordpress server
	"""
	print("Project Root:")
	data='willbereplaced'
	"""
	We get the password from an external file accesable to test
	"""
	try:
		with open (os.path.join(settings.PROJECT_ROOT, 'wordpresscred.txt'), "r") as myfile:
    			data=myfile.readlines()
		print("GOT WP CRED FILE")
		data=data[0].strip("\n")
		post_data_wordpress={'username':'testuser','password':data}
		response=self.client.post(view_url, post_data_wordpress)
		self.assertEquals(response.status_code, 302)
		self.assertRedirects(response, '/')
	except:	
		try:
			with open('/opt/UMCloudDj/wordpresscred.txt',"r") as myfile:
				data=myfile.readlines()
			print("GOT WP CRED FILE in /opt/")
			data=data[0].strip("\n")
                	post_data_wordpress={'username':'testuser','password':data}
                	response=self.client.post(view_url, post_data_wordpress)
                	self.assertEquals(response.status_code, 302)
                	self.assertRedirects(response, '/')
		except:
			print("WORDPRESS CRED NOT INCLUDED")

    def test_sign_up_in(self):
	"""
	Test if User can be created by the view that creates a user from the website
	UMCloudDj.views.sign_up_in()
	"""
	view_url="/signup/"
	post_data={'username':'cowsaysmoo','email':'cow@moo.com','password':'iamacow','first_name':'Cow','last_name':'Moo','website':'www.cow.moo','job_title':'Cow','company_name':'Moo'}
	response = self.client.post(view_url, post_data)
	cow=User.objects.get(username="cowsaysmoo")
	self.assertEqual(cow.last_name, 'Moo')
	
	

    def tearDown(self):
	print("end of UMCloud Views test")
