<template>
  <Drawer
    :visible="showEditFeaturePanel"
    header="Object bewerken"
    :dismissable="false"
    :modal="false"
    @update:visible="onCancel"
  >
    <div class="tw-flex tw-flex-col tw-gap-0">
      <span class="tw-font-[var(--font-weight-bold)]">Actieve laag</span>
      <p class="tw-mt-0">{{ editLayerStore.highlightedFeatureAndLayer?.layer.name }}</p>
    </div>
    <Message v-if="!editLayerStore.isRedrawingFeature && hasMultipleVertices" severity="info" class="tw-mb-3">
      Gebruik Alt+klik om punten te verwijderen.
    </Message>
    <Message v-if="editLayerStore.isRedrawingFeature" severity="info" class="tw-mb-3">{{
      isMultipartGeometry
        ? "Teken de geometrie opnieuw en druk op Enter om af te ronden."
        : "Teken de geometrie opnieuw."
    }}</Message>
    <div class="tw-flex tw-flex-col">
      <ErrorAccordion :error="geoServerError" />
      <label class="form__label" for="edit-layer-panel-choose-layer">Objectgegevens</label>
      <LayerCrudForm
        ref="form"
        :layer-properties="layerProperties"
        :handle-submit="handleSubmit"
        :initial-values="featureValues"
      />
    </div>

    <template #footer>
      <div class="tw-flex tw-flex-col tw-items-stretch tw-gap-2">
        <Button label="Annuleren" icon="pi pi-times" class="tw-flex-auto" outlined @click="onCancel"></Button>
        <Button
          v-if="currentGeometryType"
          label="Opnieuw tekenen"
          icon="pi pi-refresh"
          class="tw-flex-auto"
          outlined
          :disabled="editLayerStore.isRedrawingFeature"
          @click="startRedrawingFeature"
        ></Button>
        <Button
          label="Verwijder object"
          severity="danger"
          icon="pi pi-times"
          class="tw-flex-auto"
          outlined
          @click="toggleShowDeleteModal"
        ></Button>
        <Button
          label="Opslaan"
          icon="pi pi-save"
          class="tw-flex-auto"
          :disabled="editLayerStore.isRedrawingFeature"
          @click="submitFormManually"
        ></Button>
      </div>
    </template>
  </Drawer>

  <EditLayerActionModal
    :visible="showDeleteModal"
    header="Verwijderen"
    :message="`Wanneer u verwijdert, gaan dit object verloren op de laag **${editLayerStore.highlightedFeatureAndLayer?.layer.name}**.`"
    cancel-label="Annuleren"
    confirm-label="Verwijderen"
    confirm-icon="pi pi-times"
    :on-cancel="cancelDeleteModal"
    :on-confirm="onDelete"
  />
</template>

<script setup lang="ts">
import { useEditLayerStore } from "@/stores/edit_layer_store";
import { computed, ref, unref, watch } from "vue";
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
import ErrorAccordion from "@/components/ErrorAccordion.vue";

interface AddFeaturePanelProps {
  user: IUser;
  refreshLayer: (id: string) => void;
}

// Props
const { user, refreshLayer } = defineProps<AddFeaturePanelProps>();

const emit = defineEmits<{
  (e: "set-tool", tool: string): void;
}>();

// Toast
const toast = useToast();

// Store
const editLayerStore = useEditLayerStore();

// References
const showEditFeaturePanel = ref<boolean>(false);
const showDeleteModal = ref<boolean>(false);
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

const multipartGeometryTypes = ["MultiPoint", "MultiLineString", "MultiPolygon"];

const geometryTypesWithMultipleVertices = ["LineString", "Polygon", "MultiLineString", "MultiPolygon"];

const currentGeometryType = computed(() =>
  editLayerStore.highlightedFeatureAndLayer?.feature?.getGeometry()?.getType(),
);

const isMultipartGeometry = computed(() => {
  return currentGeometryType.value ? multipartGeometryTypes.includes(currentGeometryType.value) : false;
});

const hasMultipleVertices = computed(() => {
  return currentGeometryType.value ? geometryTypesWithMultipleVertices.includes(currentGeometryType.value) : false;
});

watch(
  () => editLayerStore.highlightedFeatureAndLayer?.feature,
  (value) => {
    if (value && !showEditFeaturePanel.value && editLayerStore.editLayerMode === EditLayerMode.EDIT) {
      editLayerStore.toggleHideOtherPanels();
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
defineRule("required", (value: string) => {
  if (!required(value)) {
    return "Dit veld is verplicht";
  }
  return true;
});

const handleSubmit = (values: any) => {
  featureValues.value = values;

  handleSaveFeature();
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

const toggleShowDeleteModal = () => {
  showDeleteModal.value = !showDeleteModal.value;
};

const onCancel = () => {
  handleDrawerClose(false);
};

const startRedrawingFeature = () => {
  if (!currentGeometryType.value) {
    return;
  }

  editLayerStore.setDraftFeature(null);
  editLayerStore.setIsRedrawingFeature(true);
  geoServerError.value = null;

  emit("set-tool", currentGeometryType.value);
};

const onDelete = () => {
  toggleShowDeleteModal();

  handleDeleteFeature();
};

const cancelDeleteModal = () => {
  toggleShowDeleteModal();
};

const handleDeleteFeature = async () => {
  try {
    const feature = editLayerStore.highlightedFeatureAndLayer!.feature as Feature;

    await deleteFeatureOnLayer(
      editLayerStore.highlightedFeatureAndLayer!.layer,
      feature,
      unref(featureProperties),
      unref(geometryNameRef),
      user,
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
    const error = e instanceof Error ? e.message : String(e);
    geoServerError.value = error;
    console.error(error);
  }
};

const handleSaveFeature = async () => {
  try {
    const feature = editLayerStore.modifiedFeature as Feature;
    const featureValuesToSubmit = Object.fromEntries(
      Object.entries(unref(featureValues.value)).filter(([key, value]) => value != null && key !== "geometry"),
    );

    feature.setProperties(featureValuesToSubmit);

    await editFeatureOnLayer(
      editLayerStore.highlightedFeatureAndLayer!.layer,
      feature,
      unref(featureProperties),
      unref(geometryNameRef),
      unref(layerProperties).map((property) => property.name),
      user,
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
    const error = e instanceof Error ? e.message : String(e);
    geoServerError.value = error;
    console.error(error);
  }
};
</script>
