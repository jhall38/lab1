# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-31 09:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urlexpander', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='shortened_url',
            new_name='shortend_url',
        ),
    ]