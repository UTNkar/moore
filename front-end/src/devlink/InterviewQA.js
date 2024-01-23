import React from 'react';

import * as _Builtin from './_Builtin';

export function InterviewQA({
  as: _Component = _Builtin.VFlex,
  question = 'Question?',
  answer = 'Answer.',
  heading = 'Heading',
}) {
  return (
    <_Component className="remove-first-child-spacing block" tag="div">
      <_Builtin.Heading tag="h2">{heading}</_Builtin.Heading>
      <_Builtin.Paragraph>{question}</_Builtin.Paragraph>
      <_Builtin.Blockquote>{answer}</_Builtin.Blockquote>
    </_Component>
  );
}
