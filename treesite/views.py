# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse, JsonResponse

from .models import Node
from .serializers import NodeSerializer
from . import serializers

from rest_framework.decorators import api_view

import time

# Create your views here.

testing = False


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed


def index(request):
    print(request)
    all_nodes = Node.objects.all()
    template = loader.get_template('treesite/index.html')
    context = {
        'nodes': all_nodes,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    node_object = get_object_or_404(Node, pk=question_id)
    return render(request, 'treesite/detail.html', {'node': node_object})


def children(request, question_id):
    children_list = Node.objects.filter(root=question_id)
    template = loader.get_template('treesite/children.html')
    context = {
        'children': children_list
    }
    return HttpResponse(template.render(context, request))


def free(request):
    objs = Node.objects
    all = objs.all()
    print(all)
    n1 = objs.get(id=1)
    print(n1)
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
    tree_data = request.data['tree']
    db_node_objects = Node.objects
    updating_tree_data = read_tree(update_or_create_node, tree_data, db_node_objects)
    db_node_objects = Node.objects
    resulting_tree_data = read_tree(update_deleted, updating_tree_data, db_node_objects)
    return JsonResponse({'tree': resulting_tree_data})


def read_tree(func, tree_data, db_node_objects):
    res = list()
    for root_node in tree_data:
        res.append(read_subtree(func, root_node, db_node_objects))
    return res


def read_subtree(func, node_data, db_node_objects):
    children_data = node_data['children']
    node_data.pop('children', None)
    res = func(node_data, db_node_objects)
    res['children'] = list()
    for child_data in children_data:
        res['children'].append(read_subtree(func, child_data, db_node_objects))
    # print("Result: ", res)
    return res

@timeit
def update_deleted(node_data, db_node_objects):
    if node_data['id'] is not None:
        node_object = db_node_objects.get(id=node_data['id'])
        node_data['deleted'] = node_object.deleted
    return node_data


def update_or_create_node(node_data, db_node_objects):
    node_ser = NodeSerializer(data=node_data)
    if node_ser.is_valid():
        if node_data['id'] is None:
            node_data = create_node(node_data, db_node_objects)
        else:
            node_data = update_node(node_data, db_node_objects)
    return node_data

@timeit
def create_node(node_data, db_node_objects):
    # print("Create node: ", node_data['name'])
    node_object = Node()
    node_object.deleted = node_data['deleted']
    node_object.name = node_data['name']
    parent_node = db_node_objects.get(id=node_data['root'])
    node_object.root = parent_node
    if parent_node.deleted:
        node_object.deleted = parent_node.deleted
    if not testing:
        node_object.save()
    node_data = NodeSerializer(node_object).data
    return node_data

@timeit
def update_node(node_data, db_node_objects):
    # print("Update node: ", node_data['name'])
    node_object = db_node_objects.get(id=node_data['id'])
    if node_object.name != node_data['name']:
        node_object.name = node_data['name']
        if not testing:
            node_object.save()
    if node_data['deleted'] and node_object.deleted != node_data['deleted']:
        delete_subtree(node_object, db_node_objects)
    node_data = NodeSerializer(node_object).data
    return node_data

@timeit
def delete_subtree(node_object, db_node_objects):
    node_object.deleted = True
    if not testing:
        node_object.save()
    node_children = db_node_objects.filter(root=node_object.id)
    if node_children.exists:
        for child in node_children.iterator():
            delete_subtree(child, db_node_objects)
