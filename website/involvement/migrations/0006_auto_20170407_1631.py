# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 14:31
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('involvement', '0005_auto_20170403_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='removed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='recruitmentpage',
            name='included_teams',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, help_text='Choose teams to include on the page. This overrulesexcluded teams', related_name='include_on_page', to='involvement.Team', verbose_name='Included teams'),
        ),
    ]
