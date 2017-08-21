# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from . import views

from . import views

# Create your urls here.

app_name = 'treesite'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/children/$', views.children, name='children'),
    url(r'^free/$', views.free, name='free')
]
