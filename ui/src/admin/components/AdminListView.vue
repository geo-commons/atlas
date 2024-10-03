<script setup lang="ts">
import AdminListViewHeader from "@/admin/components/AdminListViewHeader.vue";
import AdminListViewDialog from "@/admin/components/AdminListViewDialog.vue";
import { onMounted, Ref, ref } from "vue";
import AdminListViewTable, { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import AdminListViewFilter, { TableFilter } from "@/admin/components/AdminListViewFilter.vue";
import { useRoute, useRouter } from "vue-router";
import { TableHeaderRef } from "@/admin/components/AdminListViewTableHeader.vue";

// Properties
type AdminListViewProps = {
  enableImportExport?: boolean;
  enableCreateObject?: boolean;
  enableSort?: boolean;
  singularName: string;
  pluralName: string;
  apiName: string;
  loading: boolean;
  getObjects: (searchParams?: URLSearchParams) => Promise<Array<object>>;
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
  // This prop is only necessary if enableImportExport is true
  selectedItems?: Array<any>;
};

const props = withDefaults(defineProps<AdminListViewProps>(), {
  enableImportExport: true,
  enableCreateObject: true,
  enableSort: false,
});

// Dialog logic
export type DialogTypes = "import-dialog" | "export-dialog" | "create-object-dialog";
export type ShowDialogType = { show: boolean; type: DialogTypes };

const showDialog: Ref<ShowDialogType> = ref({
  show: false,
  type: "create-object-dialog",
});

// Table logic
let params: URLSearchParams = new URLSearchParams();
const items: Ref<Array<object>> = ref([]);
const sort: Ref<TableHeaderRef> = ref({ sortKey: "", sortAscending: true });
const router = useRouter();
const route = useRoute();

const updateSearchTerm = async (value: string) => {
  if (value) {
    params.set("search", value);
  } else {
    params.delete("search");
  }

  await router.push({
    path: route.path,
    query: {
      ...Object.fromEntries(params),
    },
  });

  items.value = await props.getObjects(params);
};

const updateListFilters = async (value: any, key: string) => {
  if (value && value?.length) {
    params.set(key, value.map((val: any) => val.id).join(","));
  } else {
    params.delete(key);
  }

  await router.push({
    path: route.path,
    query: {
      ...Object.fromEntries(params),
    },
  });

  items.value = await props.getObjects(params);
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

  await router.push({
    path: route.path,
    query: {
      ...Object.fromEntries(params),
    },
  });

  items.value = await props.getObjects(params);
};

// Lifecycle hooks
onMounted(async () => {
  params = new URLSearchParams(route.query as any);
  const order = params.get("ordering");
  sort.value = {
    sortKey: order ? order.replace("-", "") : "",
    sortAscending: order ? !order.startsWith("-") : true,
  };
  items.value = await props.getObjects(params);
});

const toggleDialog = (type: DialogTypes) => {
  showDialog.value = {
    type: type,
    show: !showDialog.value.show,
  };
};

// Define expose, expose functions / elements to parent element
defineExpose({ toggleDialog });
</script>

<template>
  <div class="container __admin">
    <AdminListViewHeader
      :name="props.pluralName"
      :enable-sort="props.enableSort"
      :enable-create-object="props.enableCreateObject"
      :enable-import-export="props.enableImportExport"
      :api-name="props.apiName"
      @update-dialog="toggleDialog"
    />
    <div v-if="loading">Laden...</div>
    <div v-else>
      <AdminListViewFilter
        :params="params"
        :get-table-filters="props.getTableFilters"
        @update-search-term="updateSearchTerm"
        @update-list-filters="updateListFilters"
      />
      <AdminListViewTable
        :items="items"
        :api-name="props.apiName"
        :table-headers="props.tableHeaders"
        :sort="sort"
        @update-list-sort="updateListSort"
      />
      <AdminListViewDialog
        ref="adminListViewDialogRef"
        :show-dialog="showDialog"
        :singular-name="props.singularName"
        :plural-name="props.pluralName"
        :get-create-object-dialog-sections="props.getCreateObjectDialogSections"
        :save-create-object-dialog-data="props.saveCreateObjectDialogData"
        :initial-create-object-dialog-data="props.initialCreateObjectDialogData"
        :api-name="props.apiName"
        :get-objects="props.getObjects"
        :selected-items="props.selectedItems"
        @update-dialog="toggleDialog"
      />
    </div>
  </div>
</template>
