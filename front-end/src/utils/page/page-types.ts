import type { PageContext } from 'vike/types';

import type { ConfigBuiltIn } from 'node_modules/vike/dist/esm/shared/page-configs/Config';

export interface LayoutProps<Data = unknown> {
  children?: React.ReactNode;
  pageContext: PageContext<Data>;
}

export type PageConfig = ConfigBuiltIn & Vike.Config & VikePackages.ConfigVikeReact;

export interface PageProps {
  pageContext: PageContext;
}

export type PropsWithChildrenAndPageContext<T extends object = {}> = T & {
  children?: React.ReactNode;
  pageContext: PageContext;
};

export type PropsWithPageContext<T extends object = {}> = T & {
  pageContext: PageContext;
};
