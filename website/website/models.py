from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting

from django.utils.translation import ugettext_lazy as _


@register_setting(icon='openquote')
class SocialMediaSettings(BaseSetting):
    class Meta:
        verbose_name = _('Social media accounts')
    facebook = models.URLField(
        help_text=_('Your Facebook page URL'),
        blank=True,
    )
    instagram = models.CharField(
        max_length=255,
        help_text=_('Your Instagram username, without the @'),
        blank=True,
    )
    twitter = models.CharField(
        max_length=255,
        help_text=_('Your Twitter username, without the @'),
        blank=True,
    )
