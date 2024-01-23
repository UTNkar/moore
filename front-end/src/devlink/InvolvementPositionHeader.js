import React from 'react';

import * as _Builtin from './_Builtin';

export function InvolvementPositionHeader({
  as: _Component = _Builtin.Block,
  title = 'Systemutvecklare 23/24',
  team = 'Digitaliseringsgruppen',
  finalDate = '31 jan',
}) {
  return (
    <_Component className="module-item-header" tag="div">
      <_Builtin.Block className="module-item-list-icon-wrapper" tag="div">
        <_Builtin.Image
          className="involvement-list-icon"
          loading="lazy"
          width="auto"
          height="auto"
          alt="Uppsala teknolog- och naturverarkår"
          src="https://uploads-ssl.webflow.com/655e29844518537470ba5b0f/655e33434a15645ce5ef1708_logo-square-blue.svg"
        />
      </_Builtin.Block>
      <_Builtin.Block className="module-item-list-labels" tag="div">
        <_Builtin.Heading className="without-decoration without-spacing" tag="h4">
          {title}
        </_Builtin.Heading>
        <_Builtin.Block className="paragraph-row without-spacing" tag="div">
          <_Builtin.Paragraph className="card-subhead paragraph-row-item">{team}</_Builtin.Paragraph>
          <_Builtin.Paragraph className="card-subhead paragraph-row-item">{' - '}</_Builtin.Paragraph>
          <_Builtin.Paragraph className="card-subhead paragraph-row-item">{finalDate}</_Builtin.Paragraph>
        </_Builtin.Block>
      </_Builtin.Block>
    </_Component>
  );
}
