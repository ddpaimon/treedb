# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import Node
from .serializers import NodeSerializer
from . import serializers

from rest_framework.decorators import api_view

from .events import EventsManager

import time

# Create your views here.

testing = False
events_manager = EventsManager()


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


@api_view(['GET'])
def clear(request):
    """
    Remove all nodes from database
    :param request:
    :return:
    """
    Node.objects.all().delete()
    return JsonResponse({'response': 'clear'})


@api_view(['GET'])
def node(request, node_id):
    """
    Return node detail
    :param request:
    :param node_id:
    :return:
    """
    node_object = Node.objects.get(id=node_id)
    node_ser = NodeSerializer(node_object)
    return JsonResponse(node_ser.data)


@api_view(['GET'])
def tree(requets):
    """
    Return all tree from database
    :param requets:
    :return:
    """
    q_all_root = Node.objects.filter(root=None)
    # print(q_all_root)
    tree_data = {'tree': list()}
    if q_all_root.exists():
        for root_node in q_all_root.iterator():
            tree_data['tree'].append(serializers.to_json(root_node))
    return JsonResponse(tree_data)


@api_view(['GET'])
def subtree(request, node_id):
    """
    Return subtree started from target node
    :param request:
    :param node_id:
    :return:
    """
    node_data = get_object_or_404(Node, id=node_id)
    result_data = serializers.to_json(node_data)
    return JsonResponse(result_data)


@api_view(['POST'])
@timeit
def update(request):
    """
    Update, create and remove subtrees
    :param request:
    :return:
    """
    tree_data = request.data
    db_node_objects = Node.objects
    updating_tree_data = read_tree(update_or_create_node, tree_data, db_node_objects)
    db_node_objects = Node.objects
    resulting_tree_data = read_tree(update_deleted, updating_tree_data, db_node_objects)
    return JsonResponse({'tree': resulting_tree_data})


@api_view(['POST'])
def update_events(request):
    """
    Update tree with events
    :param request:
    :return:
    """
    events_data = request.data
    events_manager.deserialize_event(events_data)
    # print(events_manager.serialize_events())
    events_manager.apply()
    return JsonResponse({'nodes': []})


def read_tree(func, tree_data, db_node_objects):
    """
    Recursive read forest
    :param func:
    :param tree_data:
    :param db_node_objects:
    :return:
    """
    res = list()
    for root_node in tree_data:
        res.append(read_subtree(func, root_node, db_node_objects))
    return res


def read_subtree(func, root_node, db_node_objects, root_id=None):
    """
    Recursive read subtree
    :param func:
    :param root_node:
    :param db_node_objects:
    :return:
    """
    node_data = root_node
    res = dict()
    res['node'] = func(node_data['node'], db_node_objects, root_id)
    res['children'] = list()
    for child_data in root_node['children']:
        res['children'].append(read_subtree(func, child_data, db_node_objects, res['node']['id']))
    return res


def update_deleted(node_data, db_node_objects, root_id=None):
    if 'id' not in node_data or node_data['id'] is not None:
        node_object = db_node_objects.get(id=node_data['id'])
        node_data['deleted'] = node_object.deleted
    return node_data


def update_or_create_node(node_data, db_node_objects, root_id):
    if 'id' not in node_data or node_data['id'] is None or not db_node_objects.filter(id=node_data['id']).exists():
        node_data['id'] = None
        node_data['root'] = None
        node_ser = NodeSerializer(data=node_data)
        if node_ser.is_valid():
            if node_data['deleted'] is False:
                node_data = create_node(node_data, db_node_objects, root_id=root_id)
    else:
        print(node_data)
        node_ser = NodeSerializer(data=node_data)
        if node_ser.is_valid():
            node_data = update_node(node_data, db_node_objects)
    return node_data


def create_node(node_data, db_node_objects, root_id):
    node_object = Node()
    node_object.deleted = node_data['deleted']
    node_object.name = node_data['name']
    parent_node = db_node_objects.get(id=root_id) if root_id is not None else root_id
    node_object.root = parent_node
    if parent_node is not None:
        if parent_node.deleted:
            node_object.deleted = parent_node.deleted
    if not testing:
        node_object.save()
    node_data = NodeSerializer(node_object).data
    return node_data


def update_node(node_data, db_node_objects):
    node_object = db_node_objects.get(id=node_data['id'])
    if node_object.name != node_data['name']:
        node_object.name = node_data['name']
        if not testing:
            node_object.save()
    if node_data['deleted'] and node_object.deleted != node_data['deleted']:
        delete_subtree(node_object, db_node_objects)
    node_data = NodeSerializer(node_object).data
    return node_data


def delete_subtree(node_object, db_node_objects):
    node_object.deleted = True
    if not testing:
        node_object.save()
    node_children = db_node_objects.filter(root=node_object.id)
    if node_children.exists():
        for child in node_children.iterator():
            delete_subtree(child, db_node_objects)
