from django import template
from instagram.utils import InstagramUtils

register = template.Library()


@register.simple_tag
def get_authorization_url():
    return InstagramUtils.get_authorization_url()


@register.simple_tag
def get_latest_media(account_name):
    return InstagramUtils.get_latest_media(account_name)
