import type { PageContextServer } from 'vike/types';

import { getPositions } from '#root/api';
import { apiContextFromPageContext } from '#root/api/utils';
import { Position } from '#root/types';

export default async function data(pageContext: PageContextServer): Promise<InvolvementPageData> {
  const apiContext = apiContextFromPageContext(pageContext);
  const positions = await getPositions(apiContext);

  return { positions };
}

export interface InvolvementPageData {
  positions: Position[];
}
