<template>
  <Dialog
    :visible="visible"
    modal
    header="Verwijderen"
    :style="{ width: '25rem' }"
    :pt="{ header: '!tw-pb-0' }"
    @update:visible="onCancel"
  >
    <p>
      {{ message }}
    </p>
    <div class="tw-flex tw-items-center tw-gap-2">
      <Button label="Annuleren" class="tw-flex-auto" outlined @click="onCancel"></Button>
      <Button label="Verwijderen" icon="pi pi-times" class="tw-flex-auto" @click="onDelete"></Button>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
interface DeleteLayerCancelModalProps {
  message: string;
  visible: boolean;
  onCancel: () => void;
  onDelete: () => void;
}

const { message, visible, onCancel, onDelete } = defineProps<DeleteLayerCancelModalProps>();
</script>
