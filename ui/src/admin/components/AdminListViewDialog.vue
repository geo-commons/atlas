<script setup lang="ts">
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import AdminFileExport from "@/admin/components/AdminFileExport.vue";
import AdminFileImport from "@/admin/components/AdminFileImport.vue";
import { computed, onMounted, Ref, ref } from "vue";
import { EDialogTypes, ShowDialogType } from "@/types/dialog";
import AdminDeleteDialogContent from "@/admin/components/AdminDeleteDialogContent.vue";

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
  // This prop is only necessary if enableImportExport is true
  selectedItems?: Array<{ id: number; title: string }>;
};

const props = withDefaults(defineProps<AdminListViewDialogProps>(), {});

// Emits
const emit = defineEmits<{
  (e: "update-dialog", type: EDialogTypes): void;
  (e: "delete"): void;
  (e: "reset-selection"): void;
}>();

// Dialog logic
const sections = ref({});
const adminFormSectionsRef: Ref<{ resetForm: () => void } | null> = ref(null);

const headerMap = {
  [EDialogTypes.Create]: (singularName: string) => `Configureer nieuwe ${singularName.toLowerCase()}`,
  [EDialogTypes.Import]: (pluralName: string) => `Importeer bestaande ${pluralName.toLowerCase()}`,
  [EDialogTypes.Export]: (pluralName: string) => `Exporteer bestaande ${pluralName.toLowerCase()}`,
  [EDialogTypes.ExportAll]: (pluralName: string) => `Exporteer bestaande ${pluralName.toLowerCase()}`,
  [EDialogTypes.Delete]: (pluralName: string) => `Verwijder geselecteerde ${pluralName.toLowerCase()}`,
};

const header = computed(() => {
  const headerGenerator = headerMap[props.showDialog.type];
  return headerGenerator
    ? headerGenerator(props.showDialog.type === EDialogTypes.Create ? props.singularName : props.pluralName)
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
    class="xl:tw-w-[1216px] tw-w-[calc(100%-32px)] md:tw-w-[calc(100%-64px)]"
    :pt="{
      header: '!tw-pb-0',
    }"
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
    <div v-else-if="props.showDialog.type === EDialogTypes.Delete">
      <AdminDeleteDialogContent
        :selected-items="props.selectedItems"
        :singular-name="props.singularName"
        :plural-name="props.pluralName"
        :show-dialog="showDialog"
        @update-dialog="(dialogType: ShowDialogType) => emit('update-dialog', dialogType)"
        @delete="emit('delete')"
      />
    </div>
  </Dialog>
</template>
