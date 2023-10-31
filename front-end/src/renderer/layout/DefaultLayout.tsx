import { PropsWithChildren } from '#root/utils/types';

import Footer from './Footer';
import Header from './Header';

export default function DefaultLayout({ children }: PropsWithChildren) {
  return (
    <>
      <Header />

      <main className="flex flex-1 flex-col items-start justify-items-start">{children}</main>

      <Footer />
    </>
  );
}
