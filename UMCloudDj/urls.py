#from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

#urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'UMCloudDj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
#)

# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib import admin

#UMCloudDj.uploadeXe

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url='/userstable/')), # Just for ease of use.
	url(r'^upload/', 'UMCloudDj.views.upload_view'),
	url(r'^management/', 'UMCloudDj.views.management_view'),
	url(r'^reports/', 'UMCloudDj.views.reports_view'),

	url(r'^getreportzambia/', 'UMCloudDj.views.get_report_zambia'),
	url(r'getreportstatements/', 'UMCloudDj.views.get_report_statements'),
        url(r'statementsreports/$', 'UMCloudDj.views.report_statements_view'),
	url(r'^mcqreports/$', 'UMCloudDj.views.report_selection_view', name='mcqreports'),
	url(r'^sendtestlog/$', 'UMCloudDj.views.sendtestlog_view', name='sendtestlog'),
	url(r'^sendelpfile/$', 'UMCloudDj.views.sendelpfile_view', name='sendelpfile'),
	url(r'^checklogin/$', 'UMCloudDj.views.checklogin_view', name='checklogin'),
	url(r'^getassignedcourseids/$', 'UMCloudDj.views.getassignedcourseids_view', name='getassignedcourseids'),
	#url(r'^testelpfiles/$', 'UMCloudDj.views.testelpfiles_view', name='testelpfiles'),
	#url(r'^selectelptest/$', 'UMCloudDj.views.elptestresults_selection_view', name='showelptestresults_selection'),
        #url(r'^selectapptest/$', 'UMCloudDj.views.apptestresults_selection_view', name='showappunittestresults_selection'),
	#url(r'^elptestresults/$', 'UMCloudDj.views.showelptestresults_view', name='showelptestresults'),
	#url(r'^apptestresults/$', 'UMCloudDj.views.showappunittestresults_view', name='showappunittestresults'),
	url(r'^getcourse/$', 'UMCloudDj.views.getcourse_view', name='getcourse'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^login/', 'UMCloudDj.views.loginview', name='login'),
	url(r'^auth/', 'UMCloudDj.views.auth_and_login'),
        url(r'^signup/', 'UMCloudDj.views.sign_up_in'),
        url(r'^home/$', 'UMCloudDj.views.secured'),
	url(r'^logout/$', 'UMCloudDj.views.logout_view'),
	url(r'^register/$', 'UMCloudDj.views.register_view', name='register'),

	#url(r'^roles/$', 'UMCloudDj.views.role_list', name='role_list'),
	url(r'^rolestable/$', 'UMCloudDj.views.role_table', name='role_table'),
  	url(r'^rolenew/$', 'UMCloudDj.views.role_create', name='role_new'),
  	url(r'^roleedit/(?P<pk>\d+)$', 'UMCloudDj.views.role_update', name='role_edit'),
  	url(r'^roledelete/(?P<pk>\d+)$', 'UMCloudDj.views.role_delete', name='role_delete'),

	#url(r'^users/$', 'UMCloudDj.views.user_list', name='user_list'),
	url(r'^userstable/$', 'UMCloudDj.views.user_table', name='user_table'),
	url(r'^usersapprove/$','UMCloudDj.views.admin_approve_request', name='users_approve'),
 	#url(r'^userapprove/(?P<pk>\d+)$', 'UMCloudDj.views.user_approve_request', name='user_approve'),
        url(r'^usernew/$', 'UMCloudDj.views.user_create', name='user_new'),
        url(r'^useredit/(?P<pk>\d+)$', 'UMCloudDj.views.user_update', name='user_edit'),
        url(r'^userdelete/(?P<pk>\d+)$', 'UMCloudDj.views.user_delete', name='user_delete'),

	#url(r'^organisations/$', 'organisation.views.organisation_list', name='organisation_list'),
	url(r'^organisationstable/$', 'organisation.views.organisation_table', name='organisation_table'),
        url(r'^organisationnew/$', 'organisation.views.organisation_create', name='organisation_new'),
        url(r'^organisationedit/(?P<pk>\d+)$', 'organisation.views.organisation_update', name='organisation_edit'),
        url(r'^organisationdelete/(?P<pk>\d+)$', 'organisation.views.organisation_delete', name='organisation_delete'),

	#url(r'^umpackages/$', 'organisation.views.umpackage_list', name='umpackage_list'),
	url(r'^umpackagestable/$', 'organisation.views.umpackage_table', name='umpackage_table'),
        url(r'^umpackagenew/$', 'organisation.views.umpackage_create', name='umpackage_new'),
        url(r'^umpackageedit/(?P<pk>\d+)$', 'organisation.views.umpackage_update', name='umpackage_edit'),
        url(r'^umpackagedelete/(?P<pk>\d+)$', 'organisation.views.umpackage_delete', name='umpackage_delete'),

	#url(r'^schools/$', 'school.views.school_list', name='school_list'),
	url(r'^schoolstable/$', 'school.views.school_table', name='school_table'),
        url(r'^schoolnew/$', 'school.views.school_create', name='school_new'),
        url(r'^schooledit/(?P<pk>\d+)$', 'school.views.school_update', name='school_edit'),
        url(r'^schooldelete/(?P<pk>\d+)$', 'school.views.school_delete', name='school_delete'),

	#url(r'^allclasses/$', 'allclass.views.allclass_list', name='allclass_list'),
	url(r'^allclassestable/$', 'allclass.views.allclass_table', name='allclass_table'),
        url(r'^allclassnew/$', 'allclass.views.allclass_create', name='allclass_new'),
        url(r'^allclassedit/(?P<pk>\d+)$', 'allclass.views.allclass_update', name='allclass_edit'),
        url(r'^allclassdelete/(?P<pk>\d+)$', 'allclass.views.allclass_delete', name='allclass_delete'),

	#url(r'^dynatableroles/$', 'UMCloudDj.views.role_dynatable', name='role_dynatable'),


	#url(r'^progressbarupload/', include('progressbarupload.urls')),

 	#For upload feature. Need both for file upload. The second one re directs to the url and first one does somehting related to that. 
	(r'^uploadeXe/', include('uploadeXe.urls')),
	(r'^uploadeXe/$', RedirectView.as_view(url='/uploadeXe/list/')), # Just for ease of use.
	(r'^manageeXe/$', RedirectView.as_view(url='/uploadeXe/manage/')),
	(r'^managecourses/$',RedirectView.as_view(url='/uploadeXe/managecourses/')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

