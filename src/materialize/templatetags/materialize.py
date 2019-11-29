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


def render_field(templ, field, prefix=None):
    if field == '':
        return None
    t = loader.get_template(templ)
    c = {
        'field': field,
        'prefix': prefix,
    }
    return t.render(c)


@register.simple_tag
def materialize_field(field, prefix=None):
    if field == '':
        return
    widget = get_widget_name(field)
    t = ''
    # TODO: DateTimeInput
    if widget in ['EmailInput', 'DateInput', 'DateTimeInput', 'NumberInput',
                  'PasswordInput', 'Select', 'Textarea', 'TextInput',
                  'URLInput']:
        append_classes(field, widget)
        t = 'materialize/form/input.html'
    elif widget == 'CheckboxInput':
        t = 'materialize/form/p_input.html'
    elif widget == 'SelectMultiple':
        w = field.field.widget
        w.template_name = 'materialize/form/multiple_input.html'
        t = 'materialize/form/input.html'
    else:
        raise NotImplementedError('Widget %s not yet supported' % widget)

    return render_field(t, field, prefix)


@register.inclusion_tag('materialize/pagination.html')
def materialize_pagination(page, url):
    return {
        'page': page,
        'paginator': page.paginator,
        'url': url,
    }
