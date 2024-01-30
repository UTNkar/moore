import clsx from 'clsx';

import Link, { LinkProps } from '#root/components/Link';

export default function ModuleListItemCard({
  active,
  className,
  children,
  ...otherProps
}: { active: boolean } & LinkProps) {
  return (
    <Link
      {...otherProps}
      className={clsx('module-item-list-card w-inline-block', active && 'active', className)}
    >
      {children}
    </Link>
  );
}
