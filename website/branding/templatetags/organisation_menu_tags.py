from django import template

from branding.models import Logo

register = template.Library()


@register.inclusion_tag('branding/tags/organisation_menu.html',
                        takes_context=True)
def organisation_menu(context, color=''):
    logos = Logo.objects.exclude(belongs_to=context['request'].site).all()
    committees = logos.filter(category='committee')
    sections = logos.filter(category='section')
    return {
        'committees': committees,
        'sections': sections,
        'color': color,
    }
