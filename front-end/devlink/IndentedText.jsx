import React from "react";
import * as _Builtin from "./_Builtin";
import { RichText } from "./RichText";
import * as _utils from "./utils";
import _styles from "./IndentedText.module.css";

export function IndentedText({
  as: _Component = _Builtin.VFlex,
  heading = "Studiesociala aktiviteter",
  text = "",
}) {
  return (
    <_Component className={_utils.cx(_styles, "about-section-item")} tag="div">
      <_Builtin.Heading
        className={_utils.cx(_styles, "without-decoration")}
        tag="h2"
      >
        {heading}
      </_Builtin.Heading>
      <RichText content={text} />
    </_Component>
  );
}
