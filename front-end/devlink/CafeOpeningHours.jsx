import React from "react";
import * as _Builtin from "./_Builtin";
import * as _utils from "./utils";
import _styles from "./CafeOpeningHours.module.css";

export function CafeOpeningHours({ as: _Component = _Builtin.Paragraph }) {
  return (
    <_Component className={_utils.cx(_styles, "footer-paragraph")}>
      {"Måndagar: 9:00–15:00"}
      <br />
      {"Tisdagar:9:00-15:00"}
      <br />
      {"Onsdagar:9:00–15:00"}
      <br />
      {"Torsdagar:10:00–15:00"}
      <br />
      {"Fredagar:9:00–15:00"}
    </_Component>
  );
}
