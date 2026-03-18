<template>
  <div class="tools-panel__button-container">
    <button
      v-tippy="{ placement: 'bottom' }"
      class="tools-panel__button"
      :class="{
        'tools-panel__button--active': showEditFeatureMenu,
      }"
      :disabled="editLayerStore.editableLayers.length < 1"
      content="Laag objecten toevoegen"
      aria-label="Laag objecten toevoegen"
      @click="toggleEditLayerMenu"
    >
      <EditLocationIcon class="icon" />
    </button>

    <div>
      <transition name="fade">
        <div v-if="showEditFeatureMenu" class="tools-panel__draw-bar">
          <div class="tools-panel__draw-menu">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Object toevoegen"
              class="tools-panel__button"
              :class="{
                'tools-panel__button--active': editLayerStore.editLayerMode === EditLayerMode.ADD,
              }"
              content="Object toevoegen"
              @click="() => toggleAddEditFeatureMode()"
            >
              <AddIcon />
            </button>
          </div>
        </div>
      </transition>

      <transition name="fade">
        <div v-if="showEditFeatureMenu" class="tools-panel__draw-bar tools-panel__draw-bar--secondary">
          <div v-for="geometryTool in availableGeometryTools" :key="geometryTool.name" class="tools-panel__draw-menu">
            <EditLayerTool
              v-if="geometryTool.name === editLayerStore.geometryType || editLayerStore.geometryType === 'Geometry'"
              :tool="geometryTool"
              :tool-in-use="tool"
              :set-tool="setTool"
            />
          </div>
        </div>
      </transition>
    </div>
  </div>

  <Dialog
    v-model:visible="showSelectLayerDialog"
    modal
    header="Kies een kaartlaag"
    class="tw-w-[calc(100%-16px)] sm:tw-w-[25rem]"
  >
    <div v-if="editLayerStore.editableLayers.length > 1" class="tw-flex tw-flex-col tw-gap-2 tw-items-start">
      <label class="form__label" for="edit-layer-panel-choose-layer">Selecteer een kaartlaag</label>
      <Select
        :model-value="editLayerStore.selectedLayer"
        :options="
          editLayerStore.editableLayers.filter(
            (layer) =>
              layer.is_visible && layer.can_write && (layer.source_type === 'WMS_WFS' || layer.source_type === 'WFS'),
          )
        "
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
      <div class="tw-flex tw-flex-col tw-items-end tw-w-full">
        <Button label="Kies laag" @click="showSelectLayerDialog = false" />
      </div>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
import EditLocationIcon from "@/assets/icons/edit-location.icon.svg";
import LineIcon from "@/assets/icons/line-icon.svg";
import PolyGonIcon from "@/assets/icons/polygon-icon.svg";
import DotIcon from "@/assets/icons/dot-icon.svg";
import AddIcon from "@/assets/icons/add-icon.svg";
import MultiPointIcon from "@/assets/icons/multipoint-icon.svg";
import { useEditLayerStore } from "@/stores/edit_layer_store";
import { EditLayerMode } from "@/types/map";
import { ref, watch } from "vue";
import { getGeometryName, getWfsOrWFSWMSLayerFeatureInformation } from "@/services/layer";
import { useGlobalStore } from "@/stores";
import EditLayerTool from "@/components/tools/EditLayerTool.vue";

// Props
interface EditLayerMenuProps {
  tool: string;
  showEditFeatureMenu: boolean;
  toggleEditLayer: () => void;
  setTool: (tool: string) => void;
}

const { tool, showEditFeatureMenu, toggleEditLayer, setTool } = defineProps<EditLayerMenuProps>();

// Store
const editLayerStore = useEditLayerStore();
const globalStore = useGlobalStore();

// Select Layer Dialog logic
const showSelectLayerDialog = ref<boolean>(false);

const showDialogOrProceed = () => {
  if (editLayerStore.editableLayers.length > 1) {
    showSelectLayerDialog.value = true;
  }

  // If editableLayers length is only one and a new feature was drawn, you have to set selected layer by your self
  if (editLayerStore.editableLayers.length === 1) {
    editLayerStore.setSelectedLayer(editLayerStore.editableLayers[0]);
  }
};

watch(
  () => editLayerStore.selectedLayer,
  async (selectedLayer) => {
    if (selectedLayer && globalStore.user) {
      const { featureTypes } = await getWfsOrWFSWMSLayerFeatureInformation(selectedLayer, globalStore.user);

      const geometryName = await getGeometryName(featureTypes);
      const geometryType = featureTypes[0].properties.filter(
        (featureProperty) => featureProperty.name === geometryName,
      )[0].localType;

      editLayerStore.setGeometryType(geometryType);

      if (geometryType !== "Geometry") {
        setTool(geometryType);
      }
    }
  },
  { deep: true },
);

// Draw tool logic
const availableGeometryTools = [
  { name: "Point", icon: DotIcon, translation: "Punt", enableUndo: false },
  { name: "LineString", icon: LineIcon, translation: "Lijn", enableUndo: true },
  { name: "Polygon", icon: PolyGonIcon, translation: "Polygoon", enableUndo: true },
  { name: "MultiPoint", icon: MultiPointIcon, translation: "MultiPunt", enableUndo: false },
  { name: "MultiLineString", icon: LineIcon, translation: "MultiLijn", enableUndo: true },
  { name: "MultiPolygon", icon: PolyGonIcon, translation: "MultiPolygoon", enableUndo: true },
];

// Methods
const toggleEditLayerMenu = () => {
  if (editLayerStore.editLayerMode !== EditLayerMode.NONE) {
    editLayerStore.resetEditLayerProperties();
  }

  toggleEditLayer();
};

const toggleAddEditFeatureMode = () => {
  if (editLayerStore.editLayerMode !== EditLayerMode.ADD) {
    editLayerStore.setEditLayerMode(EditLayerMode.ADD);
    editLayerStore.setSelectedLayer(null);
    showDialogOrProceed();
    setTool("");

    return;
  }

  editLayerStore.resetEditLayerProperties();
  setTool("");
};
</script>
