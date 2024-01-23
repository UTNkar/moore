import React from 'react';

import * as _Builtin from './_Builtin';

export function MembershipModuleInfoCard({ as: _Component = _Builtin.Link }) {
  return (
    <_Component
      className="module-item-list-card"
      button={false}
      block="inline"
      options={{
        href: '#',
      }}
    >
      <_Builtin.Heading className="without-spacing" tag="h2">
        {'Om medlemssystemet'}
      </_Builtin.Heading>
      <_Builtin.Paragraph className="without-spacing">
        {
          'Vi ser till att din profil är både registrerad hos Mecenat och i vårt egna system. Det gör att du kan ta det av Mecenats erbjudanden och att du enkelt kan söka våra engagemang samt anmäla dig till våra evenemang. '
        }
      </_Builtin.Paragraph>
    </_Component>
  );
}
