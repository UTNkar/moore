from django import template
from instagram.utils import InstagramUtils
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.simple_tag
def get_authorization_url():
    return InstagramUtils.get_authorization_url()


@register.simple_tag
def get_latest_media(account_name):
    media = InstagramUtils.get_latest_media(account_name)
    if media is None:
        return {
            "error_message": _(
                "Either an error occured or there is no media to show"
            )
        }
    else:
        return media
