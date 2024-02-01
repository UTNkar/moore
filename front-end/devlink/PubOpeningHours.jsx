import React from "react";
import * as _Builtin from "./_Builtin";
import * as _utils from "./utils";
import _styles from "./PubOpeningHours.module.css";

export function PubOpeningHours({ as: _Component = _Builtin.Paragraph }) {
  return (
    <_Component className={_utils.cx(_styles, "footer-paragraph")}>
      {"Torsdagar: 17:30–sent"}
    </_Component>
  );
}
