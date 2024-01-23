import React from 'react';

import * as _Builtin from './_Builtin';
import { RichText } from './RichText';

export function IndentedText({
  as: _Component = _Builtin.VFlex,
  heading = 'Studiesociala aktiviteter',
  text = '',
}) {
  return (
    <_Component className="about-section-item" tag="div">
      <_Builtin.Heading className="without-decoration" tag="h2">
        {heading}
      </_Builtin.Heading>
      <RichText content={text} />
    </_Component>
  );
}
