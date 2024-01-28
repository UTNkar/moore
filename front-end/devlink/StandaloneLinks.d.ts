import * as React from "react";
import * as Types from "./types";

declare function StandaloneLinks(props: {
  as?: React.ElementType;
  phone?: Types.Basic.Link;
  email?: Types.Basic.Link;
  emailLabel?: React.ReactNode;
  url?: Types.Basic.Link;
  urlLabel?: React.ReactNode;
  phoneVisible?: Types.Visibility.VisibilityConditions;
  emailVisible?: Types.Visibility.VisibilityConditions;
  urlVisible?: Types.Visibility.VisibilityConditions;
  phoneLabel?: React.ReactNode;
}): React.JSX.Element;
