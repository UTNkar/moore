import { basicSetup, EditorView } from "codemirror";
import { EditorState } from "@codemirror/state";
import { html } from "@codemirror/lang-html";

const theme = EditorView.baseTheme({
    "&.cm-editor": {
        fontSize: "1rem",
    },
});

export { EditorView, EditorState, html, basicSetup, theme };
