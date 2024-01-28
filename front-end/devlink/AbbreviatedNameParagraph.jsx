import React from "react";
import * as _Builtin from "./_Builtin";
import * as _utils from "./utils";
import _styles from "./AbbreviatedNameParagraph.module.css";

export function AbbreviatedNameParagraph({ as: _Component = _Builtin.VFlex }) {
  return (
    <_Component className={_utils.cx(_styles, "block")} tag="div">
      <_Builtin.VFlex className={_utils.cx(_styles, "paragraph-row")} tag="div">
        <_Builtin.Paragraph
          className={_utils.cx(_styles, "paragraph-row-item")}
        >
          {"Name"}
        </_Builtin.Paragraph>
        <_Builtin.Paragraph
          className={_utils.cx(_styles, "paragraph-row-item", "spaced")}
        >
          {"("}
        </_Builtin.Paragraph>
        <_Builtin.Paragraph
          className={_utils.cx(_styles, "paragraph-row-item")}
        >
          {"N"}
        </_Builtin.Paragraph>
        <_Builtin.Paragraph
          className={_utils.cx(_styles, "paragraph-row-item")}
        >
          {")"}
        </_Builtin.Paragraph>
      </_Builtin.VFlex>
    </_Component>
  );
}
