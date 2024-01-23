import React from 'react';

import * as _Builtin from './_Builtin';

export function AbbreviatedNameParagraph({ as: _Component = _Builtin.VFlex }) {
  return (
    <_Component className="block" tag="div">
      <_Builtin.VFlex className="paragraph-row" tag="div">
        <_Builtin.Paragraph className="paragraph-row-item">{'Name'}</_Builtin.Paragraph>
        <_Builtin.Paragraph className="paragraph-row-item spaced">{'('}</_Builtin.Paragraph>
        <_Builtin.Paragraph className="paragraph-row-item">{'N'}</_Builtin.Paragraph>
        <_Builtin.Paragraph className="paragraph-row-item">{')'}</_Builtin.Paragraph>
      </_Builtin.VFlex>
    </_Component>
  );
}
