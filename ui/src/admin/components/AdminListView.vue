<script setup lang="ts">
import AdminListViewHeader from "@/admin/components/AdminListViewHeader.vue";
import AdminListViewDialog from "@/admin/components/AdminListViewDialog.vue";
import { onMounted, Ref, ref } from "vue";
import AdminListViewTable, { TableHeader } from "@/admin/components/AdminListViewTable.vue";

// Properties
type AdminListViewProps = {
  enableImportExport?: boolean;
  enableCreateObject?: boolean;
  enableSort?: boolean;
  singularName: string;
  pluralName: string;
  apiName: string;
  getObjects: () => Promise<Array<object>>;
  tableHeaders: Array<TableHeader>;
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
const items: Ref<Array<object>> = ref([]);

// Lifehooks
onMounted(async () => {
  items.value = await props.getObjects();
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
    <AdminListViewTable :items="items" :api-name="props.apiName" :table-headers="props.tableHeaders" />
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
</template>
