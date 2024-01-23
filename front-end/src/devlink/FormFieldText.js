import React from 'react';

import * as _Builtin from './_Builtin';

export function FormFieldText({ as: _Component = _Builtin.VFlex, label = 'Sektion' }) {
  return (
    <_Component className="form-field-wrapper" tag="div">
      <_Builtin.FormBlockLabel htmlFor="name-2">{label}</_Builtin.FormBlockLabel>
      <_Builtin.FormTextInput
        className="text-field"
        autoFocus={false}
        maxLength={256}
        name="name-2"
        data-name="Name 2"
        placeholder="..."
        type="text"
        disabled={false}
        required={false}
        id="name-2"
      />
    </_Component>
  );
}
