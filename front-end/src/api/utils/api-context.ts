import type { Locale } from '#root/utils/intl';
import { usePageContext } from '#root/utils/page';

import type { memberMocks } from '../mocks';

export function useApiContext(): ApiContext {
  const pageContext = usePageContext();

  return { locale: pageContext.locale, mock: true, queryHash: pageContext.locale };
}

export function wrapWithApiContext<P extends any[], RT>(
  context: ApiContext,
  func: (context: ApiContext, ..._parameters: P) => RT,
): (..._parameters: P) => RT {
  return (...params) => func(context, ...params);
}

export interface ApiContext {
  bearerToken?: string;
  csrfToken?: string;
  locale: Locale;
  mock?: boolean;
  mockMember?: keyof typeof memberMocks;
  queryHash: string;
}
