<template>
  <div class="content">
    <div class="header">
      <button
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton __normal __outline"
        type="button"
        aria-label="Ga terug"
        content="Terug"
        @click="() => $emit('show-form')"
      >
        <svg
          width="24px"
          height="24px"
          viewBox="0 0 24 24"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
        >
          <title>arrow_back_black_24dp</title>
          <g
            id="Admin"
            stroke="none"
            stroke-width="1"
            fill="none"
            fill-rule="evenodd"
          >
            <g
              id="Kaart---Zoekbalk"
              transform="translate(-24.000000, -24.000000)"
            >
              <g
                id="arrow_back_black_24dp"
                transform="translate(16.000000, 16.000000)"
              >
                <g transform="translate(8.000000, 8.000000)">
                  <polygon id="Path" points="0 0 24 0 24 24 0 24"></polygon>
                  <polygon
                    id="Path"
                    fill="#000000"
                    fill-rule="nonzero"
                    points="20 11 7.83 11 13.42 5.41 12 4 4 12 12 20 13.41 18.59 7.83 13 20 13"
                  ></polygon>
                </g>
              </g>
            </g>
          </g>
        </svg>
      </button>
      <h1>Filters</h1>
      <div class="header-spacer" />
    </div>

    <div class="select-wrapper">
      <select
        v-model="selectedLayerTitle"
        class="layer-select edit-field-border"
        @change="onLayerChange"
      >
        <option disabled value="">Selecteer een laag</option>
        <option v-for="l in availableLayers" :key="l.id" :value="l.id">
          {{ l.title }}
        </option>
      </select>
    </div>

    <div class="filters">
      <p v-if="!selectedLayerTitle">
        Kies eerst een laag voordat je de filters instelt.
      </p>

      <div v-if="selectedLayerTitle">
        <div v-for="facet in availableFacets" :key="facet" class="facet">
          <input
            :id="`facet-${facet}`"
            type="checkbox"
            :name="`facet-${facet}`"
            :value="facet"
            :checked="
              data.settings.facets && data.settings.facets.includes(facet)
            "
            @change="onChangeFacet"
          />
          <label :for="`facet-${facet}`">{{ facet }}</label>
        </div>
      </div>
    </div>
  </div>
</template>

<!-- Todo: check if shared code can be moved to base/abstract class together with ListPanelAdmin. -->
<script>
export default {
  name: "FiltersAdmin",
  props: {
    initialData: Object,
    layers: [],
    user: Object,
  },
  data() {
    return {
      data: this.initialData,
      selectedFacets: [],
      availableFacets: [],
      selectedLayerTitle: "",
      selectedLayer: {},
    };
  },
  computed: {
    availableLayers() {
      return this.layers.filter((layer) => {
        return layer.source_type === "WMS_WFS";
      });
    },
  },
  mounted() {
    if (this.data.settings.filterLayerId) {
      this.selectedLayer = this.getLayerById(this.data.settings.filterLayerId);
      this.selectedLayerTitle = this.selectedLayer.id;
    }

    if (this.selectedLayerTitle) {
      this.fetchFeatureType();
    }

    if (!this.data.settings.facets) {
      this.data.settings.facets = [];
    }
  },
  methods: {
    onLayerChange(e) {
      this.data.settings.facets = [];
      const layerId = e.target.value;
      this.data.settings.filterLayerId = layerId;
      this.selectedLayer = this.getLayerById(layerId);
      this.fetchFeatureType();
    },
    getLayerById(id) {
      return this.layers.find((layer) => {
        return layer.id === id;
      });
    },
    async fetchFeatureType() {
      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "1.0.0"],
        ["request", "DescribeFeatureType"],
        ["typename", this.selectedLayer.name],
        ["outputFormat", "application/json"],
      ]);

      try {
        const url = new URL(this.selectedLayer.url);
        url.search = params.toString();
        const result = await fetch(url.toString(), this.getFetchParameters());

        const data = await result.json();
        const featureType = data.featureTypes[0];

        this.availableFacets = featureType.properties
          .filter((ft) => ft.type == "xsd:string")
          .map((ft) => ft.name);
      } catch (e) {
        console.error(e);
      }
    },
    getFetchParameters() {
      if (
        this.selectedLayer.source &&
        this.selectedLayer.source.authenticate &&
        this.user &&
        this.user.token
      ) {
        return {
          headers: { Authorization: `Bearer ${this.user.token}` },
        };
      }

      return {};
    },
    onChangeFacet(e) {
      const changeFacet = e.target.value;

      if (this.data.settings.facets.includes(changeFacet)) {
        const facetIndex = this.data.settings.facets.indexOf(changeFacet);
        this.data.settings.facets.splice(facetIndex, 1);
      } else {
        this.data.settings.facets.push(e.target.value);
      }
    },
  },
};
</script>

<style scoped>
.content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
}

.header-spacer {
  width: 40px;
}

.select-wrapper {
  width: 100%;
}

.facet {
  display: flex;
  gap: 5px;
}

.layer-select {
  width: 100%;
  height: 40px;
  font-size: 16px;
}

.layer-select:hover {
  background: var(--color-grey-40);
}
</style>
