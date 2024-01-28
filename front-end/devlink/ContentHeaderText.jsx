import React from "react";
import * as _Builtin from "./_Builtin";
import * as _utils from "./utils";
import _styles from "./ContentHeaderText.module.css";

export function ContentHeaderText({
  as: _Component = _Builtin.VFlex,
  title = "Uppsala teknolog- och naturvetarkår",
  subhead = "Studentkåren för dig som är teknolog eller naturvetare i Uppsala",
}) {
  return (
    <_Component className={_utils.cx(_styles, "block")} tag="div">
      <_Builtin.Heading tag="h1">{title}</_Builtin.Heading>
      <_Builtin.Heading
        className={_utils.cx(_styles, "large-paragraph", "without-decoration")}
        tag="h2"
      >
        {subhead}
      </_Builtin.Heading>
    </_Component>
  );
}
