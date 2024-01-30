import { FormattedMessage } from 'react-intl';

import { usePositions } from '#root/api';
import PositionModuleListItem, {
  PositionModuleListItemHeader,
} from '#root/components/involvement/PositionModuleListItem';
import ModuleBodyWrapper from '#root/components/module/ModuleBodyWrapper';
import ModuleContentDivider from '#root/components/module/ModuleContentDivider';
import ModuleRichText from '#root/components/module/ModuleRichText';
import SidebarWrapper from '#root/components/module/ModuleSidebarWrapper';
import { useFormattedDate } from '#root/utils/intl';
import { PageProps, useActiveItem } from '#root/utils/page';

import type { InvolvementPageData } from './+data';

export default function InvolvementPage({ pageContext }: PageProps<InvolvementPageData>) {
  const positions = usePositions<InvolvementPageData>('positions');

  const activePosition = useActiveItem(positions.data, {
    fallbackFirst: true,
    idKey: 'id',
    numberKeys: ['id'],
    stringKeys: [],
  });

  const formattedTermOfOffice = {
    from: useFormattedDate(activePosition?.term_from),
    to: useFormattedDate(activePosition?.term_to),
  };

  return (
    <>
      <SidebarWrapper>
        {positions.data?.map((position) => {
          return (
            <PositionModuleListItem
              key={position.id}
              href={'/involvement/' + position.id}
              active={activePosition === position}
              position={position}
            />
          );
        })}
      </SidebarWrapper>

      <ModuleBodyWrapper>
        {activePosition && (
          <>
            <PositionModuleListItemHeader position={activePosition} />

            <ModuleContentDivider />

            {formattedTermOfOffice.from && formattedTermOfOffice.to && (
              <FormattedMessage
                tagName="p"
                id="Mandatperioden löper mellan {from_date} och {to_date}."
                values={{ from_date: formattedTermOfOffice.from, to_date: formattedTermOfOffice.to }}
              />
            )}

            {activePosition.role.description && <ModuleRichText html={activePosition.role.description} />}

            {activePosition.comment && <ModuleRichText html={activePosition.comment} />}
          </>
        )}
      </ModuleBodyWrapper>
    </>
  );
}
