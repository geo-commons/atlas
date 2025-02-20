<template>
  <Drawer
    :visible="showEditFeaturePanel"
    header="Object bewerken"
    :dismissable="false"
    :pt="{
      mask: '!tw-bg-black/0',
    }"
    @update:visible="toggleShowCancelModal"
  >
    <div class="tw-flex tw-flex-col tw-gap-4">
      <Message v-if="geoServerError" :pt="{ text: '!tw-break-all' }" severity="error">{{ geoServerError }}</Message>
      <label class="form__label" for="edit-layer-panel-choose-layer">Objectgegevens</label>
      <vee-form
        ref="form"
        v-slot="{ errors }"
        class="tw-flex tw-flex-col tw-gap-2 tw-py-2"
        :initial-values="featureValues"
        @submit="handleSubmit"
      >
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

    <template #footer>
      <div class="tw-flex tw-items-center tw-gap-2 tw-p-4">
        <Button
          label="Verwijderen"
          icon="pi pi-times"
          class="tw-flex-auto"
          outlined
          severity="danger"
          @click="toggleShowCancelModal"
        ></Button>
        <Button label="Opslaan" icon="pi pi-save" class="tw-flex-auto" @click="submitFormManually"></Button>
      </div>
    </template>
  </Drawer>

  <SaveModal
    message="Wanneer u doorgaat met opslaan, wordt het door u bewerkte object, inclusief alle bijbehorende eigenschappen,
      opgeslagen."
    :visible="showSaveModal"
    :on-cancel="cancelSaveModal"
    :on-save="save"
  />

  <CancelModal
    message="Wanneer u annuleert, gaan alle onopgeslagen wijzigingen verloren."
    :visible="showCancelModal"
    :on-cancel="cancelCancelModal"
    :on-proceed="proceed"
  />
</template>

<script setup lang="ts">
import { useEditLayerStore } from "@/stores/edit_layer_store";
import { ref, unref, watch } from "vue";
import { IFeatureProperties, ILayerProperties } from "@/types/layer";
import { IUser } from "@/types/user";
import { useToast } from "primevue";
import { EEditLayerMode } from "@/types/map";
import { defineRule, Field as VeeField, Form as VeeForm } from "vee-validate";
import { required } from "@vee-validate/rules";
import { editFeatureOnLayer, getGeometryName, getWfsOrWFSWMSLayerFeatureInformation } from "@/services/layer";
import SaveModal from "@/components/modals/SaveModal.vue";
import CancelModal from "@/components/modals/CancelModal.vue";
import Feature from "ol/Feature";

interface AddFeaturePanelProps {
  user: IUser;
  refreshLayer: (id: string) => void;
}

// Props
const { user, refreshLayer } = defineProps<AddFeaturePanelProps>();

// Toast
const toast = useToast();

// Store
const editLayerStore = useEditLayerStore();

// References
const showEditFeaturePanel = ref<boolean>(false);
const showSaveModal = ref<boolean>(false);
const showCancelModal = ref<boolean>(false);
const drawerError = ref<string | null>(null);
const geoServerError = ref<string | null>(null);
const layerProperties = ref<ILayerProperties>([]);
const featureValues = ref<{ [key: string]: any }>({});
const geometryNameRef = ref<string>("geometry");
const featureProperties = ref<IFeatureProperties>({
  targetNamespace: "",
  targetPrefix: "",
});
const form = ref(null);

watch(
  () => editLayerStore.highlightedFeatureAndLayer?.feature,
  (value) => {
    if (value && !showEditFeaturePanel.value && editLayerStore.editLayerMode === EEditLayerMode.EDIT) {
      showEditFeaturePanel.value = true;
      featureValues.value = value.getProperties();
    }
  },
  { deep: true },
);

watch(
  () => editLayerStore.highlightedFeatureAndLayer?.layer,
  async (highlightedLayer) => {
    if (highlightedLayer) {
      try {
        const { targetPrefix, targetNamespace, featureTypes } = await getWfsOrWFSWMSLayerFeatureInformation(
          highlightedLayer,
          user,
        );

        const geometryName = await getGeometryName(featureTypes);

        layerProperties.value = featureTypes[0].properties
          ? featureTypes[0].properties.filter(
              (properties) => properties.name !== geometryName && properties.name !== "id",
            )
          : [];

        geometryNameRef.value = geometryName;
        featureProperties.value = {
          targetPrefix: targetPrefix,
          targetNamespace: targetNamespace,
        };
        drawerError.value = null;
        geoServerError.value = null;

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
  featureValues.value = values;

  toggleShowEditLayerSaveModal();
};

const submitFormManually = () => {
  if (form.value) {
    (form.value as any).$el.requestSubmit();
  }
};

// Methods
const handleDrawerClose = (value: boolean) => {
  showEditFeaturePanel.value = value;
  geoServerError.value = null;
  // TODO: Don't close on escape, only close modal on escape. This is a known bug in PrimeVue: https://github.com/primefaces/primevue/issues/5138
  editLayerStore.resetFeature();
  editLayerStore.setEditLayerMode(EEditLayerMode.NONE);
  editLayerStore.setSelectedLayer(null);
};

const toggleShowEditLayerSaveModal = () => {
  showSaveModal.value = !showSaveModal.value;
};

const toggleShowCancelModal = () => {
  showCancelModal.value = !showCancelModal.value;
};

const proceed = () => {
  toggleShowCancelModal();

  handleDrawerClose(false);
};

const cancelCancelModal = () => {
  toggleShowCancelModal();
};

const save = () => {
  toggleShowEditLayerSaveModal();

  handleSaveFeature();
};

const cancelSaveModal = () => {
  toggleShowEditLayerSaveModal();
};

const handleSaveFeature = async () => {
  try {
    const feature = editLayerStore.highlightedFeatureAndLayer!.feature as Feature;
    const featureValuesToSubmit = Object.fromEntries(
      Object.entries(unref(featureValues.value)).filter(([key, value]) => value != null),
    );

    feature.setProperties(featureValuesToSubmit);

    await editFeatureOnLayer(
      editLayerStore.highlightedFeatureAndLayer!.layer,
      feature,
      unref(featureProperties),
      unref(geometryNameRef),
    );

    refreshLayer(editLayerStore.highlightedFeatureAndLayer ? editLayerStore.highlightedFeatureAndLayer.layer.id : "");

    toast.add({
      severity: "success",
      summary: "Object bewerken gelukt",
      detail: `Het bewerken van een object op kaartlaag is gelukt`,
      life: 5000,
    });

    handleDrawerClose(false);
  } catch (e) {
    geoServerError.value = (e as Error).message;
  }
};
</script>

<style scoped lang="scss">
.edit-layer-panel__error {
  color: var(--color-alert) !important;
}
</style>
