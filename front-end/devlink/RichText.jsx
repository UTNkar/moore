import React from "react";
import * as _Builtin from "./_Builtin";
import * as _utils from "./utils";
import _styles from "./RichText.module.css";

export function RichText({ as: _Component = _Builtin.RichText, content = "" }) {
  return (
    <_Component className={_utils.cx(_styles, "rich-text")} tag="div">
      {content}
    </_Component>
  );
}
