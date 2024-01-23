import React from 'react';

import * as _Builtin from './_Builtin';

export function FaqItem({ as: _Component = _Builtin.Block, question = 'Vad är UTN?', answer = '' }) {
  return (
    <_Component className="faq-item-wrapper" tag="div">
      <_Builtin.Heading
        dyn={{
          bind: {},
        }}
        tag="h3"
      >
        {question}
      </_Builtin.Heading>
      <_Builtin.RichText
        className="faq-answer"
        dyn={{
          bind: {},
        }}
        tag="div"
      >
        {answer}
      </_Builtin.RichText>
    </_Component>
  );
}
