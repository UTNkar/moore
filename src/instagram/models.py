from django.db import models
from wagtail.contrib.modeladmin.options import ModelAdmin


class InstagramFeed(models.Model):
    class Meta:
        verbose_name = 'Instagram Feed'
        verbose_name_plural = 'Instagram Feeds'

    def __str__(self):
        return self.account_name

    account_name = models.CharField(max_length=80)
    access_token = models.CharField(max_length=500)
    expires = models.DateTimeField()

    panels = []


class InstagramFeedAdmin(ModelAdmin):
    model = InstagramFeed
    menu_icon = 'fa-instagram'
    menu_order = 110
    create_template_name = "create.html"
