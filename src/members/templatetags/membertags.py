from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def status_badge(member, status):
    if status == 'member':
        cl = 'green'
    elif status == 'nonmember':
        cl = 'red'
    else:
        cl = ''

    return format_html(
        '<div class="chip {}">{}</div>',
        cl, member.get_status_text(status)
    )
