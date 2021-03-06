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
from organisation.models import Organisation, Organisation_Code
from organisation.models import UMCloud_Package
from organisation.models import User_Organisations
from users.models import UserProfile
from django import forms
from uploadeXe.models import Package as Document
from uploadeXe.models import Course 
from uploadeXe.models import Ustadmobiletest
from users.models import UserProfile
import os 
from django.conf import settings

class UMCloudDjViewTestCase(TestCase):
    fixtures = ['uploadeXe/fixtures/initial-model-data.json']
    def setUp(self):
	"""
	Have to manually create users and assign relationships for initial testing.
	"""
	testuser = User.objects.create(username='testuser1', password='12345', is_active=True, is_staff=True, is_superuser=True)
	testuser.save()
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

	orgadmin01=User.objects.create(username='orgadmin01', password='12345', is_active=True, is_staff=True, is_superuser=False)
	orgadmin01.save()
	orgadminrole=Role.objects.get(pk=2)
	orgadmin01_role = User_Roles(name="test", user_userid=orgadmin01, role_roleid=orgadminrole)
	orgadmin01_role.save()
	orgadmin01_organisation = User_Organisations(user_userid=orgadmin01, organisation_organisationid=mainorganisation)
	orgadmin01_organisation.save()
	
	test_course = Course(name="TestCourse", category="Testing", description="This is a course made for testing", publisher=testuser, organisation=mainorganisation)
	test_course.save()
	test_course.students.add(testuser)
	test_course.save()
	
	test_block=Document(name="unittest01", url="//this.is.the/linke/to/the/test/01",uid="123UGOFreei01", success="Yes", publisher=testuser)
	test_block.save()
	test_course.packages.add(test_block)
	test_course.save()

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
	self.assertEquals(response['location'],"http://testserver/")

	"""
	Test incorrect login with redirect back to login page.
	"""
	post_data_incorrect={'username':'testuser1','password':'incorrectpassword'}
	response = self.client.post(view_url,post_data_incorrect)
	self.assertContains(response,'Wrong username/password combination' , 1, status_code=200)
	self.assertContains(response, 'Log in')
	

    	"""
	Test login details from ustadmobile.com wordpress server
	"""
	print("Project Root:")
	data='willbereplaced'
	"""
	We get the password from an external file accesable to test
	"""
	try:
		with open('/opt/UMCloudDj/wordpresscred.txt',"r") as myfile:
			data=myfile.readlines()
		print("GOT WP CRED FILE in /opt/")
		data=data[0].strip("\n")
               	post_data_wordpress={'username':'testuser','password':data}
               	response=self.client.post(view_url, post_data_wordpress)
               	self.assertEquals(response.status_code, 302)
		self.assertEquals(response['location'],"http://testserver/")
	except:
		print("WORDPRESS CRED NOT INCLUDED")

	"""
        Test incorrect login details from ustadmobile.com wordpress server
        """
        print("Project Root:")
        data='willbereplaced'
        """
        We get the password from an external file accesable to test
        """
	data="incorrectpasswordlalala"
        post_data_wordpress={'username':'testuserwordpress','password':data}
        response=self.client.post(view_url, post_data_wordpress)
        self.assertContains(response,'Wrong username/password combination' , 1, status_code=200)
	self.assertContains(response, 'Log in')


    def test_sign_up_in(self):
	"""
	Test if User can be created by the view that creates a user from the website
	UMCloudDj.views.sign_up_in()
	"""
	view_url="/signup/"
	post_data={'username':'cowsaysmoo','email':'cow@moo.com','password':'iamacow','first_name':'Cow','last_name':'Moo','website':'www.cow.moo','job_title':'Cow','company_name':'Moo','dateofbirth':'02/02/2014','phonenumber':'+1234567890','address':'123 STREET, XYZ Avenue, ABC building, 3A, DEFGHIJ, KLMNOPQRST','gender':'M', 'organisationrequest':''}
	response = self.client.post(view_url, post_data)
	cow=User.objects.get(username="cowsaysmoo")
	self.assertEqual(cow.last_name, 'Moo')
	
    def test_getassignedcourseids(self):
	"""
        Test if getassignedcourseids returns users's course ids with block ids and details as an xml in the body
        """
	view_url="/getassignedcourseids/"
	post_data={'username':'testuser1','password':'12345'}
	response = self.client.post(view_url, post_data)
	self.assertEquals(response.status_code, 200)
	self.assertContains(response, "<?xml version=\"1.0\" ?><getasssignedcourseids>", status_code=200)
	self.assertContains(response, "<course>TestCourse</course><id>1</id>", status_code=200)

    def test_sendelpfile(self):
	"""
	Tests the file upload  (eXe elp package) block
	"""
	print("starting..")
        try:
		view_url="/sendelpfile/"
                with open('/opt/UMCloudDj/gt1.elp',"r") as myfile:
			print("found file here")
			post_data={'username':'testuser1', 'password':'12345', 'exeuploadelp': myfile}
                	response = self.client.post(view_url, post_data)
			print (response)
			self.assertEquals(response['courseid'], '1')
			self.assertEquals(response.status_code, 200)
        except:
                print("TEST ELP FILE NOT INCLUDED")

    def test_logout_view(self):
	"""
	Test that logout view logs people off
	"""
	
	"""
	logging user in
	"""
	self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user = authenticate(username='testuser1', password='12345')
        login = self.c.login(username='testuser1', password='12345')

	view_url="/logout/"
	self.c = Client()
        response = self.c.get(view_url)
        self.assertEquals(response.status_code, 302)
	self.assertRedirects(response, '/login/')

    def test_secured(self):
	"""
	Tests that logged in user is able to get to the main menu
	"""

	"""
	Un-Logged in user will redirect to login page.
	"""
	view_url="/home/"
	self.c = Client()
	response = self.c.get(view_url)
	self.assertEquals(response.status_code, 302)
	self.assertRedirects(response, '/login/?next=/home/')
	
	"""
	Logged in user will be able to see the secured page
	"""
	self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user = authenticate(username='testuser1', password='12345')
        login = self.c.login(username='testuser1', password='12345')

	response = self.c.get(view_url)
	self.assertEquals(response.status_code, 200)
	self.assertContains(response, "You are logged in. Here is what you can do", status_code=200)

    def test_upload_view(self):
	"""
	Tests that logged in user and not logged in user to get to the bblock upload page
	"""
	
	"""
	Not logged in user will redirect to login page
	"""
	view_url="/upload/"
	self.c = Client();
	response = self.c.get(view_url)
	self.assertEquals(response.status_code, 302)
	self.assertRedirects(response, '/login/?next=/upload/')

	"""
	Logged in user will be able to see the upload page
	"""
	self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user = authenticate(username='testuser1', password='12345')
        login = self.c.login(username='testuser1', password='12345')

        response = self.c.get(view_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Ustad Mobile Courses", status_code=200)

	
    def test_management_view(self):
	"""
        Tests that logged in user and not logged in user to get to the management page
        """

        """
        Not logged in user will redirect to login page
        """
        view_url="/management/"
        self.c = Client();
        response = self.c.get(view_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/management/')

        """
        Logged in user will be able to see the upload page
        """
        self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user = authenticate(username='testuser1', password='12345')
        login = self.c.login(username='testuser1', password='12345')

        response = self.c.get(view_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Management", status_code=200)

    def test_reports_view(self):
	"""
        Tests that logged in user and not logged in user to get to the Reports page
        """

        """
        Not logged in user will redirect to login page
        """
        view_url="/reports/"
        self.c = Client();
        response = self.c.get(view_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/reports/')

        """
        Logged in user will be able to see the upload page
        """
        self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user = authenticate(username='testuser1', password='12345')
        login = self.c.login(username='testuser1', password='12345')

        response = self.c.get(view_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Reports", status_code=200)

    def test_loginview(self):
	"""
        Tests that user to get to the Login page
        """

        view_url="/login/"
        self.c = Client();
        response = self.c.get(view_url)
        self.assertEquals(response.status_code, 200)
	self.assertContains(response, "Login", status_code=200)

    def test_register_start_view(self):
	"""
	Tests if the register / signn up for users logged out works.
	"""
	view_url="/register/start/"
	self.c = Client()
	response = self.c.get(view_url)
	self.assertEquals(response.status_code, 200)
	self.assertContains(response, "Request my account")

    def test_register_view(self):
        """
        Tests if the register / signn up for users logged out works.
        """
        view_url="/register/"
	c=Client()
        response = c.get(view_url)
        self.assertEquals(response.status_code, 301) #301 is permanant redirect
	self.assertEqual(response.get('location'),'http://testserver/register/start/')


    def test_sendtestlog_view(self):
	view_url="/sendtestlog/"
	password = ""
	try:
		with open ("umpassword.txt", "r") as myfile:
                	password=myfile.read().replace('\n', '')
	except:
		print("Cannot find test password file.")
		password="wrongpassword"

	post_data={'username':'test','password':password, 'appunittestoutput':'new|umclouddjunittestname|pass|0.5s|dategroup|uncloudjunittest|umclouddjtestversion|'}
        response = self.client.post(view_url, post_data)
	self.assertEquals(response.status_code, 200)
	ustadmobile_test = Ustadmobiletest.objects.get(name='umclouddjunittestname')
	self.assertEquals(ustadmobile_test.ustad_version, 'umclouddjtestversion')
	
    
    def test_report_statements_view(self):
	"""
        Tests that logged in user and not logged in user to get to the Report statement page
        """

        """
        Not logged in user will redirect to login page
        """
        view_url="/statementsreports/"
        self.c = Client();
        response = self.c.get(view_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/statementsreports/')

        """
        Logged in user will be able to see the upload page
        """
        self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user = authenticate(username='testuser1', password='12345')
        login = self.c.login(username='testuser1', password='12345')

        response = self.c.get(view_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Select the filters below", status_code=200)

    def test_report_selection_view(self):
	"""
        Tests that logged in user and not logged in user to get to the Report mcq page
        """

        """
        Not logged in user will redirect to login page
        """
        view_url="/mcqreports/"
        self.c = Client();
        response = self.c.get(view_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/mcqreports/')

        """
        Logged in user will be able to see the upload page
        """
        self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user = authenticate(username='testuser1', password='12345')
        login = self.c.login(username='testuser1', password='12345')

        response = self.c.get(view_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Select the filters below", status_code=200)
	
    def test_admin_approve_request_view(self):
	"""
	Tests that an organisational admin can view the requests page
	UMCloudDj.views.admin_approve_request
	"""
	view_url="/usersapprove/"
	
	"""
	Tests that you need to be logged in
	"""
	self.c = Client();
	response = self.c.get(view_url)
	self.assertEquals(response.status_code, 302)
	self.assertRedirects(response, "/login/?next=/usersapprove/")

	"""
	Tests that you need to be logged in as well as be an organisational admin
	"""
	self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user = authenticate(username='testuser1', password='12345')
        login = self.c.login(username='testuser1', password='12345')
	
	response = self.c.get(view_url)
        self.assertEquals(response.status_code, 200)
	self.assertContains(response, "You do not have permission to see this page")

	"""
	Tests that if you are an org admin you can see the page
	"""
	
	self.c = Client();
        self.user = User.objects.get(username="orgadmin01")
        self.user = authenticate(username='orgadmin01', password='12345')
        login = self.c.login(username='orgadmin01', password='12345')

        response = self.c.get(view_url)
        self.assertEquals(response.status_code, 200)
	self.assertContains(response, "No new user requests")

    def test_sign_up_in(self):
	view_url="/signup/"
	post_data={'username':'testrequest', 'email':'testrequest@testing.com','password':'12345','passwordagain':'12345','first_name':'Test','last_name':'Request','website':'http://www.testing.com/','job_title':'Tester','company_name':'TestCorp','dateofbirth':'02/02/1989','address':'TestLand','phonenumber':'+1234567890','gender':'M','organisationrequest':''}
	response=self.client.post(view_url,post_data)
	self.assertEquals(response.status_code, 200)
	testrequest=User.objects.get(username="testrequest")
	self.assertEquals('testrequest', testrequest.username)
	self.assertEquals(False, UserProfile.objects.get(user=testrequest).admin_approved)
	
	

    def test_admin_approve_request_view_approve(self):

	userrequest = User.objects.create(username="testrequest01", password="12345", is_active=True, is_staff=False, is_superuser=False)
        userrequest.save()
        studentrole = Role.objects.get(pk=6)
        userrequest_role=User_Roles(name="test", user_userid=userrequest, role_roleid=studentrole)
        userrequest_role.save()
	mainorganisation=Organisation.objects.get(pk=1)
        userrequest_organisation = User_Organisations(user_userid=userrequest, organisation_organisationid=mainorganisation)
        userrequest_organisation.save()
        userrequestProfile = UserProfile(user=userrequest, organisation_requested=mainorganisation, phone_number="+123456789",date_of_birth="1989-02-09", gender="M")
        userrequestProfile.save()
	#creating org code: to get rid of the randrange unknown error.
	newcode=Organisation_Code(organisation=mainorganisation,code="COW1234")
	newcode.save()

	view_url="/usersapprove/"
	self.c = Client();
        self.user = User.objects.get(username="orgadmin01")
        self.user = authenticate(username='orgadmin01', password='12345')
        login = self.c.login(username='orgadmin01', password='12345')

        response = self.c.get(view_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "testrequest01")

	view_url="/usersapprove/"
        self.c = Client();
        self.user = User.objects.get(username="orgadmin01")
        self.user = authenticate(username='orgadmin01', password='12345')
        login = self.c.login(username='orgadmin01', password='12345')

	testrequest01id=User.objects.get(username="testrequest01").id
	toaccept=[testrequest01id]
	post_data={'target':toaccept}
	idname=str(testrequest01id)+"_radio"
	idvalue=str(testrequest01id)+"_1"
	post_data={idname:idvalue}
	response = self.c.post(view_url, post_data)
        self.assertEquals(response.status_code, 302)
	self.assertRedirects(response, "/userstable/")
	self.assertEquals(True, UserProfile.objects.get(user=userrequest).admin_approved)

    def tearDown(self):
	print("end of UMCloud Views test")
