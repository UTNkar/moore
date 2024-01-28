import clsx from 'clsx';

import { LocalizedText } from '#root/utils/intl';
import type { Falsy } from '#root/utils/types';

import Link, { LinkProps } from './Link';

export interface TabOptions extends Omit<LinkProps, 'children'> {
  key?: React.Key;
  label: string;
}

export interface TabsProps {
  tabs: (TabOptions | 'space' | Falsy)[];
}

export default function Tabs({ tabs }: TabsProps): JSX.Element {
  return (
    <div className="module-tabs w-layout-hflex">
      {tabs.map((tab, index) => {
        if (tab === 'space') {
          return <div key={index} className="spacer" />;
        } else if (!tab) {
          return null;
        }

        // eslint-disable-next-line jsx-a11y/anchor-has-content
        return (
          <Link key={index} {...tab} className={clsx('module-tab', tab.className)}>
            <LocalizedText element="h4" className="without-decoration without-spacing">
              {tab.label}
            </LocalizedText>
          </Link>
        );
      })}
    </div>
  );
}
