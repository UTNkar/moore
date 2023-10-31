// https://vike.dev/onPrerenderStart

import { defaultLocale, locales } from '#root/utils/intl';

// We only need this for pre-rendered apps https://vike.dev/pre-rendering
export default function onPrerenderStart(prerenderContext: any): any {
  const pageContexts = [];

  prerenderContext.pageContexts.forEach((pageContext) => {
    // Duplicate pageContext for each locale
    locales.forEach((locale) => {
      // Localize URL
      let { urlOriginal } = pageContext;

      if (locale !== defaultLocale) {
        urlOriginal = `/${locale}${pageContext.urlOriginal}`;
      }

      pageContexts.push({
        ...pageContext,

        config: {
          ...(pageContext.config || {}),
          lang: locale,
        },
        // Set pageContext.locale
        locale,
        urlOriginal,
      });
    });
  });

  return {
    prerenderContext: {
      pageContexts,
    },
  };
}
