import clsx from 'clsx';

import { Container as WebflowContainer } from '#root/devlink/_Builtin';
import { PropsWithChildren } from '#root/utils/types';

export default function Container(props: PropsWithChildren<{}>) {
  const { children } = props;

  return (
    <WebflowContainer tag="div" className={clsx('container')}>
      {children}
    </WebflowContainer>
  );
}
