# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-20 11:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('treesite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='root',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='treesite.Node', verbose_name='parent'),
        ),
    ]
