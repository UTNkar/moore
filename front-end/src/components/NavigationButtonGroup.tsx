import clsx from 'clsx';

import { LocalizedText } from '#root/utils/intl';

export default function NavigationButtonGroup({ exclude }: { exclude?: 'involvement' | 'event' | 'member' }) {
  const links = (
    [
      ['involvement', 'Engagemang'],
      ['event', 'Event'],
      ['member', 'Medlemskap'],
    ] as ['involvement' | 'event' | 'member', string][]
  )
    .filter((tuple) => tuple[0] !== exclude)
    .map((tuple, i) => {
      const left = i === 0 || (!exclude && i === 1);
      const right = i > 0;

      return (
        <a
          key={tuple[0]}
          href={'/' + tuple[0]}
          className={clsx('large-button secondary w-button', { left: left, right: right })}
        >
          <LocalizedText element="span">{tuple[1]}</LocalizedText>
        </a>
      );
    });

  return (
    <div className="w-layout-vflex large-button-group-wrapper">
      <div className="w-layout-vflex button-group-wrapper">{links}</div>
    </div>
  );
}
