import { PageContext } from 'vike/types';

export type PropsWithChildren<T extends object = {}> = T & {
  children?: React.ReactNode;
};

export type PropsWithChildrenAndPageContext<T extends object = {}> = T & {
  children?: React.ReactNode;
  pageContext: PageContext;
};

export type PropsWithPageContext<T extends object = {}> = T & {
  pageContext: PageContext;
};

export type PropsWithRequiredChildren<T extends object = {}> = T & {
  children: React.ReactNode;
};
