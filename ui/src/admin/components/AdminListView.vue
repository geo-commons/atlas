<script setup lang="ts">
import AdminListViewHeader from "@/admin/components/AdminListViewHeader.vue";
import AdminListViewDialog from "@/admin/components/AdminListViewDialog.vue";
import { onMounted, Ref, ref } from "vue";
import AdminListViewTable, { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import AdminListViewFilter, { TableFilter } from "@/admin/components/AdminListViewFilter.vue";
import { useRoute, useRouter } from "vue-router";
import { TableHeaderRef } from "@/admin/components/AdminListViewTableHeader.vue";
import AdminListViewPaginator, { PaginationRef } from "@/admin/components/AdminListViewPaginator.vue";
import { PageState } from "primevue/paginator";
import Cookies from "js-cookie";
import SpinnerComponent from "@/components/Spinner.vue";
import { EDialogTypes, ShowDialogType } from "@/types/dialog";

// Properties
type AdminListViewProps = {
  enableImportExport?: boolean;
  enableCreateObject?: boolean;
  enableSort?: boolean;
  singularName: string;
  pluralName: string;
  apiName: string;
  loading: boolean;
  getObjects: (searchParams?: URLSearchParams) => Promise<{ results: Array<object>; count: number }>;
  tableHeaders: Array<TableHeader>;
  getTableFilters?: () => Array<TableFilter>;
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
  enableImportExport: true,
  enableCreateObject: true,
  enableSort: false,
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

  if (type === EDialogTypes.Export && showDialog.value.show && selectedItems.value.size < 1) {
    enableSelectable.value = true;
  }
};

// Table logic
let params: URLSearchParams = new URLSearchParams();
const items: Ref<{ results: Array<object>; count: number }> = ref({
  results: [],
  count: 0,
});
const sort: Ref<TableHeaderRef> = ref({ sortKey: "", sortAscending: true });
const pagination: Ref<PaginationRef> = ref({ page: 0, rows: 20 });
const selectedItems: Ref<Set<{ id: number; title: string }>> = ref(new Set([]));
const isAllSelected: Ref<boolean> = ref(false);
const router = useRouter();
const route = useRoute();

const updateSearchTerm = async (value: string) => {
  if (value) {
    params.set("search", value);
  } else {
    params.delete("search");
  }

  params.set("page", "1");
  params.set("page_size", pagination.value.rows.toString());

  await router.replace({
    path: route.path,
    query: {
      ...Object.fromEntries(params),
    },
  });

  const result = await props.getObjects(params);

  items.value = {
    results: result.results,
    count: result.count,
  };
};

const updateListFilters = async (value: any, key: string) => {
  if (value && value?.length) {
    params.set(key, value.map((val: any) => (val.id ? val.id : val)).join(","));
  } else {
    params.delete(key);
  }

  params.set("page", "1");
  params.set("page_size", pagination.value.rows.toString());

  await router.replace({
    path: route.path,
    query: {
      ...Object.fromEntries(params),
    },
  });

  const result = await props.getObjects(params);

  items.value = {
    results: result.results,
    count: result.count,
  };
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

  await router.replace({
    path: route.path,
    query: {
      ...Object.fromEntries(params),
    },
  });

  const result = await props.getObjects(params);

  items.value = {
    results: result.results,
    count: result.count,
  };
};

const updateListPagination = async (pageState: PageState) => {
  pagination.value = {
    page: pageState.page,
    rows: pageState.rows,
  };

  params.set("page", (pagination.value.page + 1).toString());
  params.set("page_size", pagination.value.rows.toString());

  await router.replace({
    path: route.path,
    query: {
      ...Object.fromEntries(params),
    },
  });

  items.value = await props.getObjects(params);
};

const deleteRow = async (row: any) => {
  const acknowledged = confirm(`Weet je zeker dat je de ${props.singularName} wilt verwijderen?`);
  if (!acknowledged) {
    return;
  }

  const result = await fetch(`/atlas/api/v1/${props.apiName}/${row.id}/`, {
    method: "DELETE",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": Cookies.get("csrftoken"),
    },
  });

  if (result.ok) {
    items.value = await props.getObjects(params);
  }
};

const toggleSelectedItems = (value: boolean, key: number, title: string) => {
  if (value) {
    selectedItems.value.add({
      title: title,
      id: key,
    });
    return;
  }

  for (let item of selectedItems.value) {
    if (item.id === key) {
      selectedItems.value.delete(item);
      break;
    }
  }
};

const removeAllSelectedItems = () => {
  selectedItems.value = new Set<{ id: number; title: string }>([]);
};

const enableSelectable: Ref<boolean> = ref(false);
const clearSelected: Ref<boolean> = ref(false);

const toggleSelect = () => {
  enableSelectable.value = !enableSelectable.value;

  if (!enableSelectable.value) {
    removeAllSelectedItems();
    isAllSelected.value = false;
    clearSelected.value = true;
  }
};

const toggleIsAllSelected = (value: boolean) => {
  isAllSelected.value = value;
};

const toggleClearSelected = () => {
  clearSelected.value = !clearSelected.value;
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

  // Set items
  const result = await props.getObjects(params);

  items.value = {
    results: result.results,
    count: result.count,
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

  const result = await props.saveCreateObjectDialogData(currentValues, continueEditing, sendSaveRequest);

  // Set items
  const newItems = await props.getObjects(params);

  items.value = {
    results: newItems.results,
    count: newItems.count,
  };
};

// Define expose, expose functions / elements to parent element
defineExpose({ toggleDialog });
</script>

<template>
  <div class="container __admin">
    <AdminListViewHeader
      :name="props.pluralName"
      :singular-name="props.singularName"
      :enable-sort="props.enableSort"
      :enable-create-object="props.enableCreateObject"
      :enable-import-export="props.enableImportExport"
      :api-name="props.apiName"
      @update-dialog="toggleDialog"
      @toggle-select="toggleSelect"
    />
    <div v-if="loading"><SpinnerComponent /></div>
    <div v-else>
      <AdminListViewFilter
        :params="params"
        :get-table-filters="props.getTableFilters"
        :singular-name="props.singularName"
        @update-search-term="updateSearchTerm"
        @update-list-filters="updateListFilters"
      />
      <AdminListViewTable
        :enable-selectable="enableSelectable"
        :items="items.results"
        :api-name="props.apiName"
        :pagination="pagination"
        :table-headers="props.tableHeaders"
        :sort="sort"
        :clear-selected="clearSelected"
        @update-list-sort="updateListSort"
        @toggle-element-in-checked-row="toggleSelectedItems"
        @remove-all-elements-from-selected-items="removeAllSelectedItems"
        @toggle-is-all-selected="toggleIsAllSelected"
        @delete-row="deleteRow"
        @toggle-clear-selected="toggleClearSelected"
      />
      <AdminListViewPaginator
        v-if="items.count > pagination.rows"
        :total-results="items.count"
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
        :get-objects="props.getObjects"
        :selected-items="Array.from(selectedItems)"
        :is-all-selected="isAllSelected"
        @update-dialog="toggleDialog"
      />
    </div>
  </div>
</template>
