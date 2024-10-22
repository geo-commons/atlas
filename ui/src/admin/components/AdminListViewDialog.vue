<script setup lang="ts">
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import AdminFileExport from "@/admin/components/AdminFileExport.vue";
import AdminFileImport from "@/admin/components/AdminFileImport.vue";
import { computed, onMounted, Ref, ref } from "vue";
import { EDialogTypes, ShowDialogType } from "@/types/dialog";

// Properties
type AdminListViewDialogProps = {
  apiName: string;
  singularName: string;
  pluralName: string;
  showDialog: ShowDialogType;
  getObjects: () => void;
  getCreateObjectDialogSections?: () => object;
  initialCreateObjectDialogData?: object;
  saveCreateObjectDialogData?: (
    currentValues: object,
    continueEditing: boolean,
    sendSaveRequest: (apiUrl: string, method: string, currentValues: object) => Response,
  ) => void;
  // This prop is only necessary if enableImportExport is true
  selectedItems?: Array<{ id: number; title: string }>;
};

const props = withDefaults(defineProps<AdminListViewDialogProps>(), {});

// Emits
const emit = defineEmits<{
  (e: "update-dialog", type: EDialogTypes): void;
  (e: "reset-selection"): void;
}>();

// Dialog logic
const sections = ref({});
const adminFormSectionsRef: Ref<{ resetForm: () => void } | null> = ref(null);

const header = computed(() => {
  return props.showDialog.type === EDialogTypes.Create
    ? `Configureer nieuwe ${props.singularName.toLowerCase()}`
    : props.showDialog.type === EDialogTypes.Import
      ? `Importeer bestaande ${props.pluralName.toLowerCase()}`
      : props.showDialog.type === EDialogTypes.Export || props.showDialog.type === EDialogTypes.ExportAll
        ? `Exporteer bestaande ${props.pluralName.toLowerCase()}`
        : "";
});

const updateDialog = () => {
  emit("update-dialog", props.showDialog.type);

  if (adminFormSectionsRef.value) {
    adminFormSectionsRef.value.resetForm();
  }
};

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
    :header="header"
    :dismissable-mask="true"
    class="tw-w-[80%]"
    @update:visible="updateDialog"
  >
    <AdminFormSections
      v-if="
        sections &&
        props.initialCreateObjectDialogData &&
        props.saveCreateObjectDialogData &&
        props.apiName &&
        props.showDialog.type === EDialogTypes.Create
      "
      ref="adminFormSectionsRef"
      :sections="sections"
      :initial-values="props.initialCreateObjectDialogData"
      :reset-values="props.initialCreateObjectDialogData"
      :create-view="true"
      :form-object="props.apiName"
      :object-specific-save="props.saveCreateObjectDialogData"
      @close="updateDialog"
    />
    <div v-else-if="props.showDialog.type === EDialogTypes.Import">
      <AdminFileImport
        :object-name="{ apiName: props.apiName, singularName: props.singularName, pluralName: props.pluralName }"
        @import-successful="emit('reset-selection')"
        @close="emit('update-dialog', props.showDialog.type)"
      />
    </div>
    <div v-else-if="props.showDialog.type === EDialogTypes.Export || props.showDialog.type === EDialogTypes.ExportAll">
      <AdminFileExport
        :object-name="{ apiName: props.apiName, singularName: props.singularName, pluralName: props.pluralName }"
        :selected-rows="props.selectedItems"
        :export-type="props.showDialog.type"
        @close="emit('update-dialog', props.showDialog.type)"
        @export-successful="emit('reset-selection')"
      />
    </div>
  </Dialog>
</template>
