import * as React from "react";
import * as Types from "./types";

declare function TextNotice(props: {
  as?: React.ElementType;
  content?: Types.Basic.RichTextChildren;
  heading?: React.ReactNode;
}): React.JSX.Element;
