namespace Vike {
    interface DocumentProps {
      description?: string;
      locale?: Locale;
      title?: string;
    }

    interface PageContext {
      Page: ComponentType<any>;
      documentProps: DocumentProps;
      locale: Locale;
      pageProps: any;
      urlOriginal: string;
      description: string;
      title: string;
    }

    interface Config {
      description?: string;
      locale?: Locale;
      title?: string;
    }
  }

  namespace VikePackages {
    interface ConfigVikeReact {
      Layout: ComponentType<PropsWithChildren>;
      description: string;
      title: string;
      locale: Locale;
    }
  }
