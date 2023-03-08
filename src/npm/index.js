let startState = EditorState.create({
    doc: "Hello World",
    extensions: [keymap.of(defaultKeymap)],
});

let view = new EditorView({
    state: startState,
    parent: document.body,
});
