import { LayoutProps } from "../types";
import { PageProps } from ".";

declare global {
  namespace Vike {
    interface DocumentProps {
      description?: string;
      locale?: Locale;
      title?: string;
    }

    interface PageContext {
      Page: ComponentType<PageProps>;
      documentProps: DocumentProps;
      locale: Locale;
      pageProps: PageProps;
      urlOriginal: string;
      description: string;
      title: string;
    }

    interface Config {
      Page?: ComponentType<PageProps>;
      description?: string;
      locale?: Locale;
      title?: string;
      Layout?: ComponentType<LayoutProps>;
    }
  }

  namespace VikePackages {
    interface ConfigVikeReact {
      Layout: ComponentType<LayoutProps>;
      description: string;
      title: string;
      locale: Locale;
    }
  }
}
