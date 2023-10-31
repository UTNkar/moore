import headlessUIPlugin from '@headlessui/tailwindcss';
import aspectRatioPlugin from '@tailwindcss/aspect-ratio';
import formsPlugin from '@tailwindcss/forms';
import typographyPlugin from '@tailwindcss/typography';
import childrenPlugin from 'tailwind-children';
import type { Config } from 'tailwindcss';
import colors from 'tailwindcss/colors';

const config: Config = {
  content: {
    files: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
    relative: true,
  },
  darkMode: 'class',
  plugins: [formsPlugin, aspectRatioPlugin, typographyPlugin, childrenPlugin, headlessUIPlugin],
  theme: {
    colors: {
      ...colors,
      black: '#000000',
      blue: {
        // UTN-huvudfärg: blå
        50: '#79BCFF',
        100: '#65B2FF',
        200: '#3C9EFF',
        300: '#1389FF',
        400: '#0075EA',
        500: '#0060C1',
        600: '#004C98',
        700: '#003060',
        800: '#001428',
        900: '#000000',
        950: '#000000',
        DEFAULT: '#004C98',
      },
      indigo: {
        // UTN-komplementfärg: stark blå
        50: '#9895FA',
        100: '#8581F9',
        200: '#5F5AF7',
        300: '#3933F5',
        400: '#140CF3',
        500: '#100ACD',
        600: '#0D08A6',
        700: '#090570',
        800: '#05033B',
        900: '#000005',
        950: '#000000',
        DEFAULT: '#0D08A6',
      },
      sky: {
        // UTN-komplementfärg: ljusare blå
        50: '#9FE4FA',
        100: '#8CDFF9',
        200: '#65D4F7',
        300: '#3EC9F5',
        400: '#17BFF3',
        500: '#0BA6D7',
        600: '#0988B0',
        700: '#065F7B',
        800: '#043645',
        900: '#010C10',
        950: '#000000',
        DEFAULT: '#0988B0',
      },
      teal: {
        // UTN-komplementfärg: turkos
        50: '#95FAF7',
        100: '#81F9F5',
        200: '#5AF7F2',
        300: '#33F5EF',
        400: '#0CF3EC',
        500: '#0ACDC7',
        600: '#08A6A1',
        700: '#05706D',
        800: '#033B39',
        900: '#000505',
        950: '#000000',
        DEFAULT: '#08A6A1',
      },
      white: '#FFFFFF',
    },
    extend: {
      backgroundImage: {
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      },
    },
    fontFamily: {
      mono: ['Inconsolata', 'Menlo', 'monospace'],
      sans: ['Outfit', 'Noto Sans', 'Inter', 'system-ui', 'Avenir', 'Helvetica', 'Arial', 'sans-serif'],
      serif: ['Domine', 'Merriweather', 'serif'],
    },
  },
};

export default config;
