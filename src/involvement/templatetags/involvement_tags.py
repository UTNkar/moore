from datetime import date
from django import template
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.inclusion_tag('involvement/tags/contact_card.html')
def contact_card(contact_card, large_width=7, medium_width=12, small_width=12):

    data = {
        'large_width': large_width,
        'medium_width': medium_width,
        'small_width': small_width,
    }

    position = contact_card.position
    role = position.role
    application = contact_card.application

    data['picture'] = contact_card.picture
    data['title'] = role.name
    data['description'] = role.description

    if application is not None:
        applicant = application.applicant
        data['card_name'] = applicant.get_full_name
        data['phone_number'] = role.phone_number \
            if role.phone_number else applicant.phone_number
        data['email'] = role.contact_email \
            if role.contact_email else applicant.email
    else:
        data['card_name'] = _('Vacant Position')
        data['phone_number'] = role.phone_number
        data['email'] = role.election_email

    return data


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
