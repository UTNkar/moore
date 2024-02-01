import moduleNavigationLinks from '#root/renderer/layout/moduleItems';
import { LocalizedText } from '#root/utils/intl';

import Link from '../../components/Link';

export function ModulesDesktop() {
  return (
    <nav className="navbar navbar-expand-lg bg-primary">
      <div className="container-fluid">
        <div className="navbar-nav">
          {moduleNavigationLinks.map((navigationLink, i) => (
            <Link key={i} href={navigationLink.path} className="nav-link">
              <LocalizedText className="text-white">{navigationLink.label}</LocalizedText>
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
