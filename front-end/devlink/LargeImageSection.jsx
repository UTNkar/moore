import React from "react";
import * as _Builtin from "./_Builtin";
import { RichText } from "./RichText";
import * as _utils from "./utils";
import _styles from "./LargeImageSection.module.css";

export function LargeImageSection({
  as: _Component = _Builtin.Section,
  description = "",
  image = "https://uploads-ssl.webflow.com/655e29844518537470ba5b0f/6564c083dd14dd5492bfc4d2_uthga%CC%8Ard-full.jpg",
}) {
  return (
    <_Component
      className={_utils.cx(_styles, "section")}
      grid={{
        type: "section",
      }}
      tag="section"
    >
      <_Builtin.Block
        className={_utils.cx(_styles, "container", "full-width")}
        tag="div"
      >
        <_Builtin.VFlex
          className={_utils.cx(_styles, "large-image-wrapper")}
          tag="div"
        >
          <_Builtin.Image
            className={_utils.cx(_styles, "large-image")}
            loading="eager"
            height="auto"
            width="auto"
            aria-describedby="image-desc"
            alt=""
            src={image}
          />
        </_Builtin.VFlex>
      </_Builtin.Block>
      <_Builtin.Block className={_utils.cx(_styles, "container")} tag="div">
        <_Builtin.VFlex
          className={_utils.cx(_styles, "image-description")}
          tag="div"
        >
          <RichText content={description} />
        </_Builtin.VFlex>
      </_Builtin.Block>
    </_Component>
  );
}
