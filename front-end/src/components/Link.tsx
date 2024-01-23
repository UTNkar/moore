import { Locale, defaultLocale } from '#root/utils/intl';
import { usePageContext } from '#root/utils/page';

export default function Link({ locale, href, keepScrollPosition, ...props }: LinkProps) {
  const pageContext = usePageContext();

  const className = [props.className, pageContext.urlPathname === href && 'active'].filter(Boolean).join(' ');

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
  keepScrollPosition?: boolean;
  locale?: Locale;
};
