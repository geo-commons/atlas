<script setup lang="ts">
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import AdminFileExport from "@/admin/components/AdminFileExport.vue";
import AdminFileImport from "@/admin/components/AdminFileImport.vue";
import { ShowDialogType, DialogTypes } from "@/admin/components/AdminListView.vue";
import { onMounted, Ref, ref } from "vue";

// Properties
type AdminListViewDialogProps = {
  apiName: string;
  singularName: string;
  pluralName: string;
  showDialog: ShowDialogType;
  getCreateObjectDialogSections?: () => object;
  initialCreateObjectDialogData?: object;
  saveCreateObjectDialogData?: (
    currentValues: object,
    continueEditing: boolean,
    sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
  ) => void;
};

const props = withDefaults(defineProps<AdminListViewDialogProps>(), {});

// Emits
const emit = defineEmits<{
  (e: "update-dialog", type: DialogTypes): void;
}>();

// Dialog logic
const sections = ref({});

const adminFormsRef: Ref<null | { sendSaveRequest: (apiUrl: any, method: any, currentValues: any) => void }> =
  ref(null);

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
        ? `Configureer nieuwe ${props.singularName}`
        : props.showDialog.type === 'import-dialog'
          ? `Importeer bestaande ${props.pluralName}`
          : props.showDialog.type === 'export-dialog'
            ? `Exporteer bestaande ${props.pluralName}`
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
    <!--    <div v-else-if="modalType === 'import'">-->
    <!--      <AdminFileImport :object-name="'datasets'" @import-successful="getDatasets" @close="closeFormModal" />-->
    <!--    </div>-->
    <!--    <div v-else-if="modalType === 'export'">-->
    <!--      <AdminFileExport :object-name="'datasets'" :selected-rows="selectedItems" @close="closeFormModal" />-->
    <!--    </div>-->
  </Dialog>
</template>
