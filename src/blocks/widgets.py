from django import forms
from js_asset import JS
from wagtail.utils.widgets import WidgetWithScript


class CodeMirrorWidget(WidgetWithScript, forms.Textarea):

    template_name = 'blocks/html_editor.html'

    @property
    def media(self):
        # The JS module allows us to add custom attributes to script tags.
        # In this case we need to add type=module since codemirror.js is
        # made as an ES module.
        media = forms.Media(js=[
            JS("codemirror.js", {"type": "module"})
        ])

        return media
