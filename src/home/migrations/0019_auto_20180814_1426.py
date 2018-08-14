# Generated by Django 2.0.5 on 2018-08-14 12:26

from django.db import migrations
import google.models
import involvement.blocks.contact_card_block
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20180813_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formpage',
            name='intro_en',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1))))), ('heading', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('subtitle', wagtail.core.blocks.CharBlock(required=False))))), ('image_description', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock()))))), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.core.blocks.StructBlock((('description', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)), ('text_color', wagtail.core.blocks.ChoiceBlock(choices=[('text-light', 'Light'), ('text-dark', 'Dark')])), ('link', wagtail.core.blocks.URLBlock(required=False)), ('button', wagtail.core.blocks.CharBlock(required=False))))), ('logos', wagtail.core.blocks.StructBlock((('logos', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.core.blocks.URLBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)))))),))), ('counters', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('counters', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock(required=False)))))), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.core.blocks.StructBlock((('columns', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('width', wagtail.core.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.core.blocks.StreamBlock((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1)))))))))))),))), ('contacts', wagtail.core.blocks.StructBlock((('contacts', wagtail.core.blocks.ListBlock(involvement.blocks.contact_card_block.ContactCardBlock())),))), ('events', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('show_facebook', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to embed a Facebook page', required=False)), ('facebook_page_name', wagtail.core.blocks.CharBlock(help_text='Name of the page to show. (Must be public or accessible by the registered app_id)', required=False)), ('show_instagram', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Instagram the last event from the registered Instagram feed', required=False)), ('show_youtube', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Youtube', required=False)), ('youtube_channel_id', wagtail.core.blocks.CharBlock(required=False)), ('show_google_calendar', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show the next few events from a google calendar', required=False)), ('google_calendar_id', wagtail.core.blocks.CharBlock(required=False))))), ('contact_card', involvement.blocks.contact_card_block.ContactCardBlock())), blank=True, verbose_name='English Introduction'),
        ),
        migrations.AlterField(
            model_name='formpage',
            name='intro_sv',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1))))), ('heading', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('subtitle', wagtail.core.blocks.CharBlock(required=False))))), ('image_description', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock()))))), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.core.blocks.StructBlock((('description', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)), ('text_color', wagtail.core.blocks.ChoiceBlock(choices=[('text-light', 'Light'), ('text-dark', 'Dark')])), ('link', wagtail.core.blocks.URLBlock(required=False)), ('button', wagtail.core.blocks.CharBlock(required=False))))), ('logos', wagtail.core.blocks.StructBlock((('logos', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.core.blocks.URLBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)))))),))), ('counters', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('counters', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock(required=False)))))), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.core.blocks.StructBlock((('columns', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('width', wagtail.core.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.core.blocks.StreamBlock((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1)))))))))))),))), ('contacts', wagtail.core.blocks.StructBlock((('contacts', wagtail.core.blocks.ListBlock(involvement.blocks.contact_card_block.ContactCardBlock())),))), ('events', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('show_facebook', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to embed a Facebook page', required=False)), ('facebook_page_name', wagtail.core.blocks.CharBlock(help_text='Name of the page to show. (Must be public or accessible by the registered app_id)', required=False)), ('show_instagram', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Instagram the last event from the registered Instagram feed', required=False)), ('show_youtube', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Youtube', required=False)), ('youtube_channel_id', wagtail.core.blocks.CharBlock(required=False)), ('show_google_calendar', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show the next few events from a google calendar', required=False)), ('google_calendar_id', wagtail.core.blocks.CharBlock(required=False))))), ('contact_card', involvement.blocks.contact_card_block.ContactCardBlock())), blank=True, verbose_name='Swedish Introduction'),
        ),
        migrations.AlterField(
            model_name='formpage',
            name='thank_you_text_en',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1))))), ('heading', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('subtitle', wagtail.core.blocks.CharBlock(required=False))))), ('image_description', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock()))))), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.core.blocks.StructBlock((('description', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)), ('text_color', wagtail.core.blocks.ChoiceBlock(choices=[('text-light', 'Light'), ('text-dark', 'Dark')])), ('link', wagtail.core.blocks.URLBlock(required=False)), ('button', wagtail.core.blocks.CharBlock(required=False))))), ('logos', wagtail.core.blocks.StructBlock((('logos', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.core.blocks.URLBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)))))),))), ('counters', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('counters', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock(required=False)))))), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.core.blocks.StructBlock((('columns', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('width', wagtail.core.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.core.blocks.StreamBlock((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1)))))))))))),))), ('contacts', wagtail.core.blocks.StructBlock((('contacts', wagtail.core.blocks.ListBlock(involvement.blocks.contact_card_block.ContactCardBlock())),))), ('events', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('show_facebook', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to embed a Facebook page', required=False)), ('facebook_page_name', wagtail.core.blocks.CharBlock(help_text='Name of the page to show. (Must be public or accessible by the registered app_id)', required=False)), ('show_instagram', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Instagram the last event from the registered Instagram feed', required=False)), ('show_youtube', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Youtube', required=False)), ('youtube_channel_id', wagtail.core.blocks.CharBlock(required=False)), ('show_google_calendar', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show the next few events from a google calendar', required=False)), ('google_calendar_id', wagtail.core.blocks.CharBlock(required=False))))), ('contact_card', involvement.blocks.contact_card_block.ContactCardBlock())), blank=True, verbose_name='English Thank You Text'),
        ),
        migrations.AlterField(
            model_name='formpage',
            name='thank_you_text_sv',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1))))), ('heading', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('subtitle', wagtail.core.blocks.CharBlock(required=False))))), ('image_description', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock()))))), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.core.blocks.StructBlock((('description', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)), ('text_color', wagtail.core.blocks.ChoiceBlock(choices=[('text-light', 'Light'), ('text-dark', 'Dark')])), ('link', wagtail.core.blocks.URLBlock(required=False)), ('button', wagtail.core.blocks.CharBlock(required=False))))), ('logos', wagtail.core.blocks.StructBlock((('logos', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.core.blocks.URLBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)))))),))), ('counters', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('counters', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock(required=False)))))), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.core.blocks.StructBlock((('columns', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('width', wagtail.core.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.core.blocks.StreamBlock((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1)))))))))))),))), ('contacts', wagtail.core.blocks.StructBlock((('contacts', wagtail.core.blocks.ListBlock(involvement.blocks.contact_card_block.ContactCardBlock())),))), ('events', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('show_facebook', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to embed a Facebook page', required=False)), ('facebook_page_name', wagtail.core.blocks.CharBlock(help_text='Name of the page to show. (Must be public or accessible by the registered app_id)', required=False)), ('show_instagram', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Instagram the last event from the registered Instagram feed', required=False)), ('show_youtube', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Youtube', required=False)), ('youtube_channel_id', wagtail.core.blocks.CharBlock(required=False)), ('show_google_calendar', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show the next few events from a google calendar', required=False)), ('google_calendar_id', wagtail.core.blocks.CharBlock(required=False))))), ('contact_card', involvement.blocks.contact_card_block.ContactCardBlock())), blank=True, verbose_name='Swedish Thank You Text'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body_en',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1))))), ('heading', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('subtitle', wagtail.core.blocks.CharBlock(required=False))))), ('image_description', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock()))))), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.core.blocks.StructBlock((('description', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)), ('text_color', wagtail.core.blocks.ChoiceBlock(choices=[('text-light', 'Light'), ('text-dark', 'Dark')])), ('link', wagtail.core.blocks.URLBlock(required=False)), ('button', wagtail.core.blocks.CharBlock(required=False))))), ('logos', wagtail.core.blocks.StructBlock((('logos', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.core.blocks.URLBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)))))),))), ('counters', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('counters', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock(required=False)))))), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.core.blocks.StructBlock((('columns', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('width', wagtail.core.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.core.blocks.StreamBlock((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1)))))))))))),))), ('contacts', wagtail.core.blocks.StructBlock((('contacts', wagtail.core.blocks.ListBlock(involvement.blocks.contact_card_block.ContactCardBlock())),))), ('events', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('show_facebook', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to embed a Facebook page', required=False)), ('facebook_page_name', wagtail.core.blocks.CharBlock(help_text='Name of the page to show. (Must be public or accessible by the registered app_id)', required=False)), ('show_instagram', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Instagram the last event from the registered Instagram feed', required=False)), ('show_youtube', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Youtube', required=False)), ('youtube_channel_id', wagtail.core.blocks.CharBlock(required=False)), ('show_google_calendar', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show the next few events from a google calendar', required=False)), ('google_calendar_id', wagtail.core.blocks.CharBlock(required=False))))), ('news', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=False)), ('subtitle', wagtail.core.blocks.CharBlock(required=False)), ('index', wagtail.core.blocks.PageChooserBlock(target_model=['news.NewsIndexPage'])), ('items', wagtail.core.blocks.IntegerBlock()))))), blank=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body_sv',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1))))), ('heading', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('subtitle', wagtail.core.blocks.CharBlock(required=False))))), ('image_description', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock()))))), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.core.blocks.StructBlock((('description', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)), ('text_color', wagtail.core.blocks.ChoiceBlock(choices=[('text-light', 'Light'), ('text-dark', 'Dark')])), ('link', wagtail.core.blocks.URLBlock(required=False)), ('button', wagtail.core.blocks.CharBlock(required=False))))), ('logos', wagtail.core.blocks.StructBlock((('logos', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.core.blocks.URLBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)))))),))), ('counters', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('counters', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock(required=False)))))), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.core.blocks.StructBlock((('columns', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('width', wagtail.core.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.core.blocks.StreamBlock((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1)))))))))))),))), ('contacts', wagtail.core.blocks.StructBlock((('contacts', wagtail.core.blocks.ListBlock(involvement.blocks.contact_card_block.ContactCardBlock())),))), ('events', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('show_facebook', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to embed a Facebook page', required=False)), ('facebook_page_name', wagtail.core.blocks.CharBlock(help_text='Name of the page to show. (Must be public or accessible by the registered app_id)', required=False)), ('show_instagram', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Instagram the last event from the registered Instagram feed', required=False)), ('show_youtube', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Youtube', required=False)), ('youtube_channel_id', wagtail.core.blocks.CharBlock(required=False)), ('show_google_calendar', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show the next few events from a google calendar', required=False)), ('google_calendar_id', wagtail.core.blocks.CharBlock(required=False))))), ('news', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=False)), ('subtitle', wagtail.core.blocks.CharBlock(required=False)), ('index', wagtail.core.blocks.PageChooserBlock(target_model=['news.NewsIndexPage'])), ('items', wagtail.core.blocks.IntegerBlock()))))), blank=True),
        ),
        migrations.AlterField(
            model_name='webpage',
            name='body_en',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1))))), ('heading', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('subtitle', wagtail.core.blocks.CharBlock(required=False))))), ('image_description', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock()))))), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.core.blocks.StructBlock((('description', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)), ('text_color', wagtail.core.blocks.ChoiceBlock(choices=[('text-light', 'Light'), ('text-dark', 'Dark')])), ('link', wagtail.core.blocks.URLBlock(required=False)), ('button', wagtail.core.blocks.CharBlock(required=False))))), ('logos', wagtail.core.blocks.StructBlock((('logos', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.core.blocks.URLBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)))))),))), ('counters', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('counters', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock(required=False)))))), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.core.blocks.StructBlock((('columns', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('width', wagtail.core.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.core.blocks.StreamBlock((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1)))))))))))),))), ('contacts', wagtail.core.blocks.StructBlock((('contacts', wagtail.core.blocks.ListBlock(involvement.blocks.contact_card_block.ContactCardBlock())),))), ('events', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('show_facebook', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to embed a Facebook page', required=False)), ('facebook_page_name', wagtail.core.blocks.CharBlock(help_text='Name of the page to show. (Must be public or accessible by the registered app_id)', required=False)), ('show_instagram', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Instagram the last event from the registered Instagram feed', required=False)), ('show_youtube', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Youtube', required=False)), ('youtube_channel_id', wagtail.core.blocks.CharBlock(required=False)), ('show_google_calendar', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show the next few events from a google calendar', required=False)), ('google_calendar_id', wagtail.core.blocks.CharBlock(required=False))))), ('google_calendar', wagtail.core.blocks.StructBlock((('calendars', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('source', wagtail.core.blocks.CharBlock(help_text='Calendar ID as given by google calendar')), ('color', google.models.ColorBlock()))))), ('mode', wagtail.core.blocks.ChoiceBlock(choices=[('WEEK', 'Week'), ('', 'Month'), ('AGENDA', 'Agenda')], required=False)), ('height', wagtail.core.blocks.IntegerBlock()), ('background_color', google.models.ColorBlock()), ('week_start', wagtail.core.blocks.ChoiceBlock(choices=[('2', 'Monday'), ('1', 'Sunday'), ('7', 'Saturday')]))))), ('google_drive', wagtail.core.blocks.StructBlock((('folder_id', wagtail.core.blocks.CharBlock()), ('view', wagtail.core.blocks.ChoiceBlock(choices=[('list', 'List'), ('grid', 'Grid')])), ('height', wagtail.core.blocks.IntegerBlock())))), ('google_form', wagtail.core.blocks.StructBlock((('form_id', wagtail.core.blocks.CharBlock()), ('height', wagtail.core.blocks.IntegerBlock())))), ('news', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=False)), ('subtitle', wagtail.core.blocks.CharBlock(required=False)), ('index', wagtail.core.blocks.PageChooserBlock(target_model=['news.NewsIndexPage'])), ('items', wagtail.core.blocks.IntegerBlock()))))), blank=True),
        ),
        migrations.AlterField(
            model_name='webpage',
            name='body_sv',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1))))), ('heading', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('subtitle', wagtail.core.blocks.CharBlock(required=False))))), ('image_description', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('icons', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('title', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock()))))), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('image_icons', wagtail.core.blocks.StructBlock((('description', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')])), ('hide_on_med', wagtail.core.blocks.BooleanBlock(required=False))))), ('overlay', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)), ('text_color', wagtail.core.blocks.ChoiceBlock(choices=[('text-light', 'Light'), ('text-dark', 'Dark')])), ('link', wagtail.core.blocks.URLBlock(required=False)), ('button', wagtail.core.blocks.CharBlock(required=False))))), ('logos', wagtail.core.blocks.StructBlock((('logos', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.core.blocks.URLBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False)))))),))), ('counters', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock()), ('counters', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('icon', wagtail.core.blocks.CharBlock(help_text='Material icon font icon text, as found on: https://material.io/icons')), ('value', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.CharBlock(required=False)))))), ('style', wagtail.core.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')]))))), ('columns', wagtail.core.blocks.StructBlock((('columns', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('width', wagtail.core.blocks.IntegerBlock(help_text='Width out of 12', max_value=12, min_value=1)), ('content', wagtail.core.blocks.StreamBlock((('paragraph', wagtail.core.blocks.RichTextBlock(group='Basic', template='blocks/paragraph.html')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('height', wagtail.core.blocks.IntegerBlock(default=400, min_value=1)))))))))))),))), ('contacts', wagtail.core.blocks.StructBlock((('contacts', wagtail.core.blocks.ListBlock(involvement.blocks.contact_card_block.ContactCardBlock())),))), ('events', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=True)), ('show_facebook', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to embed a Facebook page', required=False)), ('facebook_page_name', wagtail.core.blocks.CharBlock(help_text='Name of the page to show. (Must be public or accessible by the registered app_id)', required=False)), ('show_instagram', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Instagram the last event from the registered Instagram feed', required=False)), ('show_youtube', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show Youtube', required=False)), ('youtube_channel_id', wagtail.core.blocks.CharBlock(required=False)), ('show_google_calendar', wagtail.core.blocks.BooleanBlock(help_text='Whether or not to show the next few events from a google calendar', required=False)), ('google_calendar_id', wagtail.core.blocks.CharBlock(required=False))))), ('google_calendar', wagtail.core.blocks.StructBlock((('calendars', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('source', wagtail.core.blocks.CharBlock(help_text='Calendar ID as given by google calendar')), ('color', google.models.ColorBlock()))))), ('mode', wagtail.core.blocks.ChoiceBlock(choices=[('WEEK', 'Week'), ('', 'Month'), ('AGENDA', 'Agenda')], required=False)), ('height', wagtail.core.blocks.IntegerBlock()), ('background_color', google.models.ColorBlock()), ('week_start', wagtail.core.blocks.ChoiceBlock(choices=[('2', 'Monday'), ('1', 'Sunday'), ('7', 'Saturday')]))))), ('google_drive', wagtail.core.blocks.StructBlock((('folder_id', wagtail.core.blocks.CharBlock()), ('view', wagtail.core.blocks.ChoiceBlock(choices=[('list', 'List'), ('grid', 'Grid')])), ('height', wagtail.core.blocks.IntegerBlock())))), ('google_form', wagtail.core.blocks.StructBlock((('form_id', wagtail.core.blocks.CharBlock()), ('height', wagtail.core.blocks.IntegerBlock())))), ('news', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(required=False)), ('subtitle', wagtail.core.blocks.CharBlock(required=False)), ('index', wagtail.core.blocks.PageChooserBlock(target_model=['news.NewsIndexPage'])), ('items', wagtail.core.blocks.IntegerBlock()))))), blank=True),
        ),
    ]
