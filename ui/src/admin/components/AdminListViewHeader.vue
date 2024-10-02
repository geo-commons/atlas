<script setup lang="ts">
import CogIcon from "@/assets/icons/cog-icon.svg";
import SortIcon from "@/assets/icons/sort-icon.svg";
import AddIcon from "@/assets/icons/add-icon.svg";
import { DialogTypes } from "@/admin/components/AdminListView.vue";

// Properties
type AdminListViewHeaderProps = {
  enableImportExport?: boolean;
  enableCreateObject?: boolean;
  enableSort?: boolean;
  name: string;
};

const props = withDefaults(defineProps<AdminListViewHeaderProps>(), {
  enableImportExport: true,
  enableCreateObject: true,
  enableSort: false,
});

// Emits
const emit = defineEmits<{
  (e: "update-dialog", type: DialogTypes): void;
}>();
</script>

<template>
  <div class="tw-flex tw-flex-row tw-justify-between tw-items-center tw-py-8">
    <h1>{{ props.name }}</h1>
    <div class="tw-flex tw-flex-row tw-gap-2">
      <Button v-if="props.enableImportExport" outlined class="!tw-text-sm !tw-font-medium">
        <CogIcon class="tw-w-4 tw-h-4" />
        Meer opties</Button
      >
      <Button v-if="props.enableSort" outlined class="!tw-text-sm !tw-font-medium">
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
