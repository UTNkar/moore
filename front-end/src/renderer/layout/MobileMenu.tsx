import { useRef } from 'react';

import { create } from 'zustand';

import Link from '#root/components/Link';
import useEscapeRefsHandler from '#root/utils/hooks/useEscapeRefsHandler';
import { LocalizedText } from '#root/utils/intl';

import navigationLinks from './navigationLinks';

export default function MobileMenu() {
  const trigger = useRef<HTMLButtonElement>(null);
  const mobileNav = useRef<HTMLDivElement>(null);

  const store = useMobileMenuStore();

  // close the mobile menu on click outside
  useEscapeRefsHandler([trigger, mobileNav], store.hide, [store]);

  return (
    <div className="md:hidden">
      {/* Hamburger button */}
      <button
        ref={trigger}
        className={`hamburger ${store.visible && 'active'}`}
        aria-controls="mobile-nav"
        aria-expanded={store.visible}
        onClick={store.toggle}
      >
        <span className="sr-only">Menu</span>
        <svg
          className="h-6 w-6 fill-current text-gray-300 transition duration-150 ease-in-out hover:text-gray-200"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <rect y="4" width="24" height="2" rx="1" />
          <rect y="11" width="24" height="2" rx="1" />
          <rect y="18" width="24" height="2" rx="1" />
        </svg>
      </button>

      {/*Mobile navigation */}
      <nav
        id="mobile-nav"
        ref={mobileNav}
        className="absolute left-0 top-full z-20 w-full overflow-hidden px-4 transition-all duration-300 ease-in-out sm:px-6"
        style={
          store.visible
            ? { maxHeight: mobileNav.current?.scrollHeight, opacity: 1 }
            : { maxHeight: 0, opacity: 0.8 }
        }
      >
        <ul className="rounded bg-gray-800 px-4 py-2">
          {navigationLinks.map((navigationLink, i) => (
            <li key={i}>
              <Link
                className="flex w-full justify-center py-2 font-medium text-blue-500 hover:underline"
                href={navigationLink.path}
                onClick={store.hide}
              >
                <LocalizedText>{navigationLink.label}</LocalizedText>
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}

const useMobileMenuStore = create<{ hide(): void; toggle(): void; visible: boolean }>((set) => ({
  hide: () => set((state) => (state.visible ? { visible: false } : state)),
  toggle: () => set((state) => ({ visible: !state.visible })),
  visible: false,
}));
