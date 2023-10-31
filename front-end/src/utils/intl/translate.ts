import translations from '#root/translations';

import { Locale, defaultLocale, defaultTranslationLocale } from './locales';

export default function translate(text: string, locale: Locale, key: string = text): string {
  if (locale === defaultLocale) {
    return text || key;
  }

  const textTranslations = translations[key];

  if (!textTranslations) {
    console.error('No translation(s) of "' + key + '" found.');

    return text || key;
  } else if (
    (typeof textTranslations === 'string' && locale !== defaultTranslationLocale) ||
    !textTranslations[locale]
  ) {
    console.error('No translation of "' + key + '" and locale "' + locale + '" found.');

    return text || key;
  }

  if (typeof textTranslations === 'string') {
    return textTranslations;
  } else {
    return textTranslations[locale];
  }
}
