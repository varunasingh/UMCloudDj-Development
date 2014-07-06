from django.utils import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpRequest
from django.test.client import Client
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

#Testing..
from django.forms import ModelForm
from organisation.models import Organisation
from organisation.models import UMCloud_Package
from organisation.models import User_Organisations
from school.models import School
from allclass.models import Allclass
from uploadeXe.models import Role
from uploadeXe.models import User_Roles
from django import forms



class AllclassViewTestCase(TestCase):
    fixtures = ['uploadeXe/fixtures/initial-model-data.json']
    def setUp(self):
	"""
	Have to manually create users and assign relationships for initial testing.
	"""
	testuser1= User.objects.create(username='testuser1', password='12345', is_active=True, is_staff=True, is_superuser=True)
	testuser1.save()
	adminrole=Role.objects.get(pk=1)
	user_role1 = User_Roles(name="test", user_userid=testuser1, role_roleid=adminrole)
	user_role1.save()
	testuser2 = User.objects.create(username="testuser2", password="54321", is_active=True, is_staff=True, is_superuser=True)
	testuser2.save()
	user_role2 = User_Roles(name="test", user_userid=testuser2, role_roleid=adminrole)
	user_role2.save()
	mainorganisation = Organisation.objects.get(pk=1)
	user_organisation1 = User_Organisations(user_userid=testuser1, organisation_organisationid=mainorganisation)
	user_organisation1.save()
	user_organisation2 = User_Organisations(user_userid=testuser2, organisation_organisationid=mainorganisation)
	user_organisation2.save()

	testuser3 = User.objects.create(username='testuser3', password='12345', is_active=True, is_staff=True, is_superuser=True)
        testuser3.save()
        user_role3 = User_Roles(name="test", user_userid=testuser3, role_roleid=adminrole)
        user_role3.save()
	user_organisation3 = User_Organisations(user_userid=testuser3, organisation_organisationid=mainorganisation)
	user_organisation3.save()
	
	testuser4 = User.objects.create(username='testuser4', password='12345', is_active=True, is_staff=True, is_superuser=True)
        testuser4.save()
        user_role4 = User_Roles(name="test", user_userid=testuser4, role_roleid=adminrole)
        user_role4.save()
        user_organisation4 = User_Organisations(user_userid=testuser4, organisation_organisationid=mainorganisation)
	user_organisation4.save()


	school1 = School(school_name="TestSchool", school_desc="This is the desc of the TestSchool",organisation_id=1)
	school1.save()
	

    def test_allclass_create(self):
	"""
	Users can create classes
	allclass.views.allclass_create
	"""
	url_name="allclass_new"

	"""
	Classes cannot be created without logging in
	allclass.views.allclass_create
	"""
	student_list_ids=[3,4]
        post_data={'class_name':'TestClass','class_desc':'Class created by unit testing','class_location':'Testville','schoolid':1,'teacherid':2,'target': student_list_ids}
        
        requesturl = reverse(url_name)
        response = self.client.post(requesturl, post_data)
        #test_create_user = Allclass.objects.get(allclass_name="TestClass")
        #self.assertEqual("TestClass", Allclass.objects.get(allclass_name="TestClass").allclass_name)
	self.assertEqual(response.status_code, 302)


	"""
	Classes can be created with logging in
	allclass.views.allclass_create
	"""
	student_list_ids=[3,4]
	post_data={'class_name':'TestClass','class_desc':'Class created by unit testing','class_location':'Testville','schoolid':1,'teacherid':2,'target': student_list_ids}
	
	self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser1', password='hello')
        login = self.c.login(username='testuser1', password='hello')

	requesturl = reverse(url_name)
	response = self.c.post(requesturl, post_data)
	test_create_user = Allclass.objects.get(allclass_name="TestClass")
	self.assertEqual("TestClass", Allclass.objects.get(allclass_name="TestClass").allclass_name)

    @unittest.expectedFailure
    def test_allclass_create_failure(self):
	"""
	Incorrectly done model fails for logged in user
	allclass.views.allclass_create
	"""
	url_name="allclass_new"
	student_list_ids=[3,4]
        post_data_incorrect={'class_name':'TestClass','class_desc':'Class created by unit testing','class_location':'Testville','schoolid':1,'teacherid':2,'target': student_list_ids}


        self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser1', password='hello')
        login = self.c.login(username='testuser1', password='hello')

        requesturl = reverse(url_name)
        response = self.c.post(requesturl, post_data_incorrect)
        test_create_user = Allclass.objects.get(allclass_name="TestClass")
        self.assertEqual("TestClass", Allclass.objects.get(allclass_name="TestClass").allclass_name)


    def test_update(self):

	"""
        Classes can be created with logging in
        allclass.views.allclass_create
        """
        student_list_ids=[3,4]
        post_data={'class_name':'TestClass','class_desc':'Class created by unit testing','class_location':'Testville','schoolid':1,'teacherid':2,'target': student_list_ids}

        self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser1', password='hello')
        login = self.c.login(username='testuser1', password='hello')

        requesturl = reverse('allclass_new')
        response = self.c.post(requesturl, post_data)
        test_create_user = Allclass.objects.get(allclass_name="TestClass")
	print("Test Dat for test_update:")
	print(Allclass.objects.all())


	url_name='allclass_edit'
	student_list_ids_changed=[3]
	post_data_changes={'class_name':'TestClass','class_desc':'Changed Class created by unit testing','class_location':'ChangedTestville','schoolid':1,'target2':2,'target': student_list_ids_changed}


        """
        Login required
        allclass.views.allclass_update
        """
	testallclass = Allclass.objects.get(allclass_name='TestClass')
	testallclassid = testallclass.id
	requesturl = reverse(url_name, kwargs={'pk':testallclassid})
	response = self.client.post(requesturl)
	self.assertEqual(response.status_code, 302)

        #ToDo should return /login/?blah Check that

        """
        Logged in user unable to update id that doesnt exist, shoulw raise 404
	allclass.views.allclass_update
        """
        self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser1', password='hello')
        login = self.c.login(username='testuser1', password='hello')
        requesturl = reverse(url_name, kwargs={'pk':42})
        response = self.c.post(requesturl)
        self.assertEqual(response.status_code, 404)

        """
        Logged in usere should be able to update a valid user's details and return usertable
        allclass.views..allclass_update
        """
        self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser1', password='hello')
        login = self.c.login(username='testuser1', password='hello')

	testallclass = Allclass.objects.get(allclass_name='TestClass')
	testallclassid = testallclass.id

        self.c.get(url_name,kwargs={'pk':testallclassid})
        requesturl = reverse(url_name, kwargs={'pk':testallclassid})
        response = self.c.post(requesturl, post_data_changes)
	print("RESPONSE FOR CHANGE:")
	changedvalue=Allclass.objects.get(allclass_name="TestClass").allclass_location
	print(Allclass.objects.get(allclass_name="TestClass").allclass_desc);
        #self.assertEqual('ChangedTestville', changedvalue)
        #self.assertRedirects(response, '/allclassestable/')

    def test_delete(self):
	student_list_ids=[3,4]
        post_data={'class_name':'TestClass','class_desc':'Class created by unit testing','class_location':'Testville','schoolid':1,'teacherid':2,'target': student_list_ids}

        self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser1', password='hello')
        login = self.c.login(username='testuser1', password='hello')

        requesturl = reverse('allclass_new')
        response = self.c.post(requesturl, post_data)
        test_create_user = Allclass.objects.get(allclass_name="TestClass")
        print("Test Dat for test_delete:")
        print(Allclass.objects.all())

	view_name="allclass_delete"
	"""
	User logged in should be able to delete user
	allclass.views.user_delete
	"""
	self.c = Client();
	self.user = User.objects.get(username="testuser1")
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser1', password='hello')
        login = self.c.login(username='testuser1', password='hello')

	testallclass = Allclass.objects.get(allclass_name='TestClass')
	testallclassid = testallclass.id

	print("ALLCLASSES BEFORE")
	print(Allclass.objects.all())

	requesturl = reverse(view_name, kwargs={'pk':testallclassid})	
	response = self.c.get(requesturl)
	self.assertEquals(response.status_code, 200)
	print("ALLCLASSES AFTER")
	print(Allclass.objects.all())
	
	
	"""
	Logged in user deleting unknown allclass: 404
	allclass.views.allclass_delete
	"""
	
	self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser1', password='hello')
        login = self.c.login(username='testuser1', password='hello')

	requesturl = reverse(view_name, kwargs={'pk':42})
        response = self.c.get(requesturl)
        self.assertEqual(response.status_code, 404)

	
	
    
    def tearDown(self):
	print("end of AllClass tests")

	
	
	
