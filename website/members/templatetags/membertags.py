from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def status_badge(member):
    if member.status == 'member':
        cl = 'badge-success'
    elif member.status == 'alumnus':
        cl = 'badge-primary'
    elif member.status == 'nonmember':
        cl = 'badge-danger'
    else:
        cl = 'badge-default'

    return format_html(
        '<span class="badge {}">{}</span>',
        cl, member.get_status_display()
    )
