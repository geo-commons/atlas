<script setup lang="ts">
import AdminListViewHeader from "@/admin/components/AdminListViewHeader.vue";
import AdminListViewDialog from "@/admin/components/AdminListViewDialog.vue";
import { computed, onMounted, Ref, ref } from "vue";
import AdminListViewTable, { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import AdminListViewFilter, { TableFilter } from "@/admin/components/AdminListViewFilter.vue";
import { useRoute, useRouter } from "vue-router";
import { TableHeaderRef } from "@/admin/components/AdminListViewTableHeader.vue";
import AdminListViewPaginator, { PaginationRef } from "@/admin/components/AdminListViewPaginator.vue";
import { PageState } from "primevue/paginator";
import Cookies from "js-cookie";
import SpinnerComponent from "@/components/Spinner.vue";
import { EDialogTypes, ShowDialogType } from "@/types/dialog";
import { useToast } from "primevue";

// Properties
type AdminListViewProps = {
  enableImportExport?: boolean;
  enableCreateObject?: boolean;
  enableDuplicate?: boolean;
  enableDeleteMultiple?: boolean;
  enableDelete?: boolean;
  enableEdit?: boolean;
  enableSort?: boolean;
  singularName: string;
  pluralName: string;
  apiName: string;
  loading: boolean;
  getObjects: (searchParams?: URLSearchParams) => Promise<{ results: Array<object>; count: number }>;
  tableHeaders: Array<TableHeader>;
  getTableFilters?: () => Array<TableFilter>;
  viewBaseUrl?: string;
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
  enableSort: false,
  enableDelete: true,
  enableEdit: true,
  blockDelete: () => [],
});

const router = useRouter();
const toast = useToast();

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
const duplicateSelectedItems = async () => {
  if (selectedItems.value.length) {
    const data = {
      ids: selectedItems.value.map((selectedItem) => selectedItem.id),
    };

    try {
      const result = await fetch(`/atlas/api/v1/${props.apiName}/duplicate/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "X-CSRFToken": Cookies.get("csrftoken"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!result.ok) {
        throw new Error("something went wrong");
      }

      toast.add({
        severity: "success",
        summary: `Dupliceren gelukt`,
        detail: `Het dupliceren van ${props.pluralName.toLowerCase()} is gelukt`,
        life: 5000,
      });

      await refreshAndResetItems();
    } catch (e) {
      toast.add({
        severity: "error",
        summary: `Dupliceren niet gelukt`,
        detail: `Het dupliceren van ${props.pluralName.toLowerCase()} is niet gelukt`,
        life: 5000,
      });

      console.error(e);
    }
  }
};

// Delete logic
const deleteSelectedItems = async () => {
  if (selectedItems.value.length) {
    const data = {
      ids: selectedItems.value.map((selectedItem) => selectedItem.id),
    };

    try {
      const result = await fetch(`/atlas/api/v1/${props.apiName}/delete/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "X-CSRFToken": Cookies.get("csrftoken"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!result.ok) {
        throw new Error("something went wrong");
      }

      toast.add({
        severity: "success",
        summary: `Verwijderen gelukt`,
        detail: `Het verwijderen van ${props.pluralName.toLowerCase()} is gelukt`,
        life: 5000,
      });

      toggleDialog(showDialog.value.type);

      await refreshAndResetItems();
    } catch (e) {
      toast.add({
        severity: "error",
        summary: `Verwijderen mislukt`,
        detail: `Het verwijderen van ${props.pluralName.toLowerCase()} is niet gelukt`,
        life: 5000,
      });

      toggleDialog(showDialog.value.type);

      console.error(e);
    }
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
const selectedItems: Ref<Array<{ id: number; title: string }>> = ref([]);
const route = useRoute();

const doRequestAndUpdateRouter = async (params: URLSearchParams) => {
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

const updateSearchTerm = async (value: string) => {
  if (value) {
    params.set("search", value);
  } else {
    params.delete("search");
  }

  params.set("page", "1");
  params.set("page_size", pagination.value.rows.toString());

  await doRequestAndUpdateRouter(params);
};

const updateListFilters = async (value: any, key: string) => {
  if (value && value?.length) {
    params.set(key, value.map((val: any) => (val.id ? val.id : val)).join(","));
  } else {
    params.delete(key);
  }

  params.set("page", "1");
  params.set("page_size", pagination.value.rows.toString());

  await doRequestAndUpdateRouter(params);
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

  await doRequestAndUpdateRouter(params);
};

const updateListPagination = async (pageState: PageState) => {
  pagination.value = {
    page: pageState.page,
    rows: pageState.rows,
  };

  params.set("page", (pagination.value.page + 1).toString());
  params.set("page_size", pagination.value.rows.toString());

  await doRequestAndUpdateRouter(params);
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

const adminListViewTableRef: Ref<null | {
  resetSelection: () => void;
}> = ref(null);

const refreshAndResetItems = async () => {
  items.value = await props.getObjects(params);
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
      :enable-sort="props.enableSort"
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
    <div v-if="loading">
      <SpinnerComponent />
    </div>
    <div v-else>
      <AdminListViewFilter
        :params="params"
        :get-table-filters="props.getTableFilters"
        :singular-name="props.singularName"
        @update-search-term="updateSearchTerm"
        @update-list-filters="updateListFilters"
      />
      <AdminListViewTable
        ref="adminListViewTableRef"
        :items="items.results"
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
        :selected-items="selectedItems"
        @update-dialog="toggleDialog"
        @reset-selection="refreshAndResetItems"
        @delete="deleteSelectedItems"
      />
    </div>
  </div>
</template>
