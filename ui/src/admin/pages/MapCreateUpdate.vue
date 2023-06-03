<template>
  <div v-if="data" class="map-update">
    <div class="sidebar">
      <div class="sidebar-content">
        <MapLayers
          v-if="sidebar === 'Layers'"
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
      </div>
    </div>
    <MapRenderer
      ref="map"
      :features="data.features"
      :initial-layers="visibleLayers"
      :initial-position="position"
      :settings="data.settings"
      :user="user"
    />
  </div>
</template>

<script>
import Cookies from "js-cookie";
import { mapState } from "vuex";

import MapRenderer from "../../components/MapRenderer/MapRenderer";
import MapForm from "../components/MapForm";
import MapLayers from "../components/MapLayers";
import ListPanelAdmin from "../components/ListPanelAdmin";
import FiltersPanelAdmin from "../components/FiltersPanelAdmin";

export default {
  name: "MapCreateUpdate",
  components: {
    MapRenderer,
    MapForm,
    MapLayers,
    ListPanelAdmin,
    FiltersPanelAdmin,
  },
  data() {
    return {
      data: null,
      mapPadding: [0, 0, 0, 0],
      selectedArea: null,
      user: null,
      sidebar: "Form",
    };
  },
  computed: {
    ...mapState({
      position: (state) => state.position,
      layers: (state) => state.layers,
      config: (state) => state.config,
    }),
    visibleLayers() {
      if (this.data.layers) {
        return this.layers
          .filter(
            (layer) =>
              this.data.layers.includes(layer.internal_id) ||
              (layer.is_base && layer.is_visible)
          )
          .map((layer) => {
            return {
              ...layer,
              is_visible: !layer.is_base ? true : layer.is_visible,
            };
          });
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
        const result = await fetch(
          `/atlas/api/v1/maps/${this.$route.params.id}/`,
          {
            credentials: "same-origin",
            headers: { "Content-Type": "application/json" },
          }
        );

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

      const acknowledged = confirm(
        "Weet je zeker dat je de kaart wil verwijderen?"
      );
      if (!acknowledged) {
        return;
      }

      const result = await fetch(
        `/atlas/api/v1/maps/${this.$route.params.id}/`,
        {
          method: "DELETE",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get("csrftoken"),
          },
        }
      );

      if (result.ok) {
        this.$router.push(`/maps`);
      }
    },
    showSidebar(sidebar) {
      this.sidebar = sidebar;
    },
    updateLayers(layerIds) {
      this.data.layers = layerIds;
    },
    resetSelectedFilter() {
      this.data.settings.filterLayerId = null;
      this.data.settings.facets = [];
    },
    resetSelectedList() {
      this.data.settings.listLayerId = null;
    },
    updateConfig(config) {
      this.data.config = config;
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

.sidebar-content {
  max-height: 100%;
  overflow-y: auto;
  padding: 16px var(--padding-screen) 80px;
}

.button.__alert {
  margin: 32px auto 0;
}
</style>
