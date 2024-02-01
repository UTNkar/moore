import * as React from "react";
import * as Types from "./types";

declare function SectionCard(props: {
  as?: React.ElementType;
  acronym?: React.ReactNode;
  programs?: React.ReactNode;
  link?: Types.Basic.Link;
  linkLabel?: React.ReactNode;
}): React.JSX.Element;
