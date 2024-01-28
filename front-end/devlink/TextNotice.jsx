import React from "react";
import * as _Builtin from "./_Builtin";
import { RichText } from "./RichText";
import * as _utils from "./utils";
import _styles from "./TextNotice.module.css";

export function TextNotice({
  as: _Component = _Builtin.VFlex,
  content = "",
  heading = "Medlemsfördelar",
}) {
  return (
    <_Component
      className={_utils.cx(_styles, "content-card", "teal")}
      tag="div"
    >
      <_Builtin.VFlex className={_utils.cx(_styles, "over-dark")} tag="div">
        <_Builtin.Heading tag="h2">{heading}</_Builtin.Heading>
        <RichText content={content} />
      </_Builtin.VFlex>
    </_Component>
  );
}
