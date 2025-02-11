<template>
  <Dialog
    :visible="visible"
    modal
    header="Opslaan"
    :style="{ width: '25rem' }"
    :pt="{ header: '!tw-pb-0' }"
    @update:visible="onCancel"
  >
    <p>
      Wanneer u doorgaat met opslaan, wordt het door u getekende object, inclusief alle bijbehorende eigenschappen,
      opgeslagen binnen de geselecteerde laag in GeoServer.
    </p>
    <div class="tw-flex tw-items-center tw-gap-2">
      <Button label="Annuleren" icon="pi pi-times" class="tw-flex-auto" outlined @click="onCancel"></Button>
      <Button label="Opslaan" icon="pi pi-save" class="tw-flex-auto" @click="onSave"></Button>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
interface EditLayerSaveModalProps {
  visible: boolean;
  onCancel: () => void;
  onSave: () => void;
}

const { visible, onCancel, onSave } = defineProps<EditLayerSaveModalProps>();
</script>
