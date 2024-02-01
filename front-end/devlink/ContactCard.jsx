import React from 'react';

import * as _Builtin from './_Builtin';
import _styles from './ContactCard.module.css';
import * as _utils from './utils';

export function ContactCard({
  as: _Component = _Builtin.Block,
  photo = '',
  name = 'Per Wahlund',
  role = 'En givmild man',

  mailLink = {
    href: 'mailto:per@wahlund.se',
  },

  mailLabel = 'per@wahlund.se',

  phoneLink = {
    href: 'tel:+46722533211',
  },

  phoneLabel = '072- 253 32 11',
}) {
  return (
    <_Component className={_utils.cx(_styles, 'card')} tag="div">
      <_Builtin.Block
        className={_utils.cx(_styles, 'contact-card-thumbnail')}
        dyn={{
          bind: {},
        }}
        tag="div"
      >
        <_Builtin.Image
          className={_utils.cx(_styles, 'contact-card-photo')}
          loading="lazy"
          width="auto"
          height="auto"
          alt=""
          src={photo}
        />
      </_Builtin.Block>
      <_Builtin.Block className={_utils.cx(_styles, 'card-text')} tag="div">
        <_Builtin.Heading
          className={_utils.cx(_styles, 'without-decoration', 'without-spacing')}
          dyn={{
            bind: {},
          }}
          tag="h4"
        >
          {name}
        </_Builtin.Heading>
        <_Builtin.Heading
          className={_utils.cx(_styles, 'card-subhead', 'without-decoration')}
          dyn={{
            bind: {},
          }}
          tag="h5"
        >
          {role}
        </_Builtin.Heading>
        <_Builtin.Paragraph className={_utils.cx(_styles, 'standalone-link')}>
          <_Builtin.Link button={false} options={mailLink}>
            {mailLabel}
          </_Builtin.Link>
          <br />
          <_Builtin.Link button={false} options={phoneLink}>
            {phoneLabel}
          </_Builtin.Link>
        </_Builtin.Paragraph>
      </_Builtin.Block>
    </_Component>
  );
}
