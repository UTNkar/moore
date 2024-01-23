import React from 'react';

import * as _Builtin from './_Builtin';

export function SpecialNotice({
  as: _Component = _Builtin.Link,
  heading = 'Heading',
  text = 'Vi har nu utsett vinnaren. Klicka här för att se mer',
}) {
  return (
    <_Component
      className="special-notice"
      button={false}
      block="inline"
      options={{
        href: '#',
      }}
    >
      <_Builtin.Heading className="without-decoration" tag="h3">
        {heading}
      </_Builtin.Heading>
      <_Builtin.Paragraph>{text}</_Builtin.Paragraph>
    </_Component>
  );
}
