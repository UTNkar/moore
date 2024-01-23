import React from 'react';

import * as _Builtin from './_Builtin';

export function EventsModuleItemHeader({ as: _Component = _Builtin.Block }) {
  return (
    <_Component className="module-item-header" tag="div">
      <_Builtin.Block className="module-item-list-icon-wrapper" tag="div">
        <_Builtin.Image
          className="involvement-list-icon"
          loading="lazy"
          width="auto"
          height="auto"
          alt=""
          src="https://uploads-ssl.webflow.com/655e29844518537470ba5b0f/65ad52a2db24d07113b5574d_Naturvetarbalen.png"
        />
      </_Builtin.Block>
      <_Builtin.Block className="module-item-list-labels" tag="div">
        <_Builtin.Heading className="without-decoration without-spacing" tag="h4">
          {'Naturvetarbalen 2024'}
        </_Builtin.Heading>
        <_Builtin.Block className="paragraph-row without-spacing" tag="div">
          <_Builtin.Paragraph className="card-subhead paragraph-row-item">
            {'1,400–1,850 kr'}
          </_Builtin.Paragraph>
          <_Builtin.Paragraph className="card-subhead paragraph-row-item">{' - '}</_Builtin.Paragraph>
          <_Builtin.Paragraph className="card-subhead paragraph-row-item">{'31 jan'}</_Builtin.Paragraph>
        </_Builtin.Block>
      </_Builtin.Block>
    </_Component>
  );
}
