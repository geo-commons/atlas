<template>
  <div v-if="data" class="map-update" :class="{ environmentIndicator: showEnvironmentIndicator }">
    <MapLayers
      v-if="sidebar === 'layers'"
      :initial-data="data"
      @show-form="() => showSidebar('form')"
      @show-layer="showLayerSettings"
      @update-layers="updateLayers"
      @update-categories="updateCategories"
    />
    <MapLayer
      v-if="sidebar === 'layer'"
      :initial-data="selectedLayerData"
      :initial-configured-layers="data.layers"
      @show-layers="() => showSidebar('layers')"
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
        :initial-position="position"
        :initial-layers="configuredLayers"
        :user="user"
        :features="data.features"
        :settings="data.settings"
        :config="config"
        :map-id="data.slug || 'primary'"
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
    showEnvironmentIndicator() {
      return this.config.application_environment !== "production";
    },
    baseLayers() {
      return this.layers.filter((layer) => layer.is_base);
    },
    configuredLayers() {
      if (this.data.layers) {
        const mapCategoryOrderingById = new Map(
          (this.data.categories || []).map((mapCategory) => [mapCategory.id, mapCategory.ordering ?? 0]),
        );
        const mapCategoryOrderingByCategoryId = new Map(
          (this.data.categories || []).map((mapCategory) => [mapCategory.category, mapCategory.ordering ?? 0]),
        );
        const availableLayerByInternalId = new Map(this.layers.map((layer) => [layer.internal_id, layer]));

        const sortedSelectedLayers = [...this.data.layers].sort((a, b) => {
          const layerA = availableLayerByInternalId.get(a.layer);
          const layerB = availableLayerByInternalId.get(b.layer);

          const categoryOrderA =
            mapCategoryOrderingById.get(a.map_category) ??
            mapCategoryOrderingByCategoryId.get(layerA?.category?.id) ??
            Number.MAX_SAFE_INTEGER;
          const categoryOrderB =
            mapCategoryOrderingById.get(b.map_category) ??
            mapCategoryOrderingByCategoryId.get(layerB?.category?.id) ??
            Number.MAX_SAFE_INTEGER;
          if (categoryOrderA !== categoryOrderB) {
            return categoryOrderA - categoryOrderB;
          }

          const layerOrderA = a.ordering ?? Number.MAX_SAFE_INTEGER;
          const layerOrderB = b.ordering ?? Number.MAX_SAFE_INTEGER;
          if (layerOrderA !== layerOrderB) {
            return layerOrderA - layerOrderB;
          }

          return 0;
        });

        const configuredLayers = [];

        // Get configured layers.
        sortedSelectedLayers.forEach((selectedLayer) => {
          const layer = this.layers.find((l) => l.internal_id === selectedLayer.layer);

          if (!layer) {
            return;
          }

          // Push default layer settings if current layer has no custom settings.
          if (!selectedLayer.settings?.customSettings) {
            configuredLayers.push({ ...layer });
          } else {
            configuredLayers.push({
              ...layer,
              is_visible: selectedLayer.settings.is_visible,
              is_base: selectedLayer.settings.is_base,
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
            });
          }
        });

        return configuredLayers;
      }

      return this.layers;
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
        this.checkBaseLayersConfigured();
        return;
      }

      this.data = {
        features: {},
        settings: {
          facets: [],
          filterLayerId: null,
          listLayerId: null,
        },
      };
    },
    async saveMap(data, continueEditing = false) {
      let result;
      this.errors = null;

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
          this.$router.push(`/maps`);
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
    showSidebar(sidebar) {
      this.sidebar = sidebar;
    },
    showLayerSettings(selectedLayerId) {
      this.selectedLayerData = this.data.layers.find((layer) => layer.layer === selectedLayerId);
      this.showSidebar("layer");
    },
    updateLayers(layers) {
      this.data.layers = [...layers];
    },
    updateCategories(categories) {
      this.data.categories = [...categories];
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
