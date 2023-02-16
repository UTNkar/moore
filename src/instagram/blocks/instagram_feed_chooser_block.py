from wagtail.core import blocks
from instagram.models import InstagramFeed
from django import forms
from django.utils.translation import gettext_lazy as _


class InstagramFeedChooserBlock(blocks.ChooserBlock):
    target_model = InstagramFeed
    widget = forms.Select

    class Meta:
        label = 'Instagram'
        icon = "fa-instagram"
        group = _('Basic')
        template = 'instagram_feed.html'
