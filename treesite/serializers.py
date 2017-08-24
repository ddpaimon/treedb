# -*- coding: utf-8 -*-

from .models import Node
from rest_framework import serializers

# Create your serializers here.


def serialize(func, node):
    pass


def to_json(node):
    """
    Serialize subtree to json object.
    :param node: Node
    :return:
    """
    data = NodeSerializer(node).data
    data["children"] = list()
    children = Node.objects.filter(root=node.id)
    # for child in children.iterator():
    #     print(child)
    if children.exists():
        for child in children.iterator():
            data["children"].append(to_json(child))
    return data


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ("id", "root", "name", "deleted")
