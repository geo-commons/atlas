<script setup lang="ts">
import CogIcon from "@/assets/icons/cog-icon.svg";
import SortIcon from "@/assets/icons/sort-icon.svg";
import AddIcon from "@/assets/icons/add-icon.svg";
import { DialogTypes } from "@/admin/components/AdminListView.vue";
import { ref } from "vue";

// Properties
type AdminListViewHeaderProps = {
  enableImportExport?: boolean;
  enableCreateObject?: boolean;
  enableSort?: boolean;
  name: string;
  apiName: string;
};

const props = withDefaults(defineProps<AdminListViewHeaderProps>(), {
  enableImportExport: true,
  enableCreateObject: true,
  enableSort: false,
});

// Import / Export logic
const menu = ref();

const toggle = (event: any) => {
  menu.value.toggle(event);
};

const items = ref([
  {
    label: "Importeren",
    icon: "pi pi-file-import",
    command: () => {
      emit("update-dialog", "import-dialog");
    },
  },
  {
    label: "Exporteren",
    icon: "pi pi-file-export",
    command: () => {
      emit("update-dialog", "export-dialog");
    },
  },
]);

// Emits
const emit = defineEmits<{
  (e: "update-dialog", type: DialogTypes): void;
}>();
</script>

<template>
  <div class="tw-flex tw-flex-col gap-2 md:tw-flex-row md:tw-justify-between md:tw-items-center">
    <h1>{{ props.name }}</h1>
    <div class="tw-flex tw-flex-col md:tw-flex-row tw-gap-2">
      <Button
        v-if="props.enableImportExport"
        outlined
        class="!tw-text-sm !tw-font-medium"
        aria-haspopup="true"
        aria-controls="overlay_menu"
        @click="toggle"
      >
        <CogIcon class="tw-w-4 tw-h-4" />
        Meer opties</Button
      >
      <Menu id="overlay_menu" ref="menu" :model="items" :popup="true" class="!tw-text-sm" />

      <Button
        v-if="props.enableSort"
        outlined
        class="!tw-text-sm !tw-font-medium !tw-no-underline"
        as="router-link"
        label="Router"
        :to="{
          name: 'sort',
          params: { parentRoute: props.apiName },
        }"
      >
        <SortIcon class="tw-w-4 tw-h-4" />
        Sortering</Button
      >
      <Button
        v-if="props.enableCreateObject"
        class="!tw-text-sm !tw-font-medium"
        @click="$emit('update-dialog', 'create-object-dialog')"
      >
        <AddIcon class="tw-w-4 tw-h-4" />
        Nieuwe laag</Button
      >
    </div>
  </div>
</template>
