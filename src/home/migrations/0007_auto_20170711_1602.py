# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-11 14:02
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20170630_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body_en',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(group='Basic', template='blocks/image.html')), ('heading', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('image_description', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('image_alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailcore.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))), ('hide_on_med', wagtail.wagtailcore.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.wagtailcore.blocks.StructBlock((('description', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('image_alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.wagtailcore.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('description', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('button', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('logos', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailimages.blocks.ImageChooserBlock(), group='Noyce', icon='fa-pied-piper', label='Logos', template='blocks/logos.html')), ('counters', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('counters', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailcore.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.wagtailcore.blocks.CharBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock(required=False)))))), ('style', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.wagtailcore.blocks.StructBlock((('columns', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('width', wagtail.wagtailcore.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.wagtailcore.blocks.StreamBlock((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(group='Basic', template='blocks/image.html'))))))))),))), ('news', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('index', wagtail.wagtailcore.blocks.PageChooserBlock(target_model=['news.NewsIndexPage'])), ('items', wagtail.wagtailcore.blocks.IntegerBlock()))))), blank=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body_sv',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(group='Basic', template='blocks/image.html')), ('heading', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('image_description', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('image_alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailcore.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))), ('hide_on_med', wagtail.wagtailcore.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.wagtailcore.blocks.StructBlock((('description', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('image_alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.wagtailcore.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('description', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('button', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('logos', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailimages.blocks.ImageChooserBlock(), group='Noyce', icon='fa-pied-piper', label='Logos', template='blocks/logos.html')), ('counters', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('counters', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailcore.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.wagtailcore.blocks.CharBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock(required=False)))))), ('style', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.wagtailcore.blocks.StructBlock((('columns', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('width', wagtail.wagtailcore.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.wagtailcore.blocks.StreamBlock((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(group='Basic', template='blocks/image.html'))))))))),))), ('news', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('index', wagtail.wagtailcore.blocks.PageChooserBlock(target_model=['news.NewsIndexPage'])), ('items', wagtail.wagtailcore.blocks.IntegerBlock()))))), blank=True),
        ),
        migrations.AlterField(
            model_name='webpage',
            name='body_en',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(group='Basic', template='blocks/image.html')), ('heading', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('image_description', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('image_alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailcore.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))), ('hide_on_med', wagtail.wagtailcore.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.wagtailcore.blocks.StructBlock((('description', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('image_alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.wagtailcore.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('description', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('button', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('logos', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailimages.blocks.ImageChooserBlock(), group='Noyce', icon='fa-pied-piper', label='Logos', template='blocks/logos.html')), ('counters', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('counters', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailcore.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.wagtailcore.blocks.CharBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock(required=False)))))), ('style', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.wagtailcore.blocks.StructBlock((('columns', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('width', wagtail.wagtailcore.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.wagtailcore.blocks.StreamBlock((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(group='Basic', template='blocks/image.html'))))))))),))), ('google_form', wagtail.wagtailcore.blocks.StructBlock((('form_id', wagtail.wagtailcore.blocks.CharBlock()), ('height', wagtail.wagtailcore.blocks.IntegerBlock())))), ('google_drive', wagtail.wagtailcore.blocks.StructBlock((('folder_id', wagtail.wagtailcore.blocks.CharBlock()), ('view', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('list', 'List'), ('grid', 'Grid')])), ('height', wagtail.wagtailcore.blocks.IntegerBlock())))), ('news', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('index', wagtail.wagtailcore.blocks.PageChooserBlock(target_model=['news.NewsIndexPage'])), ('items', wagtail.wagtailcore.blocks.IntegerBlock()))))), blank=True),
        ),
        migrations.AlterField(
            model_name='webpage',
            name='body_sv',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(group='Basic', template='blocks/image.html')), ('heading', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('image_description', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('image_alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailcore.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))), ('hide_on_med', wagtail.wagtailcore.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.wagtailcore.blocks.StructBlock((('description', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('image_alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.wagtailcore.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('description', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('button', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('logos', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailimages.blocks.ImageChooserBlock(), group='Noyce', icon='fa-pied-piper', label='Logos', template='blocks/logos.html')), ('counters', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('counters', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('icon', wagtail.wagtailcore.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.wagtailcore.blocks.CharBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock(required=False)))))), ('style', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.wagtailcore.blocks.StructBlock((('columns', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('width', wagtail.wagtailcore.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.wagtailcore.blocks.StreamBlock((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(group='Basic', template='blocks/image.html'))))))))),))), ('google_form', wagtail.wagtailcore.blocks.StructBlock((('form_id', wagtail.wagtailcore.blocks.CharBlock()), ('height', wagtail.wagtailcore.blocks.IntegerBlock())))), ('google_drive', wagtail.wagtailcore.blocks.StructBlock((('folder_id', wagtail.wagtailcore.blocks.CharBlock()), ('view', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('list', 'List'), ('grid', 'Grid')])), ('height', wagtail.wagtailcore.blocks.IntegerBlock())))), ('news', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('index', wagtail.wagtailcore.blocks.PageChooserBlock(target_model=['news.NewsIndexPage'])), ('items', wagtail.wagtailcore.blocks.IntegerBlock()))))), blank=True),
        ),
    ]