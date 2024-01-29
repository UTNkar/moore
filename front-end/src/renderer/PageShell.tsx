import 'react-toastify/dist/ReactToastify.css';
import '../devlink/global.css';
import './css/style.css';

import { ComponentType, StrictMode, useMemo } from 'react';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ToastContainer } from 'react-toastify';

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

            <ToastContainer />
          </PageContextProvider>
        </DevLinkProvider>
      </QueryClientProvider>
    </StrictMode>
  );
}
