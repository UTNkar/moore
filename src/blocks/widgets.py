from django import forms
from wagtail.utils.widgets import WidgetWithScript
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from string import Template
from django.forms.widgets import Media


def custom_render_js(self):
    return [
        format_html(
            '<script type="module" src="{}"></script>',
            self.absolute_path(path)
        )
        if path == "my-lib.js"
        else format_html(
            '<script src="{}"></script>', self.absolute_path(path)
        )
        for path in self._js
    ]


Media.render_js = custom_render_js


class CodeMirrorWidget(WidgetWithScript, forms.Textarea):

    template_name = 'blocks/html_editor.html'

    def render_js_init(self, id, name, value):
        js = Template("""
        //document.addEventListener('DOMContentLoaded', function(){{
            import {EditorState, EditorView, keymap, defaultKeymap} from '/static/my-lib.js';
            let startState = EditorState.create({
                doc: "Hello World",
                extensions: [keymap.of(defaultKeymap)],
            });

            let view1 = new EditorView({
                state: startState,
                parent: document.querySelector("#$id"),
            });
            console.log(document.querySelector("#$id"))
        //}});
        """)
        return js.substitute(id=id)

    def render(self, name, value, attrs=None, renderer=None):
        # no point trying to come up with sensible semantics for when 'id' is missing from attrs,
        # so let's make sure it fails early in the process
        try:
            id_ = attrs['id']
        except (KeyError, TypeError):
            raise TypeError(
                "WidgetWithScript cannot be rendered without an 'id' attribute")

        value_data = self.get_value_data(value)
        widget_html = self.render_html(name, value_data, attrs)

        js = self.render_js_init(id_, name, value_data)
        out = '{0}<script type="module">{1}</script>'.format(widget_html, js)
        return mark_safe(out)

    @property
    def media(self):
        media = forms.Media(
            # css={'all': ('libraries/codemirror/codemirror.css',)},
            # js=(
            #     'libraries/codemirror/codemirror.js',
            #     'libraries/codemirror/autorefresh.js',
            #     'libraries/codemirror/xml.js',
            #     'libraries/codemirror/css.js',
            #     'libraries/codemirror/javascript.js',
            #     'libraries/codemirror/htmlmixed.js',
            # )
            js=("my-lib.js", )
        )

        return media
