import * as React from "react";
import * as Types from "./types";

declare function FaqItem(props: {
  as?: React.ElementType;
  question?: React.ReactNode;
  answer?: Types.Basic.RichTextChildren;
}): React.JSX.Element;
