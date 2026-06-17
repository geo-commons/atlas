import { useRoute, useRouter } from "@/utils/inertia-routing";
import { LayoutMode } from "@/portal/components/shared/portalCardShared";

export interface PortalQueryParams {
  query: string;
  page: number;
  page_size: number;
  sort: string;
  view: LayoutMode;
  topic: string;
}

const DEFAULT_PAGE = 1;
const DEFAULT_PAGE_SIZE = 12;
const DEFAULT_SORT = "title";
const DEFAULT_VIEW = LayoutMode.Grid;

/**
 * Composable for syncing portal filters, sorting, pagination and view mode
 * to URL query params. Enables shareable URLs and browser back/forward.
 */
export const usePortalQueryParams = () => {
  const route = useRoute();
  const router = useRouter();

  const parseFromUrl = (): PortalQueryParams => {
    const q = route.query;
    const page = parseInt(String(q.page || DEFAULT_PAGE), 10);
    const pageSize = parseInt(String(q.page_size || DEFAULT_PAGE_SIZE), 10);
    return {
      query: (q.query as string) || "",
      page: Number.isNaN(page) || page < 1 ? DEFAULT_PAGE : page,
      page_size: Number.isNaN(pageSize) || pageSize < 1 ? DEFAULT_PAGE_SIZE : pageSize,
      sort: (q.sort as string) || DEFAULT_SORT,
      view: (q.view as LayoutMode) || DEFAULT_VIEW,
      topic: (q.topic as string) || "",
    };
  };

  const syncToUrl = (params: Partial<PortalQueryParams>) => {
    const current = { ...parseFromUrl(), ...params };
    const query: Record<string, string> = {};
    if (current.query) query.query = current.query;
    if (current.page && current.page > 1) query.page = String(current.page);
    if (current.page_size && current.page_size !== DEFAULT_PAGE_SIZE) query.page_size = String(current.page_size);
    if (current.sort && current.sort !== DEFAULT_SORT) query.sort = current.sort;
    if (current.view && current.view !== DEFAULT_VIEW) query.view = current.view;
    if (current.topic) query.topic = current.topic;

    router.replace({ query });
  };

  return { parseFromUrl, syncToUrl };
};
