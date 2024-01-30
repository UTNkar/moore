import { QueryFunctionContext, UseQueryResult } from '@tanstack/react-query';

import type { Position } from '#root/types';

import { positionListMock } from './mocks';
import { ApiContext, PageDataKey, useApiContext, usePageDataQuery } from './utils';

export async function getPositions(
  context: ApiContext,
  _queryContext?: QueryFunctionContext,
): Promise<Position[]> {
  if (context.mock) {
    return positionListMock;
  } else {
    throw new Error('Missing implementation');
  }
}

export function usePositions<PageData = unknown>(
  pageDataKey: PageDataKey<PageData, Position[]>,
  context: ApiContext<PageData> = useApiContext(),
): UseQueryResult<Position[], Error> {
  return usePageDataQuery<PageData, Position[]>(getPositions, pageDataKey, [], context);
}
