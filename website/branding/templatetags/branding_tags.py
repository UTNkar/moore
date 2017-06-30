from django import template

from branding.models import Logo, SocialMediaSettings, FooterSettings

register = template.Library()


@register.inclusion_tag('branding/tags/footer.html', takes_context=True)
def custom_footer(context):
    request = context['request']
    return {
        'settings': FooterSettings.for_site(request.site)
    }


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


@register.inclusion_tag('branding/tags/social_media.html', takes_context=True)
def social_media(context, dark=False):
    request = context['request']
    return {
        'settings': SocialMediaSettings.for_site(request.site),
        'dark': dark,
    }
