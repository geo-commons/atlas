<template>
  <Drawer
    :visible="showEditFeaturePanel"
    header="Object bewerken"
    :dismissable="false"
    @update:visible="toggleShowCancelModal"
  >
    <div class="tw-flex tw-flex-col tw-gap-4">
      <Message v-if="geoServerError" :pt="{ text: '!tw-break-all' }" severity="error">{{ geoServerError }}</Message>
      <label class="form__label" for="edit-layer-panel-choose-layer">Objectgegevens</label>
      <LayerCrudForm
        ref="form"
        :layer-properties="layerProperties"
        :handle-submit="handleSubmit"
        :initial-values="featureValues"
      />
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
        <SplitButton label="Opslaan" :model="splitButtonItems" @click="submitFormManually"></SplitButton>
      </div>
    </template>
  </Drawer>

  <EditLayerSaveModal
    :message="`Wanneer u doorgaat met opslaan, worden alle aangepaste eigenschappen overschreven op de laag ${editLayerStore.highlightedFeatureAndLayer?.layer.name}.`"
    :visible="showSaveModal"
    :on-cancel="cancelSaveModal"
    :on-save="save"
  />

  <EditLayerDeleteModal
    :message="`Wanneer u verwijdert, gaan alle onopgeslagen wijzigingen verloren op de laag ${editLayerStore.highlightedFeatureAndLayer?.layer.name}.`"
    :visible="showDeleteModal"
    :on-cancel="cancelDeleteModal"
    :on-delete="onDelete"
  />

  <EditLayerCancelModal
    :message="`Wanneer u annuleert, gaan alle onopgeslagen wijzigingen verloren op de laag ${editLayerStore.highlightedFeatureAndLayer?.layer.name}.`"
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
import { EditLayerMode } from "@/types/map";
import { defineRule } from "vee-validate";
import { required } from "@vee-validate/rules";
import {
  deleteFeatureOnLayer,
  editFeatureOnLayer,
  getGeometryName,
  getWfsOrWFSWMSLayerFeatureInformation,
} from "@/services/layer";
import EditLayerSaveModal from "@/components/edit-layers/EditLayerSaveModal.vue";
import EditLayerCancelModal from "@/components/edit-layers/EditLayerCancelModal.vue";
import Feature from "ol/Feature";
import EditLayerDeleteModal from "@/components/edit-layers/EditLayerDeleteModal.vue";
import LayerCrudForm from "@/components/edit-layers/LayerCrudForm.vue";

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
const showDeleteModal = ref<boolean>(false);
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
    if (value && !showEditFeaturePanel.value && editLayerStore.editLayerMode === EditLayerMode.EDIT) {
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
  { deep: true },
);

// Form logic
const splitButtonItems = [
  {
    label: "Verwijder object",
    command: () => {
      toggleShowDeleteModal();
    },
  },
];

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
  showEditFeaturePanel.value = value;
  geoServerError.value = null;
  // TODO: Drawer is not closing on escape, only modal is now closing on escape. This is a known bug in PrimeVue: https://github.com/primefaces/primevue/issues/5138
  editLayerStore.resetFeature();
  editLayerStore.setEditLayerMode(EditLayerMode.NONE);
  editLayerStore.setSelectedLayer(null);
};

const toggleShowEditLayerSaveModal = () => {
  showSaveModal.value = !showSaveModal.value;
};

const toggleShowCancelModal = () => {
  showCancelModal.value = !showCancelModal.value;
};

const toggleShowDeleteModal = () => {
  showDeleteModal.value = !showDeleteModal.value;
};

const proceed = () => {
  toggleShowCancelModal();

  handleDrawerClose(false);
};

const onDelete = () => {
  toggleShowDeleteModal();

  handleDeleteFeature();
};

const cancelDeleteModal = () => {
  toggleShowDeleteModal();
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

const handleDeleteFeature = async () => {
  try {
    const feature = editLayerStore.highlightedFeatureAndLayer!.feature as Feature;

    await deleteFeatureOnLayer(
      editLayerStore.highlightedFeatureAndLayer!.layer,
      feature,
      unref(featureProperties),
      unref(geometryNameRef),
    );

    refreshLayer(editLayerStore.highlightedFeatureAndLayer ? editLayerStore.highlightedFeatureAndLayer.layer.id : "");

    toast.add({
      severity: "success",
      summary: "Object verwijderen gelukt",
      detail: `Het verwijderen van een object op kaartlaag is gelukt`,
      life: 5000,
    });

    handleDrawerClose(false);
  } catch (e) {
    geoServerError.value = (e as Error).message;
  }
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
