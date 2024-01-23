import React from 'react';

import * as _Builtin from './_Builtin';
import { RichText } from './RichText';

export function TextNotice({ as: _Component = _Builtin.VFlex, content = '', heading = 'Medlemsfördelar' }) {
  return (
    <_Component className="content-card teal" tag="div">
      <_Builtin.VFlex className="over-dark" tag="div">
        <_Builtin.Heading tag="h2">{heading}</_Builtin.Heading>
        <RichText content={content} />
      </_Builtin.VFlex>
    </_Component>
  );
}
