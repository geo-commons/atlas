<script setup lang="ts">
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import AdminFileExport from "@/admin/components/AdminFileExport.vue";
import AdminFileImport from "@/admin/components/AdminFileImport.vue";
import { ShowDialogType, DialogTypes } from "@/admin/components/AdminListView.vue";
import { onMounted, ref, watch } from "vue";

// Properties
type AdminListViewDialogProps = {
  apiName: string;
  singularName: string;
  pluralName: string;
  showDialog: ShowDialogType;
  isAllSelected: boolean;
  getObjects: () => void;
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

const props = withDefaults(defineProps<AdminListViewDialogProps>(), {});

// Emits
const emit = defineEmits<{
  (e: "update-dialog", type: DialogTypes): void;
}>();

// Dialog logic
const sections = ref({});

// lifecycle hooks
onMounted(async () => {
  if (props.getCreateObjectDialogSections) {
    sections.value = props.getCreateObjectDialogSections();
  }
});
</script>

<template>
  <Dialog
    :visible="props.showDialog.show"
    :modal="true"
    :closable="true"
    :draggable="false"
    :header="
      props.showDialog.type === 'create-object-dialog'
        ? `Configureer nieuwe ${props.singularName.toLowerCase()}`
        : props.showDialog.type === 'import-dialog'
          ? `Importeer bestaande ${props.pluralName.toLowerCase()}`
          : props.showDialog.type === 'export-dialog'
            ? `Exporteer bestaande ${props.pluralName.toLowerCase()}`
            : ''
    "
    :dismissable-mask="true"
    class="tw-w-[80%]"
    @update:visible="$emit('update-dialog', props.showDialog.type)"
  >
    <AdminFormSections
      v-if="
        sections &&
        props.initialCreateObjectDialogData &&
        props.saveCreateObjectDialogData &&
        props.apiName &&
        props.showDialog.type === 'create-object-dialog'
      "
      :sections="sections"
      :initial-values="props.initialCreateObjectDialogData"
      :create-view="true"
      :form-object="props.apiName"
      :object-specific-save="props.saveCreateObjectDialogData"
      @close="$emit('update-dialog', props.showDialog.type)"
    />
    <div v-else-if="props.showDialog.type === 'import-dialog'">
      <AdminFileImport
        :object-name="props.apiName"
        @import-successful="props.getObjects"
        @close="$emit('update-dialog', props.showDialog.type)"
      />
    </div>
    <div v-else-if="props.showDialog.type === 'export-dialog'">
      <AdminFileExport
        :object-name="props.apiName"
        :selected-rows="props.selectedItems"
        :is-all-selected="props.isAllSelected"
        @close="$emit('update-dialog', props.showDialog.type)"
      />
    </div>
  </Dialog>
</template>
