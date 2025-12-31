<template>
  <SidePanel
    initial-size-medium
    :initial-size-large="resetSidePanel"
    :show-panel="showPanel"
    class="point-info-panel"
    @expand-side-panel="toggleSidePanelSize"
  >
    <template #search>
      <div class="info-panel-header">
        <div class="search-query">
          <h1 v-if="searchQuery.title">{{ searchQuery.title }}</h1>
          <div class="coordinate-wrapper">
            <h1 v-if="!searchQuery.title">{{ searchQuery.coordinates }}</h1>
            <h4 v-else>{{ searchQuery.coordinates }}</h4>
            <tippy
              placement="bottom-start"
              theme="popover"
              trigger="click"
              :distance="8"
              :delay="[0, 0]"
              :a11y="null"
              :interactive="true"
            >
              <button
                v-tippy
                class="iconbutton __round show-on-hover"
                content="Toon EPSG:4326 projectie"
                aria-label="Toon EPSG:4326 projectie"
              >
                <marker-icon class="icon __small __marker" />
              </button>
              <template #content>
                <div class="container">
                  <div class="heading">
                    <h3 class="title">EPSG:4326 projectie (WGS 84)</h3>
                  </div>
                  <div class="property">
                    {{ searchQuery.coordEPSG4326 }}
                  </div>
                </div>
              </template>
            </tippy>
            <button
              v-tippy="{ hideOnClick: false }"
              class="iconbutton __round show-on-hover"
              :content="copyButtonText"
              aria-label="Kopieer coördinaten"
              @click="copyCoordinates"
            >
              <i class="pi pi-copy"></i>
            </button>
          </div>
        </div>
        <button
          v-tippy="{ placement: 'right' }"
          class="iconbutton __normal __outline"
          type="button"
          content="Sluit paneel"
          aria-label="Sluit paneel"
          @click="closeInfoPanel"
        >
          <close-icon class="icon" />
        </button>
      </div>
    </template>

    <template #default>
      <div>
        <RelatedTableDetails
          v-if="selectedRelatedTableAttributes"
          :selected-related-table-attributes="selectedRelatedTableAttributes"
          @back="back"
          @select-related-table-object="onSelectRelatedTableObject"
          @close-related-table-details="closeRelatedTableDetails"
        />
        <FeatureInfo
          v-for="visibleLayer in visibleLayers"
          v-show="!selectedFeatureDetails && !selectedRelatedTableAttributes"
          :key="visibleLayer.id"
          :is-open="true"
          :layer="visibleLayer"
          :position="position"
          :config="config"
          :atlas-features="features"
          @show-selected-feature="onFeatureSelect"
          @set-position="setPosition"
          @on-fit="onFit"
          @select-feature="selectFeature"
          @select-related-table-object="onSelectRelatedTableObject"
        />
      </div>
    </template>
  </SidePanel>
</template>

<script>
import SidePanel from "./SidePanel";
import FeatureInfo from "./FeatureInfo";
import GeoJSON from "ol/format/GeoJSON";
import { getFeatureCenterCoordinates } from "@/utils/geometry-helpers";
import CloseIcon from "@/assets/icons/close-icon.svg";
import MarkerIcon from "@/assets/icons/marker-icon.svg";
import { Tippy } from "vue-tippy";
import { useGlobalStore } from "@/stores";
import { mapStores } from "pinia";
import { useMapStore } from "@/stores/map_store";
import RelatedTableDetails from "@/components/related-tables/RelatedTableDetails.vue";

export default {
  name: "PointInfoPanel",
  components: {
    RelatedTableDetails,
    Tippy,
    MarkerIcon,
    CloseIcon,
    SidePanel,
    FeatureInfo,
  },
  props: {
    position: Object,
    config: Object,
    features: Object,
    layers: Array,
    showPanel: Boolean,
    mapId: String,
  },
  emits: ["expanded-info-panel", "set-position", "on-fit", "select-feature"],
  data() {
    return {
      resetSidePanel: null,
      selectedFeatureDetails: null,
      selectedRelatedTableAttributes: null,
      copyButtonText: "Kopieer coördinaten",
      mapStore: null,
      history: [],
    };
  },
  computed: {
    ...mapStores(useGlobalStore),
    visibleLayers() {
      return this.mapStore ? this.mapStore.visibleLayersForDetailPanel : [];
    },
    searchQuery: {
      get() {
        return this.globalStore.searchQuery;
      },
      set(value) {
        this.globalStore.setSearchQuery({ title: value, coordinates: null });
      },
    },
  },
  watch: {
    searchQuery(newValue, oldValue) {
      // When user selects a different point on the map we need to reset the selected feature details and the related table details.
      if (newValue.coordinates !== oldValue.coordinates) {
        this.selectedFeatureDetails = null;
        this.closeRelatedTableDetails();
      }
    },
  },
  mounted() {
    this.mapStore = useMapStore(this.mapId);
  },
  methods: {
    closeInfoPanel() {
      this.searchQuery = "";
      this.resetSidePanel = false;
      this.selectedFeatureDetails = null;
      this.$emit("set-position", { ...this.position, marker: null });
    },
    onFeatureSelect(feature) {
      const geometry = new GeoJSON().readFeature(feature).getGeometry();
      const geometryExtend = geometry.getExtent();
      const center = getFeatureCenterCoordinates(feature);

      this.$emit(
        "set-position",
        {
          ...this.position,
          marker: center,
          zoom: 19,
        },
        false,
        false,
      );

      this.$emit("on-fit", geometryExtend);
    },
    onFit(value) {
      this.$emit("on-fit", value);
    },
    setPosition(value) {
      this.$emit("set-position", value);
    },
    toggleSidePanelSize(value) {
      this.resetSidePanel = value;
      this.$emit("expanded-info-panel", value);
    },
    onSelectFeatureDetails(selectedFeature) {
      this.selectedFeatureDetails = selectedFeature;
    },
    onSelectRelatedTableObject(attributes) {
      if (attributes) {
        this.history.push(attributes);
        this.selectedRelatedTableAttributes = attributes;
      }
    },
    closeFeatureInfoDetails() {
      this.selectedFeatureDetails = null;
    },
    closeRelatedTableDetails() {
      this.selectedRelatedTableAttributes = null;
      this.history = [];
    },
    back() {
      let lastHistoryItem = null;

      while (this.history.length > 0) {
        lastHistoryItem = this.history.pop();

        // stop and move to lastHistoryItem when it is a different object than the current active selectedRelatedTableAttributes
        if (lastHistoryItem !== this.selectedRelatedTableAttributes) {
          this.selectedRelatedTableAttributes = lastHistoryItem;
          return;
        }
      }

      // if no history item was found, reset the history and selected related table attributes
      this.selectedRelatedTableAttributes = null;
      this.history = [];
    },
    copyCoordinates() {
      navigator.clipboard
        .writeText(this.searchQuery.coordinates)
        .then(() => {
          this.copyButtonText = "Gekopieerd";
          setTimeout(() => {
            this.copyButtonText = "Kopieer coördinaten";
          }, 2000);
        })
        .catch((err) => {
          console.error("Failed to copy coordinates:", err);
        });
    },
    selectFeature(geometry) {
      this.$emit("select-feature", geometry);
    },
  },
};
</script>

<style scoped>
h1 {
  font-size: var(--font-size-normal);
  margin-bottom: 2px;
  margin-top: 0;
}

h4 {
  margin: 0;
  font-weight: var(--font-weight-normal);
}

.point-info-panel :deep(.header) {
  border-bottom: 1px solid var(--color-grey-60);
  padding: var(--padding-screen);
}

.search-query {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  flex-grow: 1;
}

.coordinate-wrapper {
  display: flex;
  font-size: var(--font-size-small);
  align-items: center;
  gap: 4px;
}

.info-panel-header {
  display: flex;
  justify-content: space-between;
  width: 100%;
  gap: 4px;
}

@media (min-width: 576px) {
  .info-panel-header {
    margin-top: 0;
  }
}

.show-on-hover {
  display: none;
}

.search-query:hover .show-on-hover {
  display: flex;
}

.container {
  font-weight: normal;
  text-align: left;
}

.heading {
  padding: 8px;
  text-align: center;
  border-bottom: 1px solid var(--color-grey-60);
}

.title {
  margin: 0;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-normal);
}

.property {
  padding: 8px;
  display: flex;
  flex-direction: column;
  font-weight: var(--font-weight-normal);
}
</style>
