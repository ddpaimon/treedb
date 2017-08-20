# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse

from .models import Node

# Create your views here.


def index(request):
    print(request)
    all_nodes = Node.objects.all()
    template = loader.get_template('treesite/index.html')
    context = {
        'nodes': all_nodes,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    node = get_object_or_404(Node, pk=question_id)
    return render(request, 'treesite/detail.html', {'node': node})


def free(request):
    return HttpResponse(request)
