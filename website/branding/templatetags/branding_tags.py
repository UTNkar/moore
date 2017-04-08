from django import template

from branding.models import Logo

register = template.Library()


@register.inclusion_tag('branding/tags/structure_header.html',
                        takes_context=True)
def structure_header(context, logo_color=''):
    logos = Logo.objects.exclude(belongs_to=context['request'].site).all()
    committees = logos.filter(category='committee')
    sections = logos.filter(category='section')
    return {
        'committees': committees,
        'sections': sections,
        'color': logo_color,
    }
