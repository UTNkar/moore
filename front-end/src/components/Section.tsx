import clsx from 'clsx';

import { Section as WebflowSection } from '#root/devlink/_Builtin/Basic';
import { PropsWithChildren } from '#root/utils/types';

export default function Section(props: PropsWithChildren<{ emphasised?: boolean; subdued?: boolean }>) {
  const { children, emphasised, subdued } = props;

  return (
    <WebflowSection tag="section" className={clsx('section', { emphasised: emphasised, subdued: subdued })}>
      {children}
    </WebflowSection>
  );
}
