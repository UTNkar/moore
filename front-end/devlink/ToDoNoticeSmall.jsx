import React from "react";
import * as _Builtin from "./_Builtin";
import * as _utils from "./utils";
import _styles from "./ToDoNoticeSmall.module.css";

export function ToDoNoticeSmall({
  as: _Component = _Builtin.Block,
  content = "",
}) {
  return (
    <_Component
      className={_utils.cx(_styles, "content-card", "grey")}
      tag="div"
    >
      <_Builtin.Heading tag="h3" editable={false}>
        {"Att göra/under utveckling"}
      </_Builtin.Heading>
      <_Builtin.RichText tag="div">{content}</_Builtin.RichText>
    </_Component>
  );
}
