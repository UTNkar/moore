# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-27 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('involvement', '0006_auto_20170407_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='email',
        ),
        migrations.RemoveField(
            model_name='team',
            name='leader_en',
        ),
        migrations.RemoveField(
            model_name='team',
            name='leader_sv',
        ),
        migrations.AddField(
            model_name='role',
            name='election_email',
            field=models.EmailField(blank=True, help_text='The email address to contact for more information regarding the role.', max_length=254, verbose_name='Election contact email address'),
        ),
        migrations.AlterField(
            model_name='application',
            name='cover_letter',
            field=models.TextField(blank=True, help_text='Present yourself and state why you are who we are looking for', verbose_name='Cover Letter'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='email',
            field=models.EmailField(blank=True, help_text='Enter an email address on which your reference in reachable', max_length=254, verbose_name='email address'),
        ),
    ]
