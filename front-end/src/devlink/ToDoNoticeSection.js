import React from 'react';

import * as _Builtin from './_Builtin';

export function ToDoNoticeSection({ as: _Component = _Builtin.Section, content = '', visible = true }) {
  return visible ? (
    <_Component
      className="section"
      grid={{
        type: 'section',
      }}
      tag="section"
    >
      <_Builtin.BlockContainer
        className="container"
        grid={{
          type: 'container',
        }}
        tag="div"
      >
        <_Builtin.Block className="content-card grey" tag="div">
          <_Builtin.Heading tag="h2">{'Att göra'}</_Builtin.Heading>
          <_Builtin.RichText tag="div">{content}</_Builtin.RichText>
        </_Builtin.Block>
      </_Builtin.BlockContainer>
    </_Component>
  ) : null;
}
