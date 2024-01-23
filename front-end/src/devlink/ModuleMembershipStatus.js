import React from 'react';

import * as _Builtin from './_Builtin';

export function ModuleMembershipStatus({ as: _Component = _Builtin.Block }) {
  return (
    <_Component className="content-card small blue over-dark" tag="div">
      <_Builtin.Heading tag="h4">{'Tack för att du är medlem i UTN'}</_Builtin.Heading>
      <_Builtin.Paragraph>
        {
          'I detta fall sparar du mellan 100 och 240 kr på ditt medlemskap, beroende på vilka tillägg du väljer.'
        }
      </_Builtin.Paragraph>
    </_Component>
  );
}
