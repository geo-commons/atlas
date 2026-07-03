<template>
  <div v-if="data" class="map-update" :class="{ environmentIndicator: showEnvironmentIndicator }">
    <MapLayers
      v-if="sidebar === 'layers'"
      :initial-data="data"
      @show-form="() => showSidebar('form')"
      @show-layer="showLayerSettings"
      @update-layer-config="updateLayerConfig"
    />
    <MapLayer
      v-if="sidebar === 'layer'"
      :initial-data="selectedLayerData"
      :initial-configured-layers="data.layers"
      @show-layers="() => showSidebar('layers')"
      @update-base-layer-status="handleBaseLayerStatusUpdate"
    />
    <MapAbout
      v-if="sidebar === 'about'"
      :initial-data="data"
      @show-form="() => showSidebar('form')"
      @update-about="handleAboutUpdate"
    />
    <LayerListPanel v-if="sidebar === 'layerList'" :initial-data="data" @show-form="() => showSidebar('form')" />
    <ListPanelAdmin
      v-if="sidebar === 'list'"
      :initial-data="data"
      :layers="configuredLayers"
      @show-form="() => showSidebar('form')"
    />
    <FiltersPanelAdmin
      v-if="sidebar === 'filters'"
      :initial-data="data"
      :layers="configuredLayers"
      :user="user"
      @show-form="() => showSidebar('form')"
    />
    <ThumbnailPanelAdmin
      v-if="sidebar === 'thumbnail'"
      :initial-thumbnail="data.thumbnail"
      @show-form="() => showSidebar('form')"
      @update-map="getMap"
    />
    <MapForm
      v-if="sidebar === 'form'"
      :initial-data="data"
      :errors="errors"
      @delete="deleteMap"
      @submit="saveMap"
      @show-panel="showSidebar"
    />
    <div class="editor-map-wrapper">
      <map-renderer
        ref="map"
        :initial-position="mapPosition"
        :initial-layers="configuredRenderLayers"
        :layer-tree="configuredLayerTree"
        :user="user"
        :features="data.features"
        :settings="data.settings"
        :config="config"
        :map-id="data.is_main ? 'primary' : data.slug || 'primary'"
        :admin-map="true"
        :hide-reset-button="true"
        :about="data.about"
        :about-title="data.about_title"
        :thumbnail="data.thumbnail"
      />
    </div>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import { mapState } from "pinia";

import MapForm from "../components/MapForm";
import MapLayers from "../components/MapLayers";
import ListPanelAdmin from "../components/ListPanelAdmin";
import FiltersPanelAdmin from "../components/FiltersPanelAdmin";
import MapLayer from "@/admin/components/MapLayer.vue";
import LayerListPanel from "../components/LayerListPanel.vue";
import MapAbout from "../components/MapAbout.vue";
import { useGlobalStore } from "@/stores";
import ThumbnailPanelAdmin from "@/admin/components/ThumbnailPanelAdmin.vue";
import { useToast } from "primevue";
import MapRenderer from "@/components/MapRenderer/MapRenderer.vue";
import { useQueryCache } from "@pinia/colada";
import { buildCategoryTree, flattenCategoryTreeLayers } from "@/utils/map-layer-tree";

export default {
  name: "MapCreateUpdate",
  components: {
    MapRenderer,
    ThumbnailPanelAdmin,
    MapLayer,
    MapForm,
    MapLayers,
    ListPanelAdmin,
    FiltersPanelAdmin,
    LayerListPanel,
    MapAbout,
  },
  setup() {
    const queryCache = useQueryCache();
    return { queryCache };
  },
  data() {
    return {
      data: null,
      toast: useToast(),
      mapPadding: [0, 0, 0, 0],
      selectedArea: null,
      sidebar: "form",
      selectedLayerData: null,
      userLayerSettings: null,
      errors: null,
    };
  },
  computed: {
    ...mapState(useGlobalStore, ["position", "layers", "config", "map", "user"]),
    mapPosition() {
      const normalizedPosition = this.normalizePosition(this.data?.settings?.position);

      if (!normalizedPosition) {
        return this.position;
      }

      return {
        ...this.position,
        zoom: normalizedPosition.zoom,
        center: [normalizedPosition.center.x, normalizedPosition.center.y],
        marker: null,
        geolocation: null,
        animate: true,
        animateFast: true,
      };
    },
    showEnvironmentIndicator() {
      return this.config.application_environment !== "production";
    },
    baseLayers() {
      return this.layers.filter((layer) => layer.is_base);
    },
    configuredLayers() {
      if (this.data.layers) {
        return this.configuredLegacyLayers(this.data.layers);
      }

      return this.layers;
    },
    configuredLayerTree() {
      const orderingByLayerId = new Map((this.data.layers || []).map((layer) => [layer.layer, layer.ordering]));
      return buildCategoryTree(
        this.configuredLayers.filter((layer) => !layer.is_base),
        this.getCategoriesFromLayers(),
        this.data.categories || [],
        orderingByLayerId,
      );
    },
    configuredRenderLayers() {
      return [...this.configuredBaseLayers(), ...flattenCategoryTreeLayers(this.configuredLayerTree)];
    },
  },
  watch: {
    "data.features.filters"(newValue) {
      if (!newValue && this.$refs.map && this.$refs.map.showFilters) {
        this.$refs.map.toggleFilters();
      }
    },
    "data.features.list"(newValue) {
      if (!newValue && this.$refs.map && this.$refs.map.showList) {
        this.$refs.map.toggleList();
      }
    },
    "data.features.showAbout"(newValue) {
      if (this.$refs.map) {
        this.$refs.map.showAbout = newValue || false;
      }
    },
  },
  created() {
    this.getMap();
  },
  methods: {
    async getMap() {
      if (this.$route.params.id) {
        const result = await fetch(`/atlas/api/v1/maps/${this.$route.params.id}/`, {
          credentials: "same-origin",
          headers: { "Content-Type": "application/json" },
        });

        if (!result.ok) {
          console.error("Could not fetch maps");
        }

        this.data = await result.json();
        this.ensureMapPositionSettings();
        this.checkBaseLayersConfigured();
        return;
      }

      this.data = {
        features: {},
        layers: [],
        categories: [],
        settings: {
          position: this.getDefaultPosition(),
          facets: [],
          filterLayerId: null,
          listLayerId: null,
        },
      };
    },
    getConfiguredLayer(selectedLayer) {
      const layer = this.layers.find((candidate) => candidate.internal_id === selectedLayer.layer);

      if (!layer) {
        return null;
      }

      if (!selectedLayer.settings?.customSettings) {
        return { ...layer };
      }

      return {
        ...layer,
        is_visible: selectedLayer.settings.is_visible,
        is_base: selectedLayer.settings.is_base,
        is_filterable_in_legend: selectedLayer.settings.is_filterable_in_legend,
        opacity: selectedLayer.settings.opacity,
        zoom_min: selectedLayer.settings.zoom_min,
        zoom_max: selectedLayer.settings.zoom_max,
        display_properties: selectedLayer.settings.display_properties,
        search_fields: selectedLayer.settings.search_fields,
        server_style: selectedLayer.settings.server_style,
        client_style: selectedLayer.settings.client_style,
        friendly_fields: selectedLayer.settings.friendly_fields,
        templated_properties: selectedLayer.settings.templated_properties,
        linked_data: selectedLayer.settings.linked_data,
        templates: selectedLayer.settings.templates,
      };
    },
    configuredLegacyLayers(selectedLayers) {
      return selectedLayers.map(this.getConfiguredLayer).filter(Boolean);
    },
    configuredBaseLayers() {
      return this.configuredLegacyLayers(this.data.layers || []).filter((layer) => layer.is_base);
    },
    getCategoriesFromLayers() {
      const categoriesById = new Map();

      this.layers.forEach((layer) => {
        if (!layer.category) {
          return;
        }

        categoriesById.set(layer.category.id, layer.category);

        if (layer.category.parent) {
          categoriesById.set(layer.category.parent.id, layer.category.parent);
        }
      });

      return [...categoriesById.values()];
    },
    async saveMap(data, continueEditing = false) {
      let result;
      this.errors = null;

      data.settings = data.settings || {};
      data.settings.position = this.normalizePosition(data.settings.position) || this.getDefaultPosition();

      if (data.is_main) {
        data.published = true;
        data.show_in_overview = false;
      }

      if (!data.features.list) {
        data.settings.listLayerId = null;
      }

      if (!data.features.filters) {
        data.settings.filterLayerId = null;
        data.settings.facets = [];
      }

      if (data.thumbnail) {
        // Remove thumbnail from data object to make sure it is not posted with
        // the rest of the map data since a file is not stringify-able.
        delete data.thumbnail;
      }

      if (this.$route.params.id) {
        result = await fetch(`/atlas/api/v1/maps/${this.$route.params.id}/`, {
          method: "PATCH",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get("csrftoken"),
          },
          body: JSON.stringify(data),
        });
      } else {
        result = await fetch(`/atlas/api/v1/maps/`, {
          method: "POST",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get("csrftoken"),
          },
          body: JSON.stringify(data),
        });
      }

      if (result.ok) {
        await this.queryCache.invalidateQueries(["maps"]);

        this.toast.add({
          severity: "success",
          summary: "Kaart succesvol opgeslagen",
          detail: "Alle instellingen zijn succesvol opgeslagen",
          life: 5000,
        });

        if (!continueEditing) {
          this.$router.push(data.is_main ? "/" : "/maps");
        }
      } else {
        this.errors = await result.json();

        this.toast.add({
          severity: "error",
          summary: "Er is iets misgegaan",
          detail: "Het opslaan is niet gelukt, probeer het later opnieuw",
          life: 5000,
        });
      }
    },
    async deleteMap(e) {
      e.preventDefault();

      const acknowledged = confirm("Weet je zeker dat je de kaart wilt verwijderen?");
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/maps/${this.$route.params.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.$router.push(`/maps`);
      }
    },
    checkBaseLayersConfigured() {
      let hasBase = this.data.layers.some((layer) => {
        if (layer.settings.customSettings && layer.settings.is_base) {
          return true;
        }

        const defaultLayerSettings = this.layers.find((l) => l.internal_id === layer.layer);

        return defaultLayerSettings.is_base;
      });

      if (!hasBase) {
        const baseLayer = this.baseLayers[0];

        this.data.layers.push({
          layer: baseLayer.internal_id,
          settings: {
            customSettings: false,
          },
        });
      }
    },
    ensureMapPositionSettings() {
      if (!this.data.settings) {
        this.data.settings = {};
      }

      if (!this.data.settings.position) {
        this.data.settings.position = this.getDefaultPosition();
      }
    },
    normalizePosition(position) {
      const zoom = Number(position?.zoom);
      const centerX = Number(position?.center?.x);
      const centerY = Number(position?.center?.y);

      if (![zoom, centerX, centerY].every(Number.isFinite)) {
        return null;
      }

      return {
        zoom,
        center: {
          x: centerX,
          y: centerY,
        },
      };
    },
    getDefaultPosition() {
      return {
        zoom: this.config.position.zoom,
        center: {
          x: this.config.position.center.x,
          y: this.config.position.center.y,
        },
      };
    },
    showSidebar(sidebar) {
      this.sidebar = sidebar;
    },
    showLayerSettings(selectedLayerId) {
      this.selectedLayerData = this.data.layers.find((layer) => layer.layer === selectedLayerId);

      if (!this.selectedLayerData) {
        this.selectedLayerData = {
          layer: selectedLayerId,
          settings: { customSettings: false },
        };
        this.data.layers.push(this.selectedLayerData);
      }

      this.showSidebar("layer");
    },
    updateLayerConfig(config) {
      this.data.layers = [...config.layers];
      this.data.categories = [...config.categories];
    },
    ensureCategoryConfig(category) {
      if (!category || this.data.categories?.some((mapCategory) => mapCategory.category === category.id)) {
        return;
      }

      this.data.categories = [
        ...(this.data.categories || []),
        {
          category: category.id,
          title: category.title,
          ordering: category.ordering ?? this.data.categories?.length ?? 0,
        },
      ];
    },
    removeUnusedCategoryConfigs() {
      const usedCategoryIds = new Set(
        this.configuredLayers.filter((layer) => !layer.is_base && layer.category).map((layer) => layer.category.id),
      );

      this.configuredLayers.forEach((layer) => {
        if (!layer.is_base && layer.category?.parent) {
          usedCategoryIds.add(layer.category.parent.id);
        }
      });

      this.data.categories = (this.data.categories || []).filter((category) => usedCategoryIds.has(category.category));
    },
    handleBaseLayerStatusUpdate(mapLayerConfig) {
      const layer = this.layers.find(
        (candidate) => candidate.internal_id === mapLayerConfig.layer || candidate.id === mapLayerConfig.layer,
      );

      if (!layer) {
        return;
      }

      const isBaseLayer = mapLayerConfig.settings.customSettings ? mapLayerConfig.settings.is_base : layer.is_base;

      if (isBaseLayer) {
        this.removeUnusedCategoryConfigs();
        return;
      }

      if (layer.category?.parent) {
        this.ensureCategoryConfig(layer.category.parent);
      }

      this.ensureCategoryConfig(layer.category);
    },
    handleAboutUpdate(aboutData) {
      this.data.about = aboutData?.about;
      this.data.about_title = aboutData?.about_title;
      this.data.thumbnail = aboutData?.thumbnail;
      this.data.features = { ...this.data.features, ...aboutData.features };
    },
  },
};
</script>

<style lang="scss" scoped>
.map-update {
  display: flex;
  height: 100%;
  flex-direction: row;
}

.map-update.environmentIndicator {
  height: calc(100dvh - 40px);
}

h2 {
  display: flex;
  align-items: center;
  gap: 8px;
}

.editor-map-wrapper {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  padding: 20px var(--padding-screen) var(--padding-screen) var(--padding-screen);
  max-width: 100%;
  overflow-x: auto;
}
</style>
