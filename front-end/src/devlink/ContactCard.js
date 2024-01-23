import React from 'react';

import * as _Builtin from './_Builtin';

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
  thumbnailVisible = true,
}) {
  return (
    <_Component className="card" tag="div">
      {thumbnailVisible ? (
        <_Builtin.Block
          className="contact-card-thumbnail"
          dyn={{
            bind: {},
          }}
          tag="div"
        >
          <_Builtin.Image
            className="contact-card-photo"
            loading="lazy"
            width="auto"
            height="auto"
            alt=""
            src={photo}
          />
        </_Builtin.Block>
      ) : null}
      <_Builtin.Block className="card-text" tag="div">
        <_Builtin.Heading
          className="without-decoration without-spacing"
          dyn={{
            bind: {},
          }}
          tag="h4"
        >
          {name}
        </_Builtin.Heading>
        <_Builtin.Heading
          className="card-subhead without-decoration"
          dyn={{
            bind: {},
          }}
          tag="h5"
        >
          {role}
        </_Builtin.Heading>
        <_Builtin.Paragraph className="standalone-link">
          <_Builtin.Link button={false} block="" options={mailLink}>
            {mailLabel}
          </_Builtin.Link>
          <br />
          <_Builtin.Link button={false} block="" options={phoneLink}>
            {phoneLabel}
          </_Builtin.Link>
        </_Builtin.Paragraph>
      </_Builtin.Block>
    </_Component>
  );
}
