import React from "react";
import * as _Builtin from "./_Builtin";
import { PubOpeningHours } from "./PubOpeningHours";
import { CafeOpeningHours } from "./CafeOpeningHours";
import * as _utils from "./utils";
import _styles from "./Footer.module.css";

export function Footer({ as: _Component = _Builtin.Section }) {
  return (
    <_Component
      className={_utils.cx(_styles, "footer")}
      grid={{
        type: "section",
      }}
      tag="section"
    >
      <_Builtin.VFlex className={_utils.cx(_styles, "container")} tag="div">
        <_Builtin.VFlex
          className={_utils.cx(_styles, "footer-wrapper")}
          tag="div"
        >
          <_Builtin.VFlex
            className={_utils.cx(_styles, "footer-logo-wrapper")}
            tag="div"
          >
            <_Builtin.Link
              button={false}
              options={{
                href: "/",
              }}
            >
              <_Builtin.Image
                className={_utils.cx(_styles, "footer-logo")}
                loading="lazy"
                width="auto"
                height="auto"
                alt="Uppsala teknolog- och naturverarkår"
                src="https://uploads-ssl.webflow.com/655e29844518537470ba5b0f/655e33434a15645ce5ef1708_logo-square-blue.svg"
              />
            </_Builtin.Link>
            <_Builtin.MapWidget
              className={_utils.cx(_styles, "map")}
              zoom={12}
              mapStyle="roadmap"
              enableScroll={true}
              enableTouch={true}
              apiKey={process.env.DEVLINK_ENV_GOOGLE_MAPS_API_KEY}
            />
          </_Builtin.VFlex>
          <_Builtin.VFlex
            className={_utils.cx(_styles, "footer-info-wrapper")}
            tag="div"
          >
            <_Builtin.VFlex
              className={_utils.cx(_styles, "footer-column")}
              editable={false}
              tag="div"
            >
              <_Builtin.Heading
                className={_utils.cx(
                  _styles,
                  "footer-heading",
                  "without-spacing"
                )}
                tag="h3"
              >
                {"Följ oss"}
              </_Builtin.Heading>
              <_Builtin.Heading
                className={_utils.cx(
                  _styles,
                  "footer-subheading",
                  "without-decoration"
                )}
                tag="h4"
              >
                {"Sociala medier"}
              </_Builtin.Heading>
              <_Builtin.Paragraph
                className={_utils.cx(_styles, "standalone-link")}
              >
                <_Builtin.Link
                  button={false}
                  options={{
                    href: "#",
                  }}
                >
                  {"Facebook"}
                </_Builtin.Link>
                <br />
                <_Builtin.Link
                  button={false}
                  options={{
                    href: "#",
                  }}
                >
                  {"Instagram"}
                </_Builtin.Link>
                <br />
                <_Builtin.Link
                  button={false}
                  options={{
                    href: "#",
                  }}
                >
                  {"LinkedIn"}
                </_Builtin.Link>
              </_Builtin.Paragraph>
            </_Builtin.VFlex>
            <_Builtin.VFlex
              className={_utils.cx(_styles, "footer-column")}
              editable={false}
              tag="div"
            >
              <_Builtin.Heading
                className={_utils.cx(
                  _styles,
                  "footer-heading",
                  "without-spacing"
                )}
                tag="h3"
              >
                {"Kontaktuppgifter"}
              </_Builtin.Heading>
              <_Builtin.Heading
                className={_utils.cx(
                  _styles,
                  "footer-subheading",
                  "without-decoration"
                )}
                tag="h4"
              >
                {"Telefonnummer"}
              </_Builtin.Heading>
              <_Builtin.Paragraph
                className={_utils.cx(_styles, "standalone-link")}
              >
                <_Builtin.Link
                  button={false}
                  options={{
                    href: "#",
                  }}
                >
                  {"018 123 456 789"}
                </_Builtin.Link>
              </_Builtin.Paragraph>
              <_Builtin.Heading
                className={_utils.cx(
                  _styles,
                  "footer-subheading",
                  "without-decoration"
                )}
                tag="h4"
              >
                {"E-post"}
              </_Builtin.Heading>
              <_Builtin.Paragraph
                className={_utils.cx(_styles, "standalone-link")}
              >
                <_Builtin.Link
                  button={false}
                  options={{
                    href: "#",
                  }}
                >
                  {"info@utn.se"}
                </_Builtin.Link>
              </_Builtin.Paragraph>
              <_Builtin.Heading
                className={_utils.cx(
                  _styles,
                  "footer-subheading",
                  "without-decoration"
                )}
                tag="h4"
              >
                {"Adress"}
              </_Builtin.Heading>
              <_Builtin.Paragraph
                className={_utils.cx(_styles, "footer-paragraph")}
              >
                {"Polacksbacken"}
                <br />
                {"Hus 73"}
                <br />
                {"752 37 Uppsala"}
              </_Builtin.Paragraph>
            </_Builtin.VFlex>
            <_Builtin.VFlex
              className={_utils.cx(_styles, "footer-column")}
              tag="div"
            >
              <_Builtin.Heading
                className={_utils.cx(
                  _styles,
                  "footer-heading",
                  "without-spacing"
                )}
                editable={false}
                tag="h3"
              >
                {"Öppettider"}
              </_Builtin.Heading>
              <_Builtin.Heading
                className={_utils.cx(
                  _styles,
                  "footer-subheading",
                  "without-decoration"
                )}
                editable={false}
                tag="h4"
              >
                {"Expeditionen"}
              </_Builtin.Heading>
              <_Builtin.Paragraph
                className={_utils.cx(_styles, "footer-paragraph")}
              >
                {"Vardagar 9:00–15:15"}
              </_Builtin.Paragraph>
              <_Builtin.Heading
                className={_utils.cx(
                  _styles,
                  "footer-subheading",
                  "without-decoration"
                )}
                editable={false}
                tag="h4"
              >
                {"Pub på Uthgård"}
              </_Builtin.Heading>
              <PubOpeningHours />
              <_Builtin.Heading
                className={_utils.cx(
                  _styles,
                  "footer-subheading",
                  "without-decoration"
                )}
                editable={false}
                tag="h4"
              >
                {"Café Bocken"}
              </_Builtin.Heading>
              <CafeOpeningHours />
            </_Builtin.VFlex>
          </_Builtin.VFlex>
        </_Builtin.VFlex>
      </_Builtin.VFlex>
    </_Component>
  );
}
