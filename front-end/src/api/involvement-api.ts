import { QueryFunctionContext, UseQueryResult, useQuery } from '@tanstack/react-query';

import type { Position } from '#root/types';

import { positionListMock } from './mocks';
import { ApiContext, useApiContext, wrapWithApiContext } from './utils';

export async function getPositions(
  context: ApiContext,
  _queryContext: QueryFunctionContext,
): Promise<Position[]> {
  if (context.mock) {
    return positionListMock;
  } else {
    throw new Error('Missing implementation');
  }
}

export function usePositions(context: ApiContext = useApiContext()): UseQueryResult<Position[], Error> {
  return useQuery({
    queryFn: wrapWithApiContext(context, getPositions),
    queryHash: context.queryHash,
    queryKey: ['positions'],
  });
}
