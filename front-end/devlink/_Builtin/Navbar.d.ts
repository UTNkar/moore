import * as React from "react";
import { EASING_FUNCTIONS } from "../utils";
import { LinkProps, TagProps } from "./Basic";
declare const BREAKPOINTS: {
  medium: number;
  small: number;
  tiny: number;
};
type NavbarConfig = {
  animation: string;
  collapse: keyof typeof BREAKPOINTS;
  docHeight: boolean;
  duration: number;
  easing: keyof typeof EASING_FUNCTIONS;
  easing2: keyof typeof EASING_FUNCTIONS;
  noScroll: boolean;
};
export declare const NavbarContext: React.Context<
  NavbarConfig & {
    animDirect: -1 | 1;
    animOver: boolean;
    getBodyHeight: () => number | void;
    getOverlayHeight: () => number | undefined;
    isOpen: boolean;
    menu: React.MutableRefObject<HTMLElement | null>;
    root: React.MutableRefObject<HTMLElement | null>;
    toggleOpen: () => void;
    navbarMounted: boolean;
    setFocusedLink: React.Dispatch<React.SetStateAction<number>>;
  }
>;
type NavbarChildrenType =
  | NavbarContainerProps
  | NavbarBrandProps
  | NavbarMenuProps
  | NavbarButtonProps;
type NavbarProps = {
  tag: React.ElementType;
  config: NavbarConfig;
  className?: string;
  children?:
    | React.ReactElement<NavbarChildrenType>[]
    | React.ReactElement<NavbarChildrenType>;
};
export declare function NavbarWrapper(props: NavbarProps): React.JSX.Element;
type NavbarContainerProps = TagProps & {
  toggleOpen: () => void;
  isOpen: boolean;
  children: React.ReactNode;
};
export declare function NavbarContainer({
  children,
  ...props
}: NavbarContainerProps): React.JSX.Element;
type NavbarBrandProps = LinkProps;
export declare function NavbarBrand({
  className,
  ...props
}: NavbarBrandProps): React.JSX.Element;
type NavbarMenuProps = React.PropsWithChildren<{
  tag?: React.ElementType;
  className?: string;
  isOpen?: boolean;
}>;
export declare function NavbarMenu({
  tag,
  className,
  ...props
}: NavbarMenuProps): React.ReactElement<
  any,
  string | React.JSXElementConstructor<any>
>;
type NavbarLinkProps = LinkProps;
export declare function NavbarLink({
  className,
  ...props
}: NavbarLinkProps): React.JSX.Element;
type NavbarButtonProps = React.PropsWithChildren<{
  tag?: React.ElementType;
  className?: string;
}>;
export declare function NavbarButton({
  tag,
  className,
  ...props
}: NavbarButtonProps): React.ReactElement<
  any,
  string | React.JSXElementConstructor<any>
>;
export {};
