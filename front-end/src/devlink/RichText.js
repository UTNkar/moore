import React from 'react';

import * as _Builtin from './_Builtin';

export function RichText({ as: _Component = _Builtin.RichText, content = '' }) {
  return (
    <_Component className="rich-text" tag="div">
      {content}
    </_Component>
  );
}
