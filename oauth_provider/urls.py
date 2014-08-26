from django.conf.urls import *
#changed from :
#from django.conf.urls.default import * # Reason: This is depreciates.

from views import request_token, user_authorization, access_token, oauth_home

urlpatterns = patterns('',
	url(r'^$', oauth_home, name='oauth_home'),
    url(r'^initiate',    request_token,      name='oauth_request_token'),
    url(r'^authorize',        user_authorization, name='oauth_user_authorization'),
    url(r'^token',     access_token,       name='oauth_access_token'),
)
