import { Position } from '#root/types';

import { roleMocks } from './role-mocks';

/* eslint-disable sort-exports/sort-exports */

export const positionMocks: Record<keyof typeof roleMocks, Position> = {
  eventkoordinator: {
    appointments: 1,
    id: 4,
    recruitment_end: '2023-08-31',
    recruitment_start: '2023-06-01',
    role: roleMocks.eventkoordinator,
    term_from: '2024-01-01',
    term_to: '2024-12-31',
  },

  styrelseledamot: {
    appointments: 1,
    id: 3,
    recruitment_end: '2023-08-31',
    recruitment_start: '2023-06-01',
    role: roleMocks.styrelseledamot,
    term_from: '2024-01-01',
    term_to: '2024-12-31',
  },

  systemutvecklare: {
    appointments: 1,
    id: 1,
    recruitment_end: '2023-08-31',
    recruitment_start: '2023-06-01',
    role: roleMocks.systemutvecklare,
    term_from: '2024-01-01',
    term_to: '2024-12-31',
  },

  utbildningsansvarig: {
    appointments: 1,
    id: 5,
    recruitment_end: '2023-08-31',
    recruitment_start: '2023-06-01',
    role: roleMocks.utbildningsansvarig,
    term_from: '2024-01-01',
    term_to: '2024-12-31',
  },

  viceProjektledare: {
    appointments: 1,
    id: 2,
    recruitment_end: '2023-08-31',
    recruitment_start: '2023-06-01',
    role: roleMocks.viceProjektledare,
    term_from: '2024-01-01',
    term_to: '2024-12-31',
  },
};

export const positionListMock: Position[] = [positionMocks.eventkoordinator, positionMocks.viceProjektledare];
