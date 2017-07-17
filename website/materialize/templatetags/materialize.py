from django import template
from django.template import loader

register = template.Library()


def get_widget_name(field):
    return field.field.widget.__class__.__name__


def append_classes(field, widget=''):
    field.field.label_suffix = ''
    classes = field.field.widget.attrs.get('class', '')
    classes += ' validate'
    if field.errors:
        classes += ' invalid'
    if widget == 'Textarea':
        classes += ' materialize-textarea'
    if widget == 'DateInput':
        classes += ' datepicker'
    field.field.widget.attrs['class'] = classes


def render_field(template, field, prefix=None):
    t = loader.get_template(template)
    c = {
        'field': field,
        'prefix': prefix,
    }
    return t.render(c)


@register.simple_tag
def materialize_field(field, prefix=None):
    widget = get_widget_name(field)
    if widget in ['EmailInput', 'DateInput', 'DateTimeInput', 'NumberInput',
                  'PasswordInput', 'Select', 'Textarea', 'TextInput',
                  'URLInput']:
        append_classes(field, widget)
        return render_field('materialize/form/input.html', field, prefix)
    elif widget == 'CheckboxInput':
        return render_field('materialize/form/p_input.html', field)
    # TODO: CheckboxSelectMultiple, DateTimeInput
    else:
        raise NotImplementedError('Widget %s not yet supported' % widget)


@register.inclusion_tag('materialize/pagination.html')
def materialize_pagination(page, url):
    return {
        'page': page,
        'paginator': page.paginator,
        'url': url,
    }
