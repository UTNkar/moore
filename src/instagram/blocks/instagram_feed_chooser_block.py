from wagtail.core import blocks
from instagram.models import InstagramFeed
from django import forms
from django.utils.translation import ugettext_lazy as _


class InstagramFeedChooserBlock(blocks.ChooserBlock):
    target_model = InstagramFeed
    widget = forms.Select

    class Meta:
        label = _('Instagram')
        icon = "fa-instagram"
        group = _('Basic')
        template = 'instagram_feed.html'
