from django import template
from django.template import loader

register = template.Library()


def get_widget(field):
    return field.field.widget.__class__.__name__


def render_field(template, field, prefix=None):
    t = loader.get_template(template)
    c = {
        'field': field,
        'prefix': prefix,
    }
    html = t.render(c)
    return html


@register.simple_tag
def materialize_field(field, prefix=None):
    widget = get_widget(field)
    if widget == 'EmailInput':
        return render_field('materialize/form/email_input.html', field, prefix)
    elif widget == 'PasswordInput':
        return render_field(
            'materialize/form/password_input.html', field, prefix
        )
    elif widget == 'Select':
        return render_field('materialize/form/select.html', field, prefix)
    elif widget == 'TextInput':
        return render_field('materialize/form/text_input.html', field, prefix)
    else:
        return field.as_widget()
