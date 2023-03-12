import { EditorView, keymap } from "@codemirror/view";
import { defaultKeymap } from "@codemirror/commands";
import { EditorState } from "@codemirror/state";

let startState = EditorState.create({
    doc: "Hello World",
    extensions: [keymap.of(defaultKeymap)],
});

let view1 = new EditorView({
    state: startState,
    parent: document.querySelector("#editor1"),
});

console.log("its working");

export { EditorView, EditorState, keymap, defaultKeymap };
