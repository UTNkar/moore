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


@register.filter
def status_icon(value):
    if value == 'draft':
        return 'fa-pencil'
    elif value == 'submitted':
        return 'fa-envelope-open'
    elif value == 'approved':
        return 'fa-thumbs-up'
    elif value == 'disapproved':
        return 'fa-thumbs-down'
    elif value == 'appointed':
        return 'fa-check'
    elif value == 'turned_down':
        return 'fa-close'
    else:
        return 'fa-exclamation-triangle'
