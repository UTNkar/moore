from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def status_badge(member):
    if member.status == 'member':
        cl = 'green'
    elif member.status == 'alumnus':
        cl = 'blue'
    elif member.status == 'nonmember':
        cl = 'red'
    else:
        cl = ''

    return format_html(
        '<div class="chip {}">{}</div>',
        cl, member.get_status_display()
    )
