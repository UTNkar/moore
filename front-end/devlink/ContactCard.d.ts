import * as React from "react";
import * as Types from "./types";

declare function ContactCard(props: {
  as?: React.ElementType;
  photo?: Types.Asset.Image;
  name?: React.ReactNode;
  role?: React.ReactNode;
  mailLink?: Types.Basic.Link;
  mailLabel?: React.ReactNode;
  phoneLink?: Types.Basic.Link;
  phoneLabel?: React.ReactNode;
}): React.JSX.Element;
