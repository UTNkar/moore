# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-02 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('involvement', '0007_auto_20170427_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='election_email',
            field=models.EmailField(default='styrelsen@utn.se', help_text='The email address to contact for more information regarding the role.', max_length=254, verbose_name='Election contact email address'),
        ),
    ]
