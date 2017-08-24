# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse, JsonResponse

from .models import Node
from .serializers import NodeSerializer
from . import serializers

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


def children(request, question_id):
    children_list = Node.objects.filter(root=question_id)
    template = loader.get_template('treesite/children.html')
    context = {
        'children': children_list
    }
    return HttpResponse(template.render(context, request))


def free(request):
    return HttpResponse(request)


def tree(request, node_id):
    node = Node.objects.get(id=node_id)
    result_data = serializers.to_json(node)
    return JsonResponse(result_data, safe=False)
