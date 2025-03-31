<template>
  <Drawer
    :visible="showAddFeaturePanel"
    header="Object toevoegen"
    :dismissable="false"
    @update:visible="toggleShowCancelModal"
  >
    <div v-if="editLayerStore.selectedLayer" class="tw-py-4">
      <div v-if="layerTypeIsWFSOrWMSWFS && !drawerError" class="tw-flex tw-flex-col tw-gap-4">
        <Message v-if="geoServerError" :pt="{ text: '!tw-break-all' }" severity="error">{{ geoServerError }}</Message>
        <label class="form__label" for="edit-layer-panel-choose-layer">Objectgegevens</label>
        <LayerCrudForm ref="form" :layer-properties="layerProperties" :handle-submit="handleSubmit" />
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
      <div class="tw-flex tw-items-center tw-gap-2">
        <Button
          label="Annuleren"
          icon="pi pi-times"
          class="tw-flex-auto"
          outlined
          @click="toggleShowCancelModal"
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
    :message="`Wanneer u doorgaat met opslaan, worden alle eigenschappen en uw getekende object opgeslagen op de laag ${editLayerStore.selectedLayer?.name} in GeoServer.`"
    :visible="showSaveModal"
    :on-cancel="cancelSaveModal"
    :on-save="save"
  />

  <EditLayerCancelModal
    :message="`Wanneer u annuleert, wordt het door u getekende object, inclusief alle bijbehorende eigenschappen, niet opgeslagen
      binnen op de laag ${editLayerStore.selectedLayer?.name} in GeoServer. Alle onopgeslagen wijzigingen gaan verloren.`"
    :visible="showCancelModal"
    :on-cancel="cancelCancelModal"
    :on-proceed="proceed"
  />
</template>

<script setup lang="ts">
import { useEditLayerStore } from "@/stores/edit_layer_store";
import { computed, ref, unref, watch } from "vue";
import { ELayerTypes, IFeatureProperties, ILayer, ILayerProperties } from "@/types/layer";
import { addFeatureOnLayer, getGeometryName, getWfsOrWFSWMSLayerFeatureInformation } from "@/services/layer";
import { IUser } from "@/types/user";
import { defineRule, Field as VeeField, Form as VeeForm } from "vee-validate";
import { required } from "@vee-validate/rules";
import Feature from "ol/Feature";
import { useToast } from "primevue";
import { EditLayerMode } from "@/types/map";
import EditLayerSaveModal from "@/components/edit-layers/EditLayerSaveModal.vue";
import EditLayerCancelModal from "@/components/edit-layers/EditLayerCancelModal.vue";
import LayerCrudForm from "@/components/edit-layers/LayerCrudForm.vue";

interface AddFeaturePanelProps {
  layers: Array<ILayer>;
  user: IUser;
  refreshLayer: (id: string) => void;
}

// Props
const { layers, user, refreshLayer } = defineProps<AddFeaturePanelProps>();

// Emits
const emit = defineEmits<{
  (e: "set-selected-area", area: null | string): void;
  (e: "set-tool", tool: string): void;
}>();

// Toast
const toast = useToast();

// Store
const editLayerStore = useEditLayerStore();

// References
const showAddFeaturePanel = ref<boolean>(false);
const showSaveModal = ref<boolean>(false);
const showCancelModal = ref<boolean>(false);
const drawerError = ref<string | null>(null);
const geoServerError = ref<string | null>(null);
const layerProperties = ref<ILayerProperties>([]);
const geometryNameRef = ref<string>("geometry");
const featureValues = ref<{ [key: string]: any }>({});
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
    if (oldValue === null && value !== null && !showAddFeaturePanel.value) {
      showAddFeaturePanel.value = true;
    }
  },
  { deep: true },
);

watch(
  () => editLayerStore.visibleLayers,
  (value) => {
    if (value.length === 1) {
      editLayerStore.setSelectedLayer(value[0]);
    }
  },
  { deep: true, immediate: true },
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

        if (form.value && (form.value as any).form) {
          (form.value as any).form.resetForm();
        }
      } catch (e: unknown) {
        layerProperties.value = [];
        drawerError.value = (e as Error).message;

        console.error((e as Error).message);
      }
    }
  },
  { deep: true, immediate: true },
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
  if (form.value && (form.value as any).form) {
    (form.value as any).form.$el.requestSubmit();
  }
};

// Methods
const handleDrawerClose = (value: boolean) => {
  showAddFeaturePanel.value = value;
  geoServerError.value = null;
  // TODO: Drawer is not closing on escape, only modal is now closing on escape. This is a known bug in PrimeVue: https://github.com/primefaces/primevue/issues/5138
  editLayerStore.resetFeature();
  editLayerStore.setSelectedLayer(null);
  editLayerStore.setEditLayerMode(EditLayerMode.NONE);

  emit("set-selected-area", null);
  emit("set-tool", "");
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
    const feature = editLayerStore.feature as Feature;
    const featureValuesToSubmit = Object.fromEntries(
      Object.entries(unref(featureValues.value)).filter(([key, value]) => value != null),
    );

    feature.setProperties(featureValuesToSubmit);

    await addFeatureOnLayer(editLayerStore.selectedLayer!, feature, unref(featureProperties), unref(geometryNameRef));

    refreshLayer(editLayerStore.selectedLayer ? editLayerStore.selectedLayer.id : "");

    toast.add({
      severity: "success",
      summary: "Object toevoegen gelukt",
      detail: `Het toevoegen van een object op kaartlaag ${editLayerStore.selectedLayer?.name} is gelukt`,
      life: 5000,
    });

    handleDrawerClose(false);
  } catch (e) {
    geoServerError.value = (e as Error).message;
  }
};
</script>
