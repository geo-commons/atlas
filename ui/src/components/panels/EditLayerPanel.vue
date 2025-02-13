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
        :options="layers.filter((layer) => layer.is_visible)"
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

    <div v-if="editLayerStore.selectedLayer" class="tw-py-4">
      <div v-if="layerTypeIsWFSOrWMSWFS && !drawerError" class="tw-flex tw-flex-col">
        <label class="form__label" for="edit-layer-panel-choose-layer">Objectgegevens</label>
        <vee-form ref="form" v-slot="{ errors }" class="tw-flex tw-flex-col tw-gap-2 tw-py-2" @submit="handleSubmit">
          <div v-for="property in layerProperties" :key="property.name">
            <Message
              :class="{
                'tw-hidden': !errors[property.name],
              }"
              class="edit-layer-panel__error"
              severity="error"
              variant="simple"
              >{{ errors[property.name] }}
            </Message>
            <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-items-start">
              <label
                :for="property.name"
                :class="{
                  'edit-layer-panel__error': errors[property.name],
                }"
                >{{ property.name }}</label
              >
              <vee-field
                v-slot="{ field }"
                :name="property.name"
                type="text"
                :rules="property.nillable ? '' : 'required'"
              >
                <InputText
                  v-bind="field"
                  :id="property.name"
                  :placeholder="property.name"
                  type="text"
                  :invalid="Boolean(errors[property.name])"
                />
              </vee-field>
            </div>
          </div>
        </vee-form>
      </div>
      <!-- Write transactions are restricted to layers of type 'WFS' and 'WMS_WFS'.
      Display an error message if the selected layer's source type is anything other than these two.
      If layer is of type 'WFS' or 'WMS_WFS' but their is still an error, show this error-->
      <div v-else>
        <Message severity="error">{{
          layerTypeIsWFSOrWMSWFS
            ? drawerError
            : "Atlas ondersteund enkel het toevoegen van objecten voor WFS en WMS_WFS kaartlagen"
        }}</Message>
      </div>
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
        <Button
          :disabled="isSaveButtonDisabled"
          label="Opslaan"
          icon="pi pi-save"
          class="tw-flex-auto"
          @click="submitFormManually"
        ></Button>
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
import { computed, ref, unref, watch } from "vue";
import { ELayerTypes, IFeatureProperties, ILayer, ILayerProperties } from "@/types/layer";
import EditLayerSaveModal from "@/components/modals/EditLayerSaveModal.vue";
import EditLayerCancelModal from "@/components/modals/EditLayerCancelModal.vue";
import { addFeatureToLayer, getWfsOrWFSWMSLayerFeatureInformation } from "@/services/layer";
import { IUser } from "@/types/user";
import { Form as VeeForm, Field as VeeField, defineRule } from "vee-validate";
import { required } from "@vee-validate/rules";

interface EditLayerPanelProps {
  layers: Array<ILayer>;
  user: IUser;
}

// Props
const { layers, user } = defineProps<EditLayerPanelProps>();

// Emits
const emit = defineEmits<{
  (e: "set-selected-area", area: null | string): void;
  (e: "set-tool", tool: string): void;
}>();

// Store
const editLayerStore = useEditLayerStore();

// References
const showEditLayerPanel = ref<boolean>(false);
const showEditLayerSaveModal = ref<boolean>(false);
const showEditLayerCancelModal = ref<boolean>(false);
const drawerError = ref<string | null>(null);
const layerProperties = ref<ILayerProperties>([]);
const featureProperties = ref<IFeatureProperties>({
  targetNamespace: "",
  targetPrefix: "",
});
const form = ref(null);

// Computes
const layerTypeIsWFSOrWMSWFS = computed(() => {
  return editLayerStore.selectedLayer
    ? editLayerStore.selectedLayer.source_type === ELayerTypes.WFS ||
        editLayerStore.selectedLayer.source_type === ELayerTypes.WMS_WFS
    : false;
});

const isSaveButtonDisabled = computed(() => {
  return !layerTypeIsWFSOrWMSWFS.value || !editLayerStore.selectedLayer;
});

watch(
  () => editLayerStore.feature,
  (value, oldValue) => {
    if (oldValue === null && value !== null && !showEditLayerPanel.value) {
      showEditLayerPanel.value = true;
    }
  },
  { deep: true },
);

// Watch
watch(
  () => editLayerStore.selectedLayer,
  async (selectedLayer) => {
    if (selectedLayer) {
      try {
        const { targetPrefix, targetNamespace, featureTypes } = await getWfsOrWFSWMSLayerFeatureInformation(
          selectedLayer,
          user,
        );

        layerProperties.value = featureTypes[0].properties ? featureTypes[0].properties : [];
        featureProperties.value = {
          targetPrefix: targetPrefix,
          targetNamespace: targetNamespace,
        };
        drawerError.value = null;

        if (form.value) {
          (form.value as any).resetForm();
        }
      } catch (e: unknown) {
        layerProperties.value = [];
        drawerError.value = (e as Error).message;

        console.error((e as Error).message);
      }
    }
  },
  { deep: true },
);

// Form logic
defineRule("required", (value: string) => {
  if (!required(value)) {
    return "Dit veld is verplicht";
  }
  return true;
});

const handleSubmit = (values: any) => {
  console.log(values);

  toggleShowEditLayerSaveModal();
};

const submitFormManually = () => {
  if (form.value) {
    (form.value as any).$el.requestSubmit();
  }
};

// Methods
const handleDrawerClose = (value: boolean) => {
  showEditLayerPanel.value = value;
  // TODO: Don't close on escape, only close modal on escape. This is a known bug in PrimeVue: https://github.com/primefaces/primevue/issues/5138
  editLayerStore.resetFeature();
  editLayerStore.setSelectedLayer(null);

  emit("set-selected-area", null);
  emit("set-tool", "");
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

const handleSaveFeature = async () => {
  try {
    await addFeatureToLayer(editLayerStore.selectedLayer!, editLayerStore.feature, unref(featureProperties));
  } catch (e) {
    console.error((e as Error).message);
  }

  handleDrawerClose(false);
};
</script>

<style scoped lang="scss">
.edit-layer-panel__error {
  color: var(--color-alert) !important;
}
</style>
