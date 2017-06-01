# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 12:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('title_en', models.CharField(blank=True, help_text='Enter the title to be shown on the banner.', max_length=255, verbose_name='English banner title')),
                ('title_sv', models.CharField(blank=True, help_text='Enter the title to be shown on the banner.', max_length=255, verbose_name='Swedish banner title')),
                ('text_en', models.TextField(blank=True, help_text='Enter a text to be shown on the banner.', verbose_name='English banner text')),
                ('text_sv', models.TextField(blank=True, help_text='Enter a text to be shown on the banner.', verbose_name='Swedish banner text')),
                ('link', models.URLField(blank=True, verbose_name='Button URL')),
                ('button_en', models.TextField(blank=True, help_text='Enter the text to be displayed on the button.', verbose_name='English button text')),
                ('button_sv', models.TextField(blank=True, help_text='Enter the text to be displayed on the button.', verbose_name='Swedish button text')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='homepage',
            name='body_en',
            field=wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image_description', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('image_alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailcore.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))), ('hide_on_med', wagtail.wagtailcore.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.wagtailcore.blocks.StructBlock((('description', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('image_alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.wagtailcore.blocks.BooleanBlock(required=False))))), ('counters', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('counters', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailcore.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.wagtailcore.blocks.CharBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock(required=False)))))), ('style', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(template='blocks/image.html'))), blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='body_sv',
            field=wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image_description', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('image_alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailcore.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))), ('hide_on_med', wagtail.wagtailcore.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.wagtailcore.blocks.StructBlock((('description', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('image_alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.wagtailcore.blocks.BooleanBlock(required=False))))), ('counters', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('counters', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailcore.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.wagtailcore.blocks.CharBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock(required=False)))))), ('style', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(template='blocks/image.html'))), blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='title_sv',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banner',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='banners', to='home.HomePage'),
        ),
    ]
