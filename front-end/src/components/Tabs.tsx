import clsx from 'clsx';

import type { Falsy } from '#root/utils/types';

import Link, { LinkProps } from './Link';

export interface TabOptions extends LinkProps {
  key?: React.Key;
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
        return <Link key={index} keepScrollPosition {...tab} className={clsx('module-tab', tab.className)} />;
      })}
    </div>
  );
}
