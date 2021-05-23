from django import forms
from wagtail.utils.widgets import WidgetWithScript


class CodeMirrorWidget(WidgetWithScript, forms.Textarea):

    def render_js_init(self, id, name, value):
        js = """
        document.addEventListener('DOMContentLoaded', function(){{
            CodeMirror.fromTextArea(
                document.getElementById("{id}"),
                {{
                lineWrapping: true,
                indentUnit: 4,
                mode: "htmlmixed",
                autoRefresh: true
                }}
            )
        }});
        """
        return js.format(id=id, value=value)

    @property
    def media(self):
        return forms.Media(
            css={'all': ('libraries/codemirror/codemirror.css',)},
            js=(
                'libraries/codemirror/codemirror.js',
                'libraries/codemirror/autorefresh.js',
                'libraries/codemirror/xml.js',
                'libraries/codemirror/css.js',
                'libraries/codemirror/javascript.js',
                'libraries/codemirror/htmlmixed.js',
            )
        )
