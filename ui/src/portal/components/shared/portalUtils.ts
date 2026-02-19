/**
 * Returns whether the given link is active for the current path.
 * @param path - Current route path (e.g. from useRoute().path)
 * @param link - Link object with href
 * @returns true if the link is active for the current path
 */
export const isPortalLinkActive = (path: string | undefined, link: { href?: string } | null | undefined): boolean => {
  if (!link?.href) return false;
  const p = path ?? (typeof window !== "undefined" ? window.location.pathname : "");
  const href = link.href.replace(/\/$/, "") || "/";
  return p === href || p === link.href || (href !== "/" && p.startsWith(href + "/"));
};
