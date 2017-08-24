# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse, JsonResponse

from .models import Node
from .serializers import NodeSerializer
from . import serializers

from rest_framework.decorators import api_view

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


@api_view(['GET'])
def node(request, node_id):
    node_object = Node.objects.get(id=node_id)
    node_ser = NodeSerializer(node_object)
    return JsonResponse(node_ser.data)


@api_view(['GET'])
def tree(requets):
    q_all_root = Node.objects.filter(root=None)
    print(q_all_root)
    tree_data = {'tree': list()}
    if q_all_root.exists():
        for root_node in q_all_root.iterator():
            tree_data['tree'].append(serializers.to_json(root_node))
    return JsonResponse(tree_data)


@api_view(['GET'])
def subtree(request, node_id):
    node_data = get_object_or_404(Node, id=node_id)
    result_data = serializers.to_json(node_data)
    return JsonResponse(result_data)


@api_view(['POST'])
def update(request):
    tree_data = request.data
    read_tree(tree_data['tree'])
    return JsonResponse(tree_data)


def read_tree(tree_data):
    res = list()
    for root_node in tree_data:
        res.append(read_subtree(root_node))


def read_subtree(node_data):
    children_data = node_data['children']
    node_data.pop('children', None)
    res = update_or_create_node(node_data)
    print(res)
    res['children'] = list()
    for child_data in children_data:
        res['children'].append(read_subtree(child_data))
    return res


def update_or_create_node(node_data):
    node_ser = NodeSerializer(data=node_data)
    if node_ser.is_valid():
        if node_data['id'] is None:
            create_node(node_data)
        else:
            update_node(node_data)
    return node_data


def create_node(node_data):
    # node_object = Node(**node_data)
    # parent_node = Node.objects.get(id=node_object.root)
    # if parent_node.deleted: node_object.deleted = parent_node.deleted
    # node_object.save()
    pass


def update_node(node_data):
    # node = Node.objects.get(id=node_data['id'])
    pass


def delete_node(node_data):
    # node_object = Node.objects.get(id=node_data['id'])
    pass
