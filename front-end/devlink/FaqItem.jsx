import React from "react";
import * as _Builtin from "./_Builtin";
import * as _utils from "./utils";
import _styles from "./FaqItem.module.css";

export function FaqItem({
  as: _Component = _Builtin.Block,
  question = "Vad är UTN?",
  answer = "",
}) {
  return (
    <_Component className={_utils.cx(_styles, "faq-item-wrapper")} tag="div">
      <_Builtin.Heading
        dyn={{
          bind: {},
        }}
        tag="h3"
      >
        {question}
      </_Builtin.Heading>
      <_Builtin.RichText
        className={_utils.cx(_styles, "faq-answer")}
        dyn={{
          bind: {},
        }}
        tag="div"
      >
        {answer}
      </_Builtin.RichText>
    </_Component>
  );
}
