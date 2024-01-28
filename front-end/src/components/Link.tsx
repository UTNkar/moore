import { Locale, defaultLocale } from '#root/utils/intl';
import { usePageContext } from '#root/utils/page';

export default function Link({ locale, href, keepScrollPosition, hasSubpaths, ...props }: LinkProps) {
  const pageContext = usePageContext();

  const className = [
    props.className,
    (!hasSubpaths || href === '/'
      ? pageContext.urlPathname === href
      : pageContext.urlPathname.startsWith(href)) && 'active',
  ]
    .filter(Boolean)
    .join(' ');

  locale = locale || pageContext.locale;

  if (href && href.charAt(0) !== '#' && locale !== defaultLocale) {
    href = '/' + locale + href;
  }

  /* eslint-disable jsx-a11y/anchor-has-content */

  return (
    <a
      {...props}
      href={href}
      className={className}
      {...(keepScrollPosition ? { 'keep-scroll-position': true } : {})}
    />
  );
}

export type LinkProps = React.AnchorHTMLAttributes<HTMLAnchorElement> & {
  hasSubpaths?: boolean;
  keepScrollPosition?: boolean;
  locale?: Locale;
};
