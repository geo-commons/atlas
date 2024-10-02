<script setup lang="ts">
import AdminListViewHeader from "@/admin/components/AdminListViewHeader.vue";
import AdminListViewDialog from "@/admin/components/AdminListViewDialog.vue";
import { Ref, ref } from "vue";

// Properties
type AdminListViewProps = {
  enableImportExport?: boolean;
  enableCreateObject?: boolean;
  enableSort?: boolean;
  singularName: string;
  pluralName: string;
  apiName: string;
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
export type DialogTypes = "import-dialog" | "export-dialog" | "create-object-dialog";
export type ShowDialogType = { show: boolean; type: DialogTypes };

const showDialog: Ref<ShowDialogType> = ref({
  show: false,
  type: "create-object-dialog",
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
      @update-dialog="toggleDialog"
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
      @update-dialog="toggleDialog"
    />
  </div>
</template>
