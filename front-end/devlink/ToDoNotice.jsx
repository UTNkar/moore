import React from "react";
import * as _Builtin from "./_Builtin";
import * as _utils from "./utils";
import _styles from "./ToDoNotice.module.css";

export function ToDoNotice({
  as: _Component = _Builtin.Section,
  content = "",
  visible = true,
}) {
  return visible ? (
    <_Component
      className={_utils.cx(_styles, "section")}
      grid={{
        type: "section",
      }}
      tag="section"
    >
      <_Builtin.BlockContainer
        className={_utils.cx(_styles, "container")}
        grid={{
          type: "container",
        }}
        tag="div"
      >
        <_Builtin.Block
          className={_utils.cx(_styles, "content-card", "grey")}
          tag="div"
        >
          <_Builtin.Heading tag="h2">{"Att göra"}</_Builtin.Heading>
          <_Builtin.RichText tag="div">{content}</_Builtin.RichText>
        </_Builtin.Block>
      </_Builtin.BlockContainer>
    </_Component>
  ) : null;
}
