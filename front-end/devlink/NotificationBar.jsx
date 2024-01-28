import React from "react";
import * as _Builtin from "./_Builtin";
import * as _utils from "./utils";
import _styles from "./NotificationBar.module.css";

export function NotificationBar({
  as: _Component = _Builtin.Block,
  title = "Idag är det julafton",
  text = "– och farmor vill ha klappar.",
  aktiv = true,
  secondaryBackground = false,
  content = " och farmor behöver sina klappar.",
}) {
  return aktiv ? (
    <_Component
      className={_utils.cx(_styles, "notification-bar-wrapper")}
      tag="div"
    >
      <_Builtin.BlockContainer
        className={_utils.cx(_styles, "container", "center")}
        grid={{
          type: "container",
        }}
        tag="div"
      >
        <_Builtin.RichText
          className={_utils.cx(_styles, "notification-bar")}
          tag="div"
        >
          {content}
        </_Builtin.RichText>
      </_Builtin.BlockContainer>
      {secondaryBackground ? (
        <_Builtin.Block
          className={_utils.cx(
            _styles,
            "notification-bar-secondary-background"
          )}
          tag="div"
        />
      ) : null}
    </_Component>
  ) : null;
}
