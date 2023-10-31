import type { Config, ConfigEnv } from 'vike/types';

// https://vike.dev/config
export default {
  clientRouting: true,
  hydrationCanBeAborted: true,
  meta: {
    description: { env: 'server-and-client' },
    Layout: { env: 'server-and-client' },
    onBeforeRenderIsomorph: {
      effect: ({ configDefinedAt, configValue }) => {
        if (typeof configValue !== 'boolean') {
          throw new Error(`${configDefinedAt} should be a boolean`);
        }

        if (configValue) {
          return {
            meta: {
              onBeforeRender: {
                // We override Vike's default behavior of always loading/executing onBeforeRender() on the server-side.
                // If we set onBeforeRenderIsomorph to true, then onBeforeRender() is loaded/executed in the browser as well, allowing us to fetch data direcly from the browser upon client-side navigation (without involving our Node.js/Edge server at all).
                env: 'server-and-client',
              },
            },
          };
        }
      },
      env: 'config-only',
    },
    renderMode: {
      effect: ({ configDefinedAt, configValue }) => {
        let env: ConfigEnv | undefined;

        if (configValue === 'HTML') env = 'server-only';
        if (configValue === 'SPA') env = 'client-only';
        if (configValue === 'SSR') env = 'server-and-client';

        if (!env) {
          throw new Error(`${configDefinedAt} should be 'SSR', 'SPA', or 'HTML'`);
        }

        return {
          meta: {
            Page: { env },
          },
        };
      },
      env: 'config-only',
    },
    title: { env: 'server-and-client' },
  },
  // https://vike.dev/passToClient
  passToClient: ['pageProps', 'title', 'description', 'urlOriginal', 'locale'],
} satisfies Config;
