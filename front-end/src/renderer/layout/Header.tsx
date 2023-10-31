import Link from '#root/components/Link';
import LogoIcon from '#root/components/LogoIcon';
import { useLocalizedText } from '#root/utils/intl';
// import { LocalizedText } from '#root/utils/intl';

// import MobileMenu from './MobileMenu';
// import navigationLinks from './navigationLinks';

export default function Header() {
  return (
    <header className="absolute z-30 w-full">
      <div className="container">
        <div className="flex h-20 items-center justify-between">
          <div className="mr-4 shrink-0">
            <Link
              href="/"
              className="block"
              aria-label={useLocalizedText('Uppsala teknolog- och naturvetarkår')}
            >
              <LogoIcon className="h-10 w-10 fill-blue" />
            </Link>
          </div>

          {/* Desktop navigation */}
          {/* <nav className="hidden md:flex md:grow">
            <ul className="flex grow flex-wrap items-center justify-end">
              {navigationLinks.map((navigationLink, i) => (
                <li key={i}>
                  <Link
                    className="flex items-center px-4 py-3 font-semibold text-blue-600 transition duration-150 ease-in-out hover:underline"
                    href={navigationLink.path}
                  >
                    <LocalizedText>{navigationLink.label}</LocalizedText>
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          <MobileMenu /> */}
        </div>
      </div>
    </header>
  );
}
