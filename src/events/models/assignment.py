from django.db import models
from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, \
    InlinePanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from events.models import Ticket, EventApplication

@register_snippet
class Assignment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True)
    application = models.ForeignKey(EventApplication, on_delete=models.SET_NULL, null=True)
