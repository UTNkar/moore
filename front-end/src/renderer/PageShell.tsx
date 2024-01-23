import './css/style.css';
import '../devlink/global.css';

import { ComponentType, StrictMode } from 'react';

import { DevLinkProvider } from '#root/devlink/devlinkContext';
import { LayoutProps, PageContextProvider, PropsWithChildrenAndPageContext } from '#root/utils/page';

import DefaultLayout from './layout/DefaultLayout';

export default function PageShell({ children, pageContext }: PropsWithChildrenAndPageContext) {
  const Layout: ComponentType<LayoutProps> = (pageContext.config as any).Layout || DefaultLayout;

  return (
    <StrictMode>
      <DevLinkProvider>
        <PageContextProvider pageContext={pageContext}>
          <Layout pageContext={pageContext}>{children}</Layout>
        </PageContextProvider>
      </DevLinkProvider>
    </StrictMode>
  );
}
