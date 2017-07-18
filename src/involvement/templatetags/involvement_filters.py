from datetime import date

from django import template

register = template.Library()


@register.filter
def date_color(value):
    delta = value - date.today()

    if delta.days < 0:
        return 'inherit'
    elif delta.days < 1:
        return "#E53935"
    elif delta.days <= 3:
        return "#FBC02D"
    else:
        return "inherit"


@register.filter
def status_icon(value):
    if value == 'draft':
        return 'edit'
    elif value == 'submitted':
        return 'send'
    elif value == 'approved':
        return 'thumb_up'
    elif value == 'disapproved':
        return 'thumb_down'
    elif value == 'appointed':
        return 'person_pin'
    elif value == 'turned_down':
        return 'do_not_disturb'
    else:
        return 'error'
