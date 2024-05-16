<template>
  <div v-if="data" class="map-update">
    <MapLayers
      v-if="sidebar === 'Layers'"
      :initial-data="data"
      @change="updateLayers"
      @show-form="() => showSidebar('Form')"
      @show-layer="showLayerSettings"
    />
    <MapLayer
      v-if="sidebar === 'Layer'"
      :initial-data="selectedLayerData"
      @change="updateLayers"
      @show-layers="() => showSidebar('Layers')"
    />
    <LayerListPanel
      v-if="sidebar === 'LayerList'"
      :initial-data="data"
      @change="updateLayers"
      @show-form="() => showSidebar('Form')"
    />
    <ListPanelAdmin
      v-if="sidebar === 'List'"
      :initial-data="data"
      :layers="visibleLayers"
      @change="updateLayers"
      @show-form="() => showSidebar('Form')"
    />
    <FiltersPanelAdmin
      v-if="sidebar === 'Filters'"
      :initial-data="data"
      :layers="visibleLayers"
      :user="user"
      @change="updateLayers"
      @show-form="() => showSidebar('Form')"
    />
    <MapForm
      v-if="sidebar === 'Form'"
      :initial-data="data"
      @delete="deleteMap"
      @submit="saveMap"
      @show-layers="() => showSidebar('Layers')"
      @show-list="() => showSidebar('List')"
      @show-filters="() => showSidebar('Filters')"
    />
    <MapRenderer
      ref="map"
      class="editor-map"
      :features="data.features"
      :initial-layers="visibleLayers"
      :initial-position="position"
      :settings="data.settings"
      :user="user"
      :admin-map="true"
      @update-user-settings="updateUserSettings"
    />
  </div>
</template>

<script>
import Cookies from "js-cookie";
import { mapState } from "pinia";

import MapRenderer from "../../components/MapRenderer/MapRenderer";
import MapForm from "../components/MapForm";
import MapLayers from "../components/MapLayers";
import ListPanelAdmin from "../components/ListPanelAdmin";
import FiltersPanelAdmin from "../components/FiltersPanelAdmin";
import MapLayer from "@/admin/components/MapLayer.vue";
import LayerListPanel from "../components/LayerListPanel.vue";
import { useGlobalStore } from "@/stores";

export default {
  name: "MapCreateUpdate",
  components: {
    MapLayer,
    MapRenderer,
    MapForm,
    MapLayers,
    ListPanelAdmin,
    FiltersPanelAdmin,
    LayerListPanel,
  },
  data() {
    return {
      data: null,
      mapPadding: [0, 0, 0, 0],
      selectedArea: null,
      user: null,
      sidebar: "Form",
      selectedLayerData: null,
      userLayerSettings: null,
    };
  },
  computed: {
    ...mapState(useGlobalStore, ["position", "layers", "config"]),
    visibleLayers() {
      if (this.data.layers) {
        let configuredLayers;

        // Get base layers.
        configuredLayers = this.layers
          .filter((layer) => layer.is_base && layer.is_visible)
          .map((layer) => {
            return {
              ...layer,
              is_visible: !layer.is_base ? true : layer.is_visible,
            };
          });

        // Get configured layers.
        this.data.layers.forEach((selectedLayer) => {
          const layer = this.layers.find((l) => l.internal_id === selectedLayer.layer);

          if (!selectedLayer.settings.customSettings) {
            configuredLayers.push({ ...layer });
          } else {
            let isVisibleUserSetting;
            let opacityUserSetting;

            // Make sure user settings from the map take precedence over admin config settings.
            if (this.userLayerSettings !== null && layer.id in this.userLayerSettings) {
              const userSettings = this.userLayerSettings[layer.id];
              isVisibleUserSetting = userSettings.is_visible;
              opacityUserSetting = userSettings.opacity;
            }

            configuredLayers.push({
              ...layer,
              is_visible:
                typeof isVisibleUserSetting === "boolean" ? isVisibleUserSetting : selectedLayer.settings.is_visible,
              opacity: opacityUserSetting ? opacityUserSetting : selectedLayer.settings.opacity,
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
      if (!newValue) {
        this.resetSelectedFilter();
      }
    },
    "data.features.list"(newValue) {
      if (!newValue) {
        this.resetSelectedList();
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
    async saveMap(data) {
      let result;

      if (this.$route.params.id) {
        result = await fetch(`/atlas/api/v1/maps/${this.$route.params.id}/`, {
          method: "PUT",
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
        this.$router.push(`/maps`);
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
    showSidebar(sidebar) {
      this.sidebar = sidebar;
    },
    showLayerSettings(selectedLayerId) {
      this.selectedLayerData = this.data.layers.find((layer) => layer.layer === selectedLayerId);
      this.showSidebar("Layer");
    },
    updateLayers(layers) {
      this.data.layers = layers;
    },
    resetSelectedFilter() {
      this.data.settings.filterLayerId = null;
      this.data.settings.facets = [];
    },
    resetSelectedList() {
      this.data.settings.listLayerId = null;
    },
    updateUserSettings(value) {
      this.userLayerSettings = value;
    },
  },
};
</script>

<style scoped>
.map-update {
  display: flex;
  height: 100%;
  flex-direction: row;
}

.editor-map {
  z-index: 0;
}
</style>
