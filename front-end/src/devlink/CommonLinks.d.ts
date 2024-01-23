import * as React from "react";
import * as Types from "./types";

declare function CommonLinks(props: {
  as?: React.ElementType;
  urlLabel?: React.ReactNode;
  url?: Types.Basic.Link;
  phoneLabel?: React.ReactNode;
  phone?: Types.Basic.Link;
  eMail?: Types.Basic.Link;
  eMailLabel?: React.ReactNode;
}): React.JSX.Element;
