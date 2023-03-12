import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig({
    build: {
        // put output in folder named static so django can find the generated files
        outDir: "static",
        lib: {
            // Could also be a dictionary or array of multiple entry points
            entry: resolve(__dirname, "index.js"),
            name: "MyLib",
            // the proper extensions will be added
            fileName: "my-lib",
        },
    },
});
