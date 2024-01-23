import React from 'react';

import * as _Builtin from './_Builtin';

export function SectionCard({
  as: _Component = _Builtin.Block,
  acronym = 'XX',
  programs = 'Program som ingår i sektionen.',

  link = {
    href: 'https://i.utn.se',
  },

  linkLabel = 'i.utn.se',
}) {
  return (
    <_Component className="card" tag="div">
      <_Builtin.Block className="card-text" tag="div">
        <_Builtin.VFlex className="section-name-wrapper" tag="div">
          <_Builtin.Heading
            className="section-name without-decoration without-spacing"
            dyn={{
              bind: {},
            }}
            tag="h3"
          >
            {acronym}
          </_Builtin.Heading>
          <_Builtin.Heading
            className="section-name-suffix without-decoration without-spacing"
            dyn={{
              bind: {},
            }}
            tag="h3"
          >
            {'-sektionen'}
          </_Builtin.Heading>
        </_Builtin.VFlex>
        <_Builtin.Heading tag="h4">{'Inkluderade program'}</_Builtin.Heading>
        <_Builtin.Paragraph>{programs}</_Builtin.Paragraph>
        <_Builtin.Heading tag="h4">{'Sektionsförening'}</_Builtin.Heading>
        <_Builtin.Paragraph
          dyn={{
            bind: {},
          }}
        >
          <_Builtin.Link button={false} block="" options={link}>
            {linkLabel}
          </_Builtin.Link>
        </_Builtin.Paragraph>
      </_Builtin.Block>
    </_Component>
  );
}
