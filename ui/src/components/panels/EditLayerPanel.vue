<template>
  <Drawer
    :visible="showEditLayerPanel"
    header="Object toevoegen"
    :dismissable="false"
    :pt="{
      mask: '!tw-bg-black/0',
    }"
    @update:visible="toggleShowEditLayerCancelModal"
  >
    <div class="tw-flex tw-flex-col tw-gap-2">
      <label class="form__label" for="edit-layer-panel-choose-layer">Selecteer een kaartlaag</label>
      <Select
        :model-value="editLayerStore.selectedLayer"
        :options="layers"
        filter
        name="edit-layer-panel-choose-layer"
        option-label="title"
        placeholder="Selecteer kaartlaag"
        fluid
        :pt="{
          overlay: '!tw-max-w-48',
        }"
        @update:model-value="(layer) => editLayerStore.setSelectedLayer(layer)"
      />
    </div>

    <template #footer>
      <div class="tw-flex tw-items-center tw-gap-2 tw-p-4">
        <Button
          label="Annuleren"
          icon="pi pi-times"
          class="tw-flex-auto"
          outlined
          @click="toggleShowEditLayerCancelModal"
        ></Button>
        <Button label="Opslaan" icon="pi pi-save" class="tw-flex-auto" @click="toggleShowEditLayerSaveModal"></Button>
      </div>
    </template>
  </Drawer>

  <EditLayerSaveModal
    :visible="showEditLayerSaveModal"
    :on-cancel="cancelLayerSaveModal"
    :on-save="saveLayerSaveModal"
  />

  <EditLayerCancelModal
    :visible="showEditLayerCancelModal"
    :on-cancel="cancelLayerCancelModal"
    :on-proceed="proceedLayerCancelModal"
  />
</template>

<script setup lang="ts">
import { useEditLayerStore } from "@/stores/edit_layer_store";
import { ref, watch } from "vue";
import { ILayer } from "@/types/layer";
import EditLayerSaveModal from "@/components/modals/EditLayerSaveModal.vue";
import EditLayerCancelModal from "@/components/modals/EditLayerCancelModal.vue";

interface EditLayerPanelProps {
  layers: Array<ILayer>;
}

// Props
const { layers } = defineProps<EditLayerPanelProps>();

// Store
const editLayerStore = useEditLayerStore();

// References
const showEditLayerPanel = ref<boolean>(false);
const showEditLayerSaveModal = ref<boolean>(false);
const showEditLayerCancelModal = ref<boolean>(false);

// Watch
watch(
  () => editLayerStore.feature,
  (value, oldValue) => {
    if (oldValue === null && value !== null && !showEditLayerPanel.value) {
      showEditLayerPanel.value = true;
    }
  },
  { deep: true },
);

// Methods
const handleDrawerClose = (value: boolean) => {
  showEditLayerPanel.value = value;
  // TODO: ADD prevention (modal to check if somebody actually wants to close modal and reset his work)
  // TODO: Explore why line and polygon additions don't get removed
  // TODO: Explore why enter always closes the drawer
  // TODO: Don't close on escape, only close modal on escape
  editLayerStore.resetFeature();
};

const toggleShowEditLayerSaveModal = () => {
  showEditLayerSaveModal.value = !showEditLayerSaveModal.value;
};

const toggleShowEditLayerCancelModal = () => {
  showEditLayerCancelModal.value = !showEditLayerCancelModal.value;
};

const proceedLayerCancelModal = () => {
  toggleShowEditLayerCancelModal();

  handleDrawerClose(false);
};

const cancelLayerCancelModal = () => {
  toggleShowEditLayerCancelModal();
};

const saveLayerSaveModal = () => {
  toggleShowEditLayerSaveModal();

  handleSaveFeature();
};

const cancelLayerSaveModal = () => {
  toggleShowEditLayerSaveModal();
};

const handleSaveFeature = () => {
  // TODO: ADD prevention (modal to check if somebody actually wants to close modal and reset his work)
  // TODO: Explore why line and polygon additions don't get removed

  showEditLayerPanel.value = false;
  editLayerStore.resetFeature();
};
</script>

<style scoped lang="scss"></style>
