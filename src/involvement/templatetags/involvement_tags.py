from datetime import date

from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.inclusion_tag('involvement/tags/contact_card.html')
def contact_card(card, width=7):
    role = {}
    if card.role:
        role['role_text'] = card.role.__str__()
        member = card.role.in_role().first()
        if member:
            role['name'] = member.get_full_name()
            role['email'] = member.get_primary_email()
        else:
            role['name'] = _('Vacant Position')
    return {
        'card': card,
        'role': role,
        'width': width,
    }


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
