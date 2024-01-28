import { Role } from '#root/types';

import { teamMocks } from './team-mocks';

export const roleMocks = {
  eventkoordinator: {
    archived: false,
    contact_email: 'eventkoordinator@utn.se',
    id: 4,
    name: 'Eventkoordinator',
    role_type: 'group_leader',
    teams: [teamMocks.eventgruppen],
  } as Role,

  styrelseledamot: {
    archived: false,
    contact_email: 'styrelseledamot@utn.se',
    id: 3,
    name: 'Styrelseledamot',
    role_type: 'presidium',
    teams: [teamMocks.presidiet],
  } as Role,

  systemutvecklare: {
    archived: false,
    contact_email: 'systemutvecklare@utn.se',
    contact_phone_number: '018-471 00 00',
    id: 1,
    name: 'Systemutvecklare',
    role_type: 'admin',
    teams: [teamMocks.digitaliseringsgruppen],
  } as Role,

  utbildningsansvarig: {
    archived: false,
    contact_email: 'utbildningsansvarig@utn.se',
    id: 5,
    name: 'Utbildningsansvarig',
    role_type: 'engaged',
    teams: [teamMocks.utbildningsutskottet],
  } as Role,

  viceProjektledare: {
    archived: false,
    contact_email: 'vice.projektledare@utn.se',
    id: 2,
    name: 'Vice-projektledare',
    role_type: 'board',
    teams: [teamMocks.balkommitten],
  } as Role,
};
