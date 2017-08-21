# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Node(models.Model):
    name = models.CharField(max_length=20)
    root = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='parent', related_name='child', blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def get_children(self):
        return self.objects.all()