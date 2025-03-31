<template>
  <Drawer
    :visible="showEditFeaturePanel"
    header="Object bewerken"
    :dismissable="false"
    @update:visible="toggleShowCancelModal"
  >
    <div class="tw-flex tw-flex-col tw-gap-0">
      <span class="tw-font-[var(--font-weight-bold)]">Actieve laag</span>
      <p class="tw-mt-0">{{ editLayerStore.highlightedFeatureAndLayer?.layer.name }}</p>
    </div>
    <div class="tw-flex tw-flex-col">
      <Message v-if="geoServerError" class="tw-mb-4" :pt="{ text: '!tw-break-all' }" severity="error">{{
        geoServerError
      }}</Message>
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

  <EditLayerActionModal
    :visible="showSaveModal"
    header="Opslaan"
    :message="`Wanneer u doorgaat met opslaan, worden alle aangepaste eigenschappen overschreven op de laag ${editLayerStore.highlightedFeatureAndLayer?.layer.name}.`"
    cancel-label="Annuleren"
    cancel-icon="pi pi-times"
    confirm-label="Opslaan"
    confirm-icon="pi pi-save"
    :on-cancel="cancelSaveModal"
    :on-confirm="save"
  />

  <EditLayerActionModal
    :visible="showDeleteModal"
    header="Verwijderen"
    :message="`Wanneer u verwijdert, gaan dit object verloren op de laag ${editLayerStore.highlightedFeatureAndLayer?.layer.name}.`"
    cancel-label="Annuleren"
    confirm-label="Verwijderen"
    confirm-icon="pi pi-times"
    :on-cancel="cancelDeleteModal"
    :on-confirm="onDelete"
  />

  <EditLayerActionModal
    :visible="showCancelModal"
    header="Annuleren"
    :message="`Wanneer u annuleert, gaan alle onopgeslagen wijzigingen verloren op de laag ${editLayerStore.highlightedFeatureAndLayer?.layer.name}.`"
    cancel-label="Verder met bewerken"
    confirm-label="Bewerken sluiten"
    confirm-icon="pi pi-times"
    :on-cancel="cancelCancelModal"
    :on-confirm="proceed"
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
import Feature from "ol/Feature";
import LayerCrudForm from "@/components/edit-layers/LayerCrudForm.vue";
import EditLayerActionModal from "@/components/edit-layers/EditLayerActionModal.vue";

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
        drawerError.value = "Er is iets fout gegaan bij het ophalen van de data";

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
  editLayerStore.resetEditLayerProperties();
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
    geoServerError.value = "Er is iets fout gegaan bij het verwijderen";
    console.error((e as Error).message);
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
    geoServerError.value = "Er is iets fout gegaan bij het opslaan";
    console.error((e as Error).message);
  }
};
</script>
