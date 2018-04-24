# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-12 09:46
from __future__ import unicode_literals

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0003_auto_20170711_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googleformpage',
            name='results_en',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.images.blocks.ImageChooserBlock(group='Basic', template='blocks/image.html')), ('heading', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('subtitle', wagtail.core.blocks.CharBlock(required=False))))), ('image_description', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock()))))), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.core.blocks.StructBlock((('description', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)), ('link', wagtail.core.blocks.URLBlock(required=False)), ('button', wagtail.core.blocks.CharBlock(required=False))))), ('logos', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), group='Noyce', icon='fa-pied-piper', label='Logos', template='blocks/logos.html')), ('counters', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('counters', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock(required=False)))))), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.core.blocks.StructBlock((('columns', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('width', wagtail.core.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.core.blocks.StreamBlock((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.images.blocks.ImageChooserBlock(group='Basic', template='blocks/image.html'))))))))),))), ('person', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('name', wagtail.core.blocks.CharBlock()), ('role', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('email', wagtail.core.blocks.EmailBlock(required=False)))))), blank=True),
        ),
        migrations.AlterField(
            model_name='googleformpage',
            name='results_sv',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.images.blocks.ImageChooserBlock(group='Basic', template='blocks/image.html')), ('heading', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('subtitle', wagtail.core.blocks.CharBlock(required=False))))), ('image_description', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock()))))), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.core.blocks.StructBlock((('description', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)), ('link', wagtail.core.blocks.URLBlock(required=False)), ('button', wagtail.core.blocks.CharBlock(required=False))))), ('logos', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), group='Noyce', icon='fa-pied-piper', label='Logos', template='blocks/logos.html')), ('counters', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('counters', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock(required=False)))))), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.core.blocks.StructBlock((('columns', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('width', wagtail.core.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.core.blocks.StreamBlock((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.images.blocks.ImageChooserBlock(group='Basic', template='blocks/image.html'))))))))),))), ('person', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('name', wagtail.core.blocks.CharBlock()), ('role', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('email', wagtail.core.blocks.EmailBlock(required=False)))))), blank=True),
        ),
    ]
