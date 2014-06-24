# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('uploadeXe.views',
    url(r'^list/$', 'list', name='list'),
    url(r'^manage/$', 'manage', name='manage'),
    url(r'^new/$', 'new', name='new'),
    url(r'^edit/(?P<pk>\d+)$', 'edit', name='edit'),
)
