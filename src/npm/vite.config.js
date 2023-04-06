import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig({
    build: {
        lib: {
            entry: resolve(__dirname, "index.js"),
            name: "Moore NPM dependencies",
        },
        rollupOptions: {
            input: {
                codemirror: resolve(__dirname, "codemirror.js"),
                materialize: resolve(__dirname, "materialize.js"),
            },
            output: [
                {
                    entryFileNames: ({ name }) => `${name}.js`,
                    // format: "esm",
                    dir: resolve(__dirname, "static"),
                },
            ],
        },
    },
});
