// https://vike.dev/onRenderClient
import { Root, createRoot, hydrateRoot } from 'react-dom/client';
import type { PageContextClient } from 'vike/types';

import { PageProps } from '#root/utils/page';

import PageShell from './PageShell';

let reactRoot: Root;

export default async function onRenderClient(pageContext: PageContextClient): Promise<void> {
  const { Page, pageProps = {} as PageProps } = pageContext;

  console.log(pageProps);

  pageProps.pageContext = pageContext;

  const page = (
    <PageShell pageContext={pageContext}>
      <Page {...pageProps} />
    </PageShell>
  );

  const rootElement = document.getElementById('root');

  if (rootElement.innerHTML !== '' && pageContext.isHydration) {
    reactRoot = hydrateRoot(rootElement, page);
  } else {
    if (!reactRoot) {
      reactRoot = createRoot(rootElement);
    }

    reactRoot.render(page);
  }
}
