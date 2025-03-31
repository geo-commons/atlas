<template>
  <Dialog
    :visible="visible"
    modal
    class="tw-max-w-[25rem] tw-w-[25rem]"
    :header="header"
    :pt="{ header: '!tw-pb-0' }"
    @update:visible="onCancel"
  >
    <p>{{ message }}</p>
    <div class="tw-flex tw-items-center tw-gap-2">
      <Button :label="cancelLabel" :icon="cancelIcon" class="tw-flex-auto" outlined @click="onCancel" />
      <Button :label="confirmLabel" :icon="confirmIcon" class="tw-flex-auto" @click="onConfirm" />
    </div>
  </Dialog>
</template>

<script setup lang="ts">
interface EditLayerActionModalProps {
  visible: boolean;
  message: string;
  header: string;
  cancelLabel: string;
  cancelIcon?: string;
  confirmLabel: string;
  confirmIcon?: string;
  onCancel: () => void;
  onConfirm: () => void;
}

const { visible, message, header, cancelLabel, cancelIcon, confirmLabel, confirmIcon, onCancel, onConfirm } =
  defineProps<EditLayerActionModalProps>();
</script>
