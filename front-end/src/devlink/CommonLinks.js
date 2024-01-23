import React from 'react';

import * as _Builtin from './_Builtin';

export function CommonLinks({
  as: _Component = _Builtin.VFlex,
  urlLabel = 'url.se',

  url = {
    href: 'https://url.se',
  },

  phoneLabel = '072-253 32 11',

  phone = {
    href: 'tel:+4672-2533211',
  },

  eMail = {
    href: '#',
  },

  eMailLabel = '',
}) {
  return (
    <_Component className="block" tag="div">
      <_Builtin.Paragraph
        dyn={{
          bind: {},
        }}
      >
        <_Builtin.Link className="block" button={false} block="" options={url}>
          {urlLabel}
        </_Builtin.Link>
        <_Builtin.Link className="block" button={false} block="" options={eMail}>
          {eMailLabel}
        </_Builtin.Link>
        <_Builtin.Link className="block" button={false} block="" options={phone}>
          {phoneLabel}
        </_Builtin.Link>
      </_Builtin.Paragraph>
    </_Component>
  );
}
