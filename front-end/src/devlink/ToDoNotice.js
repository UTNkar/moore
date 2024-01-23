import React from 'react';

import * as _Builtin from './_Builtin';

export function ToDoNotice({ as: _Component = _Builtin.Block, content = '' }) {
  return (
    <_Component className="content-card grey" tag="div">
      <_Builtin.Heading tag="h3" editable={false}>
        {'Att göra/under utveckling'}
      </_Builtin.Heading>
      <_Builtin.RichText tag="div">{content}</_Builtin.RichText>
    </_Component>
  );
}
