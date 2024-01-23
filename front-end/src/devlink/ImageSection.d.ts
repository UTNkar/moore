import * as React from "react";
import * as Types from "./types";

declare function ImageSection(props: {
  as?: React.ElementType;
  description?: React.ReactNode;
  image?: Types.Asset.Image;
}): React.JSX.Element;
