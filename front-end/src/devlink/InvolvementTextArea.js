import React from 'react';

import * as _Builtin from './_Builtin';

export function InvolvementTextArea({
  as: _Component = _Builtin.VFlex,
  heading = 'Personligt brev',
  subhead = 'Presentera dig själv och skriv varför just du är rätt person för posten.',
}) {
  return (
    <_Component className="block" tag="div">
      <_Builtin.Heading tag="h4">{heading}</_Builtin.Heading>
      <_Builtin.Paragraph>{subhead}</_Builtin.Paragraph>
      <_Builtin.FormTextarea
        className="content-card small bordered text-area"
        required={false}
        autoFocus={false}
        placeholder="..."
        maxLength={5000}
        name="Field-X"
        data-name="Field X"
        id="Field-X"
      />
    </_Component>
  );
}
