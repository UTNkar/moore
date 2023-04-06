from django import forms
from js_asset import JS
from wagtail.utils.widgets import WidgetWithScript
from django.utils.html import format_html
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
            import {
                EditorState, EditorView, keymap, defaultKeymap
            } from '/static/codemirror.js';
            let startState = EditorState.create({
                doc: "Hello World",
                extensions: [keymap.of(defaultKeymap)],
            });

            let view1 = new EditorView({
                state: startState,
                parent: document.querySelector("#$id"),
            });
            console.log(document.querySelector("#$id"));
        """)
        return js.substitute(id=id)

    def render(self, name, value, attrs=None, renderer=None):
        # Javascript in wagtail don't run as type=module and as of wagtail 2.16
        # there is no support for this. There for we have to override it.
        # render returns the tempalte and the extra script tag, all we have to
        # do is to add type=module ourselves
        out = super().render(
            name, value, attrs=attrs, renderer=renderer
        )
        out = out.replace("<script>", "<script type='module'>")
        return out

    @property
    def media(self):
        # The JS module allows us to add custom attributes to script tags.
        # In this case we need to add type=module since codemirror.js is
        # made as an ES module.
        media = forms.Media(js=[
            JS("codemirror.js", {"type": "module"})
        ])

        return media
