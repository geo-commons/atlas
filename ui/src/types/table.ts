/**
 * Table as returned by the portal tables API.
 * Used for portal cards and overview pages.
 */
export interface IPortalTable {
  id: number;
  title: string;
  description: string | null;
  slug: string;
  login_required: boolean;
  only_internal: boolean;
}
