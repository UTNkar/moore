import './css/style.css';

import { StrictMode } from 'react';

import { PageContextProvider } from '#root/utils/page';
import { PropsWithChildrenAndPageContext } from '#root/utils/types';

import DefaultLayout from './layout/DefaultLayout';

export default function PageShell({ children, pageContext }: PropsWithChildrenAndPageContext) {
  const Layout = pageContext.config.Layout || DefaultLayout;

  return (
    <StrictMode>
      <PageContextProvider pageContext={pageContext}>
        <Layout>{children}</Layout>
      </PageContextProvider>
    </StrictMode>
  );
}
