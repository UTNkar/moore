import React from 'react';

import * as _Builtin from './_Builtin';
import { ContentHeaderText } from './ContentHeaderText';

export function HomeIntroductionPageBlock({
  as: _Component = _Builtin.Section,
  title = 'Uppsala teknolog- och naturvetarkår',
  subhead = 'Studentkåren för dig som är teknolog eller naturvetare i Uppsala',
}) {
  return (
    <_Component
      className="section"
      grid={{
        type: 'section',
      }}
      tag="section"
    >
      <_Builtin.VFlex className="container" tag="div">
        <ContentHeaderText title={title} subhead={subhead} />
        <_Builtin.VFlex className="large-button-group-wrapper" tag="div">
          <_Builtin.Link
            className="large-button"
            button={true}
            block=""
            options={{
              href: '/engagera-dig',
            }}
          >
            {'Bli medlem'}
          </_Builtin.Link>
          <_Builtin.VFlex className="button-group-wrapper" tag="div">
            <_Builtin.Link
              className="large-button secondary left"
              button={true}
              block=""
              options={{
                href: '/engagera-dig',
              }}
            >
              {'Engagera dig'}
            </_Builtin.Link>
            <_Builtin.Link
              className="large-button right secondary"
              button={true}
              block=""
              options={{
                href: '/engagera-dig',
              }}
            >
              {'Påverka studierna'}
            </_Builtin.Link>
          </_Builtin.VFlex>
        </_Builtin.VFlex>
      </_Builtin.VFlex>
    </_Component>
  );
}
