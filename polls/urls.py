# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

# Create your urls here.

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
