import React from 'react';

import * as _Builtin from './_Builtin';

export function EngagementHeader({ as: _Component = _Builtin.NotSupported }) {
  return (
    <_Component _atom="DOM">
      <_Builtin.BlockContainer
        className="full-width container"
        grid={{
          type: 'container',
        }}
        tag="div"
      >
        <_Builtin.VFlex className="secondary-navbar-wrapper" tag="div">
          <_Builtin.VFlex className="navbar-item-group" tag="div">
            <_Builtin.Link
              className="secondary-navbar-item-wrapper"
              button={false}
              block="inline"
              options={{
                href: '#',
              }}
            >
              <_Builtin.Block className="secondary-navbar-item-label" tag="div">
                {'Lediga poster'}
              </_Builtin.Block>
            </_Builtin.Link>
            <_Builtin.Link
              className="secondary-navbar-item-wrapper"
              button={false}
              block="inline"
              options={{
                href: '#',
              }}
            >
              <_Builtin.Block className="secondary-navbar-item-label" tag="div">
                {'Sökta poster'}
              </_Builtin.Block>
            </_Builtin.Link>
          </_Builtin.VFlex>
          <_Builtin.VFlex className="navbar-item-group separated" tag="div">
            <_Builtin.Link
              className="secondary-navbar-item-wrapper"
              button={false}
              block="inline"
              options={{
                href: '#',
              }}
            >
              <_Builtin.Block className="secondary-navbar-item-label" tag="div">
                {'Min profil'}
              </_Builtin.Block>
            </_Builtin.Link>
          </_Builtin.VFlex>
        </_Builtin.VFlex>
      </_Builtin.BlockContainer>
    </_Component>
  );
}
