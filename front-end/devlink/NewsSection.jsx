import React from "react";
import * as _Builtin from "./_Builtin";
import * as _utils from "./utils";
import _styles from "./NewsSection.module.css";

export function NewsSection({ as: _Component = _Builtin.Section }) {
  return (
    <_Component
      className={_utils.cx(_styles, "section")}
      grid={{
        type: "section",
      }}
      tag="section"
    >
      <_Builtin.VFlex className={_utils.cx(_styles, "container")} tag="div">
        <_Builtin.Heading tag="h2">{"Nyheter"}</_Builtin.Heading>
        <_Builtin.NotSupported _atom="DynamoWrapper" />
      </_Builtin.VFlex>
    </_Component>
  );
}
