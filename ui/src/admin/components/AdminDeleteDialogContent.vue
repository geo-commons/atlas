<template>
  <div>
    <p>
      Weet u zeker dat u de volgende
      {{ props.selectedItems.length === 1 ? props.singularName.toLowerCase() : props.pluralName.toLowerCase() }} wilt
      verwijderen?
    </p>
    <ul class="selected-rows">
      <li v-for="row in props.selectedItems" :key="row.id">- {{ row.title }}</li>
    </ul>
  </div>
  <div class="admin-btn-wrapper">
    <Button severity="secondary" outlined type="button" @click="emit('update-dialog', props.showDialog.type)">
      Annuleer
    </Button>
    <Button type="button" severity="danger" :disabled="!props.selectedItems.length" @click="emit('delete')">
      Verwijderen
    </Button>
  </div>
</template>

<script setup lang="ts">
import { EDialogTypes, ShowDialogType } from "@/types/dialog";

interface AdminDeleteDialogProps {
  selectedItems: Array<{ id: number; title: string }>;
  singularName: string;
  pluralName: string;
  showDialog: ShowDialogType;
}

const props = withDefaults(defineProps<AdminDeleteDialogProps>(), {});

// Emits
const emit = defineEmits<{
  (e: "update-dialog", type: EDialogTypes): void;
  (e: "delete"): void;
}>();
</script>
