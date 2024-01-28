import './css/style.css';
import '../devlink/global.css';

import { ComponentType, StrictMode, useMemo } from 'react';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import { DevLinkProvider } from '#root/devlink/devlinkContext';
import { LayoutProps, PageContextProvider, PropsWithChildrenAndPageContext } from '#root/utils/page';

import DefaultLayout from './layout/DefaultLayout';

export default function PageShell({
  children,
  pageContext,
  reactQueryClient = useMemo(() => new QueryClient(), []),
}: PropsWithChildrenAndPageContext & {
  reactQueryClient?: QueryClient;
}) {
  const Layout: ComponentType<LayoutProps> = (pageContext.config as any).Layout || DefaultLayout;

  return (
    <StrictMode>
      <QueryClientProvider client={reactQueryClient}>
        <DevLinkProvider>
          <PageContextProvider pageContext={pageContext}>
            <Layout pageContext={pageContext}>{children}</Layout>
          </PageContextProvider>
        </DevLinkProvider>
      </QueryClientProvider>
    </StrictMode>
  );
}
