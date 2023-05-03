from django.db import models
from django import forms
from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.admin.panels import FieldPanel


class InstagramFeed(models.Model):
    class Meta:
        verbose_name = 'Instagram Feed'
        verbose_name_plural = 'Instagram Feeds'

    def __str__(self):
        return self.account_name

    account_name = models.CharField(max_length=80, primary_key=True)
    access_token = models.CharField(max_length=500)
    expires = models.DateTimeField()

    panels = [
        FieldPanel(
            'account_name',
            widget=forms.TextInput(attrs={"disabled": True})
        ),
        FieldPanel(
            'access_token',
            widget=forms.TextInput(attrs={"disabled": True})
        ),
        FieldPanel(
            'expires',
            widget=forms.DateTimeInput(attrs={"disabled": True})
        ),
    ]


class InstagramFeedAdmin(ModelAdmin):
    model = InstagramFeed
    menu_icon = 'fa-instagram'
    menu_order = 110
    create_template_name = "create.html"
    form_view_extra_css = ["create.css"]
