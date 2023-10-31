import { useMemo } from 'react';

import { usePageContext } from '#root/utils/page';

import { Locale } from './locales';
import translate from './translate';

export default function useLocalizedText(
  text: string,
  locale: Locale = usePageContext().locale,
  key?: string,
): string {
  const localizedText = useMemo(() => translate(text, locale, key), [text, locale, key]);

  return localizedText;
}
