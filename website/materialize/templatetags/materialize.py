from django import template
from django.template import loader

register = template.Library()


def get_widget_name(field):
    return field.field.widget.__class__.__name__


def append_classes(field):
    classes = field.field.widget.attrs.get('class', '')
    classes += ' validate'
    if field.errors:
        classes += ' invalid'
    field.field.widget.attrs['class'] = classes


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
    widget = get_widget_name(field)
    if widget in ['TextInput', 'EmailInput', 'PasswordInput', 'Select',
                  'Textarea']:
        append_classes(field)
        return render_field('materialize/form/input.html', field, prefix)
    else:
        return field.as_widget()
