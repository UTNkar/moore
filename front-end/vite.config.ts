import vike from 'vike/plugin';

import { resolve } from 'path';

import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';
import { imagetools } from 'vite-imagetools';

// https://vitejs.dev/config/
export default defineConfig({
  // We manually add a list of dependencies to be pre-bundled, in order to avoid a page reload at dev start which breaks Vike's CI
  optimizeDeps: { include: ['react/jsx-runtime'] },
  plugins: [imagetools(), react(), vike({ prerender: true })],
  resolve: {
    alias: { '#root': resolve(__dirname, 'src') },
  },
});
