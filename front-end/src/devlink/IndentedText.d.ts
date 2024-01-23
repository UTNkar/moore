import * as React from "react";
import * as Types from "./types";

declare function IndentedText(props: {
  as?: React.ElementType;
  heading?: React.ReactNode;
  text?: Types.Basic.RichTextChildren;
}): React.JSX.Element;
