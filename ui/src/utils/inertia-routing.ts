import { Link, router, usePage } from "@inertiajs/vue3";
import { computed, defineComponent, h, reactive } from "vue";

interface IRouteTarget {
  name?: string;
  path?: string;
  params?: Record<string, string | number | boolean | null | undefined>;
  query?: Record<string, string | number | boolean | null | undefined>;
}

const namedRoutes: Record<string, (params: IRouteTarget["params"]) => string> = {
  "metadataset-details": (params) => `/metadatasets/${params?.slug}`,
  "table-details": (params) => `/tables/${params?.slug}`,
};

const routeQueryToString = (query: Record<string, unknown> = {}): string => {
  const params = new URLSearchParams();

  Object.entries(query).forEach(([key, value]) => {
    if (value === null || value === undefined || value === "") {
      return;
    }

    params.set(key, String(value));
  });

  const queryString = params.toString();
  return queryString ? `?${queryString}` : "";
};

const normalizePath = (path: string, basePath: string): string => {
  if (/^(https?:)?\/\//.test(path) || path.startsWith("#")) {
    return path;
  }

  if (path.startsWith("/atlas/") || path.startsWith("/tables-old/")) {
    return path;
  }

  if (!basePath) {
    return path;
  }

  if (path === "/") {
    return `${basePath}/`;
  }

  return `${basePath}${path}`;
};

export const useRoute = () => {
  const page = usePage();

  return reactive({
    get app() {
      return (page.props.route as any)?.app;
    },
    get basePath() {
      return (page.props.route as any)?.basePath;
    },
    get path() {
      return (page.props.route as any)?.path ?? "/";
    },
    get fullPath() {
      return (page.props.route as any)?.fullPath ?? "/";
    },
    get query() {
      return (page.props.route as any)?.query ?? {};
    },
    get params() {
      return (page.props.route as any)?.params ?? {};
    },
    get meta() {
      return (page.props.route as any)?.meta ?? {};
    },
  }) as any;
};

export const resolveInertiaTarget = (target: string | IRouteTarget): string => {
  const page = usePage();
  const route = page.props.route as any;
  const basePath = route?.basePath ?? "";

  if (typeof target === "string") {
    return normalizePath(target, basePath);
  }

  const path =
    target.name && namedRoutes[target.name]
      ? namedRoutes[target.name](target.params)
      : (target.path ?? route?.path ?? "/");
  return `${normalizePath(path, basePath)}${routeQueryToString(target.query)}`;
};

export const useRouter = () => {
  return {
    push(target: string | IRouteTarget) {
      router.visit(resolveInertiaTarget(target));
    },
    replace(target: string | IRouteTarget) {
      router.visit(resolveInertiaTarget(target), { replace: true, preserveState: true, preserveScroll: true });
    },
    visit(target: string | IRouteTarget) {
      router.visit(resolveInertiaTarget(target));
    },
  };
};

export const RouterLink = defineComponent({
  name: "RouterLink",
  props: {
    to: {
      type: [String, Object],
      required: true,
    },
  },
  setup(props, { attrs, slots }) {
    const href = computed(() => resolveInertiaTarget(props.to as string | IRouteTarget));

    return () =>
      h(
        Link,
        {
          ...attrs,
          href: href.value,
        },
        slots,
      );
  },
});
