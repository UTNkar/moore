import React from "react";
import * as _Builtin from "./_Builtin";
import * as _utils from "./utils";
import _styles from "./SpecialNotice.module.css";

export function SpecialNotice({
  as: _Component = _Builtin.Link,
  heading = "Heading",
  text = "Vi har nu utsett vinnaren. Klicka här för att se mer",
}) {
  return (
    <_Component
      className={_utils.cx(_styles, "special-notice")}
      button={false}
      options={{
        href: "#",
      }}
    >
      <_Builtin.Heading
        className={_utils.cx(_styles, "without-decoration")}
        tag="h3"
      >
        {heading}
      </_Builtin.Heading>
      <_Builtin.Paragraph>{text}</_Builtin.Paragraph>
    </_Component>
  );
}
