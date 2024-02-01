import React from "react";
import * as _Builtin from "./_Builtin";
import { ContentHeaderText } from "./ContentHeaderText";
import * as _utils from "./utils";
import _styles from "./HomeIntroductionPageBlock.module.css";

export function HomeIntroductionPageBlock({
  as: _Component = _Builtin.Section,
  title = "Uppsala teknolog- och naturvetarkår",
  subhead = "Studentkåren för dig som är teknolog eller naturvetare i Uppsala",
}) {
  return (
    <_Component
      className={_utils.cx(_styles, "section")}
      grid={{
        type: "section",
      }}
      tag="section"
    >
      <_Builtin.VFlex className={_utils.cx(_styles, "container")} tag="div">
        <ContentHeaderText title={title} subhead={subhead} />
        <_Builtin.VFlex
          className={_utils.cx(_styles, "large-button-group-wrapper")}
          tag="div"
        >
          <_Builtin.Link
            className={_utils.cx(_styles, "large-button")}
            button={true}
            options={{
              href: "/engagera-dig",
            }}
          >
            {"Bli medlem"}
          </_Builtin.Link>
          <_Builtin.VFlex
            className={_utils.cx(_styles, "button-group-wrapper")}
            tag="div"
          >
            <_Builtin.Link
              className={_utils.cx(
                _styles,
                "large-button",
                "secondary",
                "left"
              )}
              button={true}
              options={{
                href: "/engagera-dig",
              }}
            >
              {"Engagera dig"}
            </_Builtin.Link>
            <_Builtin.Link
              className={_utils.cx(
                _styles,
                "large-button",
                "right",
                "secondary"
              )}
              button={true}
              options={{
                href: "/engagera-dig",
              }}
            >
              {"Påverka studierna"}
            </_Builtin.Link>
          </_Builtin.VFlex>
        </_Builtin.VFlex>
      </_Builtin.VFlex>
    </_Component>
  );
}
