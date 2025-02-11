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
      Wanneer u annuleert, wordt het door u getekende object, inclusief alle bijbehorende eigenschappen, niet opgeslagen
      binnen de geselecteerde laag in GeoServer. Alle onopgeslagen wijzigingen gaan verloren.
    </p>
    <div class="tw-flex tw-items-center tw-gap-2">
      <Button label="Doorgaan" class="tw-flex-auto" outlined @click="onCancel"></Button>
      <Button label="Wijzigingen annuleren" icon="pi pi-times" class="tw-flex-auto" @click="onProceed"></Button>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
interface EditLayerCancelModalProps {
  visible: boolean;
  onCancel: () => void;
  onProceed: () => void;
}

const { visible, onCancel, onProceed } = defineProps<EditLayerCancelModalProps>();
</script>
