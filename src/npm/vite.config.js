import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig({
    build: {
        lib: {
            // The index does not serve any purpose but the entry and name
            // is required for vite to create the javascript files as separate files
            entry: resolve(__dirname, "index.js"),
            name: "Moore NPM dependencies",
        },
        rollupOptions: {
            input: {
                // If new javascript files are created
                // Add them here
                codemirror: resolve(__dirname, "codemirror.js"),
                materialize: resolve(__dirname, "materialize.js"),
            },
            output: [
                {
                    entryFileNames: ({ name }) => `${name}.js`,
                    dir: resolve(__dirname, "static"),
                },
            ],
        },
    },
});
