/**
 * Shared link definitions for portal quick navigation (header and "Direct naar" menu).
 * Each item: { href, icon, label, showKey, external, showInQuickMenu }
 * - showKey: key in availableLinks to show this link (null = always show)
 * - external: open in new tab with noopener
 * - showInQuickMenu: show in "Direct naar" menu (default true)
 */
export interface PortalQuickNavLink {
  href: string;
  icon: string;
  label: string;
  showKey: "maps" | "metadatasets" | "tables" | null;
  external?: boolean;
  showInQuickMenu?: boolean;
}

export const PORTAL_QUICK_NAV_LINKS: PortalQuickNavLink[] = [
  {
    href: "/",
    icon: "pi-home",
    label: "Home",
    showKey: null,
    external: false,
    showInQuickMenu: false,
  },
  {
    href: "/maps",
    icon: "pi-map",
    label: "Kaarten",
    showKey: "maps",
    external: false,
  },
  {
    href: "/metadatasets",
    icon: "pi-database",
    label: "Metadatasets",
    showKey: "metadatasets",
    external: false,
  },
  {
    href: "/tables",
    icon: "pi-table",
    label: "Tabellen",
    showKey: "tables",
    external: false,
  },
  {
    href: "/atlas/",
    icon: "pi-external-link",
    label: "Hoofdkaart",
    showKey: null,
    external: true,
  },
];
