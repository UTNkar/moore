import * as React from "react";
import * as Types from "./types";

declare function LargeImageSection(props: {
  as?: React.ElementType;
  description?: Types.Basic.RichTextChildren;
  image?: Types.Asset.Image;
}): React.JSX.Element;
