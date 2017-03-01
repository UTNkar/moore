from datetime import date

from django import template

register = template.Library()


@register.filter
def date_color(value):
    delta = value - date.today()

    if delta.days < 1:
        return "#E53935"
    elif delta.days <= 3:
        return "#FBC02D"
    else:
        return "inherit"
