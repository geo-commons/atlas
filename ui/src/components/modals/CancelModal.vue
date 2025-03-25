<template>
  <Dialog
    :visible="visible"
    modal
    header="Annuleren"
    :style="{ width: '25rem' }"
    :pt="{ header: '!tw-pb-0' }"
    @update:visible="onCancel"
  >
    <p>
      {{ message }}
    </p>
    <div class="tw-flex tw-items-center tw-gap-2">
      <Button label="Verder met bewerken" class="tw-flex-auto" outlined @click="onCancel"></Button>
      <Button label="Bewerken sluiten" icon="pi pi-times" class="tw-flex-auto" @click="onProceed"></Button>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
interface EditLayerCancelModalProps {
  message: string;
  visible: boolean;
  onCancel: () => void;
  onProceed: () => void;
}

const { message, visible, onCancel, onProceed } = defineProps<EditLayerCancelModalProps>();
</script>
