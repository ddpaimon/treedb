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
    # url(r'^tree/$', views.tree, name='tree'),
    url(r'^tree/(?P<node_id>[0-9]+)/subtree/$', views.subtree, name='subtree'),
    url(r'^tree/$', views.tree, name='tree'),
    url(r'^tree/(?P<node_id>[0-9]+)/$', views.node, name='node'),
    url(r'^tree/update/$', views.update, name='tree_update'),
    url(r'^free/$', views.free, name='free'),
]
