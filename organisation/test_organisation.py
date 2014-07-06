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
from organisation.models import UMCloud_Package as Subscription
from organisation.models import User_Organisations
from school.models import School
from allclass.models import Allclass
from uploadeXe.models import Role
from uploadeXe.models import User_Roles
from django import forms


"""
class UMCloud_Package(models.Model):
   package_name = models.CharField(max_length=300)
   package_desc = models.CharField(max_length=2000)
   max_students = models.IntegerField()
   max_publishers = models.IntegerField()
   price_rate_permonth = models.FloatField()

class Organisation(models.Model):
   organisation_name = models.CharField(max_length=300)
   organisation_desc = models.CharField(max_length=1000)
   add_date = models.DateTimeField(default=datetime.datetime.now)
   set_package = models.ForeignKey(UMCloud_Package)


"""

class OrganisationViewTestCase(TestCase):
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
	mainorganisation = Organisation.objects.get(pk=1)
	user_organisation1 = User_Organisations(user_userid=testuser1, organisation_organisationid=mainorganisation)
	user_organisation1.save()

	subscription1=Subscription.objects.create(package_name="TestingPackage", package_desc="This is the Unit Test Package", max_students=15, max_publishers=2, price_rate_permonth=0.05)
	subscription1.save()

	organisation1 = Organisation.objects.create(organisation_name='TestingOrganisation', organisation_desc='This is the testing organisation', add_date='2014-07-07',set_package=subscription1)
	organisation1.save()

	

    def test_organisation_create(self):
	"""
	Users can create organisations
	organisation.views.organisation_create
	"""
	setpackage = Subscription.objects.get(pk=1)
	url_name="organisation_new"
	post_data_create={'organisation_name':'TestingOrganisation2','organisation_desc':'Test to create TestingOrganisation2','add_date':'2014-07-07', 'umpackageid':1}
	
	"""
	Organisations cannot be created without logging in 
	organisation.views.organisation_create
	"""
        requesturl = reverse(url_name)
        response = self.client.post(requesturl, post_data_create)
	self.assertEqual(response.status_code, 302)

	"""
	Organisation can be created with logging in
	organisation.views.organisation_create
	"""
	self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser1', password='hello')
        login = self.c.login(username='testuser1', password='hello')

	requesturl = reverse(url_name)
	response = self.c.post(requesturl, post_data_create)
	updatedorganisation = Organisation.objects.get(organisation_name="TestingOrganisation2")
	changedvalue=updatedorganisation.organisation_name
	self.assertEqual("TestingOrganisation2",changedvalue)

    @unittest.expectedFailure
    def test_school_create_failure(self):
	"""
	Incorrectly done model fails for logged in user
	organisation.views.organisation_create
	"""
	setpackage=Subscription.objects.get(pk=1)
	url_name="organisation_new"
	post_data_create_incorrect={'organisation_name':'','organisation_desc':'Incorrect Test to create TestingOrganisation2','add_date':'2014-07-07', 'umpackageid':setpackage}


        self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser1', password='hello')
        login = self.c.login(username='testuser1', password='hello')

        requesturl = reverse(url_name)
        response = self.c.post(requesturl, post_data_create_incorrect)
        self.assertEqual("TestingOrganisation2", Organisation.objects.get(organisation_name="TestingOrganisation2").organisation_name)

    def test_update(self):
        view_name='organisation_edit'
	setpackage=Subscription.objects.get(pk=1)
	post_data_update={'organisation_name':'TestingOrganisation','organisation_desc':'This is an update to Test to create TestingOrganisation','add_date':'2014-07-07', 'set_package':1}

        """
        Login required
	organisation.views.organisation_edit
        """

	testingorganisation = Organisation.objects.get(organisation_name='TestingOrganisation')
	testingorganisationid = testingorganisation.id;

	requesturl = reverse(view_name, kwargs={'pk':testingorganisationid})	
	response = self.client.post(requesturl)
	#ToDO: should check for return ./login/?blah 
        self.assertEqual(response.status_code, 302)

        """
        Logged in user unable to update id that doesnt exist, shoulw raise 404
	organisation.views.organisation_edit
        """
        self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser1', password='hello')
        login = self.c.login(username='testuser1', password='hello')

        requesturl = reverse(view_name, kwargs={'pk':42})
        response = self.c.post(requesturl)
        self.assertEqual(response.status_code, 404)

        """
        Logged in usere should be able to update a valid organisation's details and return organisationstable
        organisation.views.organisation_edit
        """
        self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser1', password='hello')
        login = self.c.login(username='testuser1', password='hello')

	testingorganisation = Organisation.objects.get(organisation_name='TestingOrganisation')
	testingorganisationid = testingorganisation.id;
	
        self.c.get(view_name,kwargs={'pk':testingorganisationid})
        requesturl = reverse(view_name, kwargs={'pk':testingorganisationid})
        response = self.c.post(requesturl, post_data_update)

	changedvalue = Organisation.objects.get(organisation_name='TestingOrganisation').organisation_desc
        self.assertEqual('This is an update to Test to create TestingOrganisation', changedvalue)
        self.assertRedirects(response, '/organisationstable/')


    def test_delete(self):
        view_name='organisation_delete'
        """
        User logged in should be able to delete Organisation
	organisation.views.organisation_delete
        """
        self.c = Client();
        self.user = User.objects.get(username="testuser1")
        self.user.set_password('hello')
        self.user.save()
        self.user = authenticate(username='testuser1', password='hello')
        login = self.c.login(username='testuser1', password='hello')

	testingorganisation = Organisation.objects.get(organisation_name='TestingOrganisation')
	testingorganisationid = testingorganisation.id

        requesturl = reverse(view_name, kwargs={'pk':testingorganisationid})
        response = self.c.get(requesturl)
        self.assertEquals(response.status_code,200)

        """
        Logged in user deleting unknown user: 4040
	school.views.school_delete
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
	print("end of Organiation Tests")

	
	
	
