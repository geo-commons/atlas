<script setup lang="ts">
import AdminListViewHeader from "@/admin/components/AdminListViewHeader.vue";
import AdminListViewDialog from "@/admin/components/AdminListViewDialog.vue";
import { computed, onMounted, Ref, ref } from "vue";
import AdminListViewTable, { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import AdminListViewFilter, { TableFilter } from "@/admin/components/AdminListViewFilter.vue";
import { useRoute, useRouter } from "@/utils/inertia-routing";
import { TableHeaderRef } from "@/admin/components/AdminListViewTableHeader.vue";
import AdminListViewPaginator, { PaginationRef } from "@/admin/components/AdminListViewPaginator.vue";
import { PageState } from "primevue/paginator";
import SpinnerComponent from "@/components/Spinner.vue";
import { EDialogTypes, ShowDialogType } from "@/types/dialog";
import { useToast } from "primevue";
import { useMutation, useQuery, useQueryCache } from "@pinia/colada";
import { apiFetch, ApiMethod } from "@/utils/api-helpers";

// Properties
type AdminListViewProps = {
  enableImportExport?: boolean;
  enableCreateObject?: boolean;
  enableDuplicate?: boolean;
  enableDeleteMultiple?: boolean;
  enableDelete?: boolean;
  enableEdit?: boolean;
  singularName: string;
  pluralName: string;
  apiName: string;
  loading: boolean;
  tableHeaders: Array<TableHeader>;
  getTableFilters?: () => Array<TableFilter>;
  viewBaseUrl?: string;
  fixedQueryParams?: Record<string, string>;
  blockDelete?: Array<number>;
  // These 3 props are only necessary if enableCreateObject is true
  getCreateObjectDialogSections?: () => object;
  initialCreateObjectDialogData?: object;
  saveCreateObjectDialogData?: (
    currentValues: object,
    continueEditing: boolean,
    sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
  ) => void;
};

const props = withDefaults(defineProps<AdminListViewProps>(), {
  enableImportExport: false,
  enableCreateObject: true,
  enableDuplicate: false,
  enableDeleteMultiple: false,
  enableDelete: true,
  enableEdit: true,
  fixedQueryParams: () => ({}),
  blockDelete: () => [],
});

const router = useRouter();
const route = useRoute();
const queryCache = useQueryCache();
const toast = useToast();

const getQueryParams = (query: URLSearchParams | Record<string, any>) => {
  const searchParams = new URLSearchParams(query instanceof URLSearchParams ? query : query);

  Object.entries(props.fixedQueryParams).forEach(([key, value]) => {
    searchParams.set(key, value);
  });

  return searchParams;
};

// Query logic
const { state } = useQuery({
  key: () => [props.apiName, route.query, props.fixedQueryParams],
  query: async () => {
    const url = new URL(`/atlas/api/v1/${props.apiName}/`, window.location.origin);
    const searchParams = getQueryParams(route.query as Record<string, any>);
    url.search = searchParams.toString();
    const res = await apiFetch(url);
    return await res.json();
  },
  staleTime: 1000 * 60,
  placeholderData: (previousData) => previousData,
});

// Dialog logic
const showDialog: Ref<ShowDialogType> = ref({
  show: false,
  type: EDialogTypes.Create,
});

const toggleDialog = (type: EDialogTypes) => {
  showDialog.value = {
    type: type,
    show: !showDialog.value.show,
  };
};

// Action logic
const enableActions = computed(() => {
  return props.enableDuplicate || props.enableImportExport || props.enableDeleteMultiple;
});

// Duplicate logic
const duplicateMutation = useMutation({
  mutation: async (ids: number[]) => {
    await apiFetch(`/atlas/api/v1/${props.apiName}/duplicate/`, ApiMethod.POST, { ids });
  },
  onSuccess: async () => {
    await queryCache.invalidateQueries({ key: [props.apiName] });
    toast.add({
      severity: "success",
      summary: `Dupliceren gelukt`,
      detail: `Het dupliceren van ${props.pluralName.toLowerCase()} is gelukt`,
      life: 5000,
    });
  },
});

const duplicateSelectedItems = async () => {
  if (selectedItems.value.length) {
    const ids = selectedItems.value.map((selectedItem) => selectedItem.id);
    duplicateMutation.mutate(ids);
  }
};

// Delete logic
const deleteMutation = useMutation({
  mutation: async (ids: number[]) => {
    await apiFetch(`/atlas/api/v1/${props.apiName}/delete/`, ApiMethod.POST, { ids });
  },
  onSuccess: async () => {
    await queryCache.invalidateQueries({ key: [props.apiName] });
    adminListViewTableRef?.value?.resetSelection();
    toast.add({
      severity: "success",
      summary: `Verwijderen gelukt`,
      detail: `Het verwijderen van ${props.pluralName.toLowerCase()} is gelukt`,
      life: 5000,
    });
    toggleDialog(showDialog.value.type);
  },
});

const deleteRowMutation = useMutation({
  mutation: async (id: number) => {
    await apiFetch(`/atlas/api/v1/${props.apiName}/${id}/`, ApiMethod.DELETE);
  },
  onSuccess: async () => {
    await queryCache.invalidateQueries({ key: [props.apiName] });
    adminListViewTableRef?.value?.resetSelection();
    toast.add({
      severity: "success",
      summary: `Verwijderen gelukt`,
      detail: `Het verwijderen van ${props.singularName.toLowerCase()} is gelukt`,
      life: 5000,
    });
  },
});

const deleteSelectedItems = async () => {
  if (selectedItems.value.length) {
    const ids = selectedItems.value.map((selectedItem) => selectedItem.id);
    deleteMutation.mutate(ids);
  }
};

const deleteRow = async (row: any) => {
  const acknowledged = confirm(`Weet je zeker dat je de ${props.singularName.toLowerCase()} wilt verwijderen?`);
  if (acknowledged) {
    deleteRowMutation.mutate(row.id);
  }
};

// Table logic
let params: URLSearchParams = new URLSearchParams();
const sort: Ref<TableHeaderRef> = ref({ sortKey: "", sortAscending: true });
const pagination: Ref<PaginationRef> = ref({ page: 0, rows: 20 });
const selectedItems: Ref<Array<{ id: number; title: string }>> = ref([]);

const updateRouter = async (params: URLSearchParams) => {
  // Reset selection to avoid having selected invisible items
  adminListViewTableRef?.value?.resetSelection();
  await router.replace({
    path: route.path,
    query: {
      ...Object.fromEntries(params),
    },
  });
  // List is automatically updated
};

const updateSearchTerm = async (value: string) => {
  if (value) {
    params.set("search", value);
  } else {
    params.delete("search");
  }

  params.set("page", "1");
  params.set("page_size", pagination.value.rows.toString());

  await updateRouter(params);
};

const updateListFilters = async (value: any, key: string) => {
  if (value && value?.length) {
    params.set(key, value.map((val: any) => (val.id ? val.id : val)).join(","));
  } else {
    params.delete(key);
  }

  params.set("page", "1");
  params.set("page_size", pagination.value.rows.toString());

  await updateRouter(params);
};

const updateListSort = async (key: string) => {
  if (sort.value.sortKey === key) {
    sort.value = {
      sortKey: key,
      sortAscending: !sort.value.sortAscending,
    };
  } else {
    sort.value = {
      sortKey: key,
      sortAscending: true,
    };
  }

  params.set("ordering", `${sort.value.sortAscending ? "" : "-"}${sort.value.sortKey}`);

  await updateRouter(params);
};

const updateListPagination = async (pageState: PageState) => {
  pagination.value = {
    page: pageState.page,
    rows: pageState.rows,
  };

  params.set("page", (pagination.value.page + 1).toString());
  params.set("page_size", pagination.value.rows.toString());

  await updateRouter(params);
};

const updateSelectedItems = (updatedSelectedItems: Array<{ id: number; title: string }>) => {
  selectedItems.value = updatedSelectedItems;
};

// Lifecycle hooks
onMounted(async () => {
  params = new URLSearchParams(route.query as any);

  // Page
  const page = params.get("page");
  const pageSize = params.get("page_size");

  pagination.value = {
    page: page ? parseInt(page) - 1 : 0,
    rows: pageSize ? parseInt(pageSize) : 20,
  };

  if (!page) {
    params.set("page", pagination.value.page === 0 ? "1" : pagination.value.page.toString());
  }

  if (!pageSize) {
    params.set("page_size", pagination.value.rows.toString());
  }

  await router.replace({
    path: route.path,
    query: {
      ...Object.fromEntries(params),
    },
  });

  // Order params
  const order = params.get("ordering");
  sort.value = {
    sortKey: order ? order.replace("-", "") : "",
    sortAscending: order ? !order.startsWith("-") : true,
  };
});

const handleSaveCreateObjectDialogData = async (
  currentValues: object,
  continueEditing: boolean,
  sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
) => {
  if (!props.saveCreateObjectDialogData) {
    return;
  }

  await props.saveCreateObjectDialogData(currentValues, continueEditing, sendSaveRequest);

  await queryCache.invalidateQueries({ key: [props.apiName] });
};

const adminListViewTableRef: Ref<null | {
  resetSelection: () => void;
}> = ref(null);

const refreshAndResetItems = async () => {
  await queryCache.invalidateQueries({ key: [props.apiName] });
  adminListViewTableRef?.value?.resetSelection();
};

// Define expose, expose functions / elements to parent element
defineExpose({ toggleDialog });
</script>

<template>
  <div class="container __admin">
    <AdminListViewHeader
      :name="props.pluralName"
      :singular-name="props.singularName"
      :enable-create-object="props.enableCreateObject"
      :enable-duplicate="props.enableDuplicate"
      :enable-import-export="props.enableImportExport"
      :enable-delete-multiple="props.enableDeleteMultiple"
      :enable-actions="enableActions"
      :api-name="props.apiName"
      :has-selected-items="selectedItems.length > 0"
      @update-dialog="toggleDialog"
      @duplicate="duplicateSelectedItems"
      @delete="deleteSelectedItems"
    />
    <div v-if="state.status === 'pending'">
      <SpinnerComponent />
    </div>
    <div v-else-if="state.data">
      <AdminListViewFilter
        :params="params"
        :get-table-filters="props.getTableFilters"
        :singular-name="props.singularName"
        @update-search-term="updateSearchTerm"
        @update-list-filters="updateListFilters"
      />
      <AdminListViewTable
        ref="adminListViewTableRef"
        :items="state.data.results"
        :api-name="props.apiName"
        :pagination="pagination"
        :table-headers="props.tableHeaders"
        :sort="sort"
        :enable-actions="enableActions"
        :view-base-url="props.viewBaseUrl"
        :block-delete="props.blockDelete"
        :enable-delete="props.enableDelete"
        :enable-edit="props.enableEdit"
        @update-list-sort="updateListSort"
        @update-selected-items="updateSelectedItems"
        @delete-row="deleteRow"
      />
      <AdminListViewPaginator
        :total-results="state.data.count"
        :pagination="pagination"
        @update-list-pagination="updateListPagination"
      />
      <AdminListViewDialog
        ref="adminListViewDialogRef"
        :show-dialog="showDialog"
        :singular-name="props.singularName"
        :plural-name="props.pluralName"
        :get-create-object-dialog-sections="props.getCreateObjectDialogSections"
        :save-create-object-dialog-data="handleSaveCreateObjectDialogData"
        :initial-create-object-dialog-data="props.initialCreateObjectDialogData"
        :api-name="props.apiName"
        :selected-items="selectedItems"
        @update-dialog="toggleDialog"
        @reset-selection="refreshAndResetItems"
        @delete="deleteSelectedItems"
      />
    </div>
  </div>
</template>
