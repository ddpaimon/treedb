# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

# Create your urls here.

app_name = 'treesite'
urlpatterns = [
    url(r'^(?P<node_id>[0-9]+)/subtree/$', views.subtree, name='subtree'),
    url(r'^$', views.tree, name='tree'),
    url(r'^(?P<node_id>[0-9]+)/$', views.node, name='node'),
    url(r'^update/$', views.update, name='tree_update'),
    url(r'^clear/$', views.clear, name='tree_clear'),
]
