<template>
  <div class="wrapper">
    <SearchForm
      :show-suggestions="showSuggestions ? true : null"
      :has-visible-layers="visibleLayers.length > 0"
      :features="features"
      :map-id="mapId"
      :show-data-panel="showDataPanel"
      @show-data-panel="toggleDataPanel"
      @on-submit="onSearch"
    >
      <template #default>
        <input
          v-model="query"
          type="search"
          name="search"
          placeholder="Zoek adres, perceel of coördinaten"
          autocomplete="off"
          aria-autocomplete="list"
          role="combobox"
          aria-owns="search-results"
          class="search-address"
          :aria-expanded="showSuggestions && results.length ? true : null"
          @keyup="onSearch"
          @keydown.enter.prevent="selectFirstAvailable"
        />
      </template>

      <template #suggestions>
        <div v-if="showSuggestions && results.length" class="results">
          <ul id="search-results" class="list" role="listbox">
            <li v-for="result in results" :key="result.id" role="option" tabindex="-1" aria-selected="false">
              <button @click="(e) => onNavigate(e, result)">
                {{ result.weergavenaam }}
              </button>
            </li>
          </ul>
        </div>
      </template>
    </SearchForm>
  </div>
</template>

<script>
import SearchForm from "./SearchForm";
import { EPSG28992Bounds } from "@/utils/projections";
import { useGlobalStore } from "@/stores";
import { mapStores } from "pinia";

const suggestEndpoint = "https://api.pdok.nl/bzk/locatieserver/search/v3_1/suggest";

const visibleSourceTypes = ["WMS_WFS", "WFS"];

export default {
  name: "SearchPanel",
  components: {
    SearchForm,
  },
  props: {
    position: Object,
    mapId: String,
    layers: Array,
    features: Object,
    showDataPanel: Boolean,
  },
  emits: ["toggle-data-panel", "set-position"],
  data() {
    return {
      showSuggestions: false,
      results: [],
    };
  },
  computed: {
    ...mapStores(useGlobalStore),
    query: {
      get() {
        return this.globalStore.searchQuery.title
          ? this.globalStore.searchQuery.title
          : this.globalStore.searchQuery.coordinates;
      },
      set(value) {
        this.globalStore.setSearchQuery({ title: value });
      },
    },
    visibleLayers() {
      return this.layers.filter(
        (layer) => layer.is_visible && !layer.is_base && visibleSourceTypes.includes(layer.source_type),
      );
    },
  },
  // TODO: check if this works
  watch: {
    "this.globalStore.searchQuery"(newValue, oldValue) {
      if (newValue.coordinates !== oldValue.coordinates) {
        this.results = [];
      }
    },
  },
  methods: {
    toggleDataPanel() {
      this.$emit("toggle-data-panel");
    },
    async onSearch(e) {
      // Since there is a separate enter key event we want to ignore it here.
      if (e.key === "Enter") {
        return;
      }

      if (!this.query) {
        this.$emit("set-position", { ...this.position, marker: null });
        this.showSuggestions = false;
        return;
      }

      let source, municipalityName;
      if (this.query.match(/[a-zA-Z]{3}[0-9]{2}/)) {
        // Check if the user searches a registry numbers (e.g. PMR00)
        source = "DKK";
        municipalityName = `kadastrale_gemeentenaam:(${encodeURIComponent(this.globalStore.config.suggest_municipalities)})`;
      } else {
        source = "BAG";
        municipalityName = `gemeentenaam:(${encodeURIComponent(this.globalStore.config.suggest_municipalities)})`;
      }

      try {
        const result = await fetch(
          `${suggestEndpoint}?fq=bron:${source}&fq=${municipalityName}&fl=weergavenaam,centroide_rd&q=${encodeURIComponent(this.query)}`,
        );
        const data = await result.json();

        this.showSuggestions = true;
        this.results = data.response.docs;

        // Check if user is searching for coordinates
        this.parseCoordinateQuery();
      } catch (e) {
        console.error(e);
        this.globalStore.setAlert("Er is een fout opgetreden, controleer de verbinding en probeer het opnieuw.");
      }
    },
    async onNavigate(e, suggestion) {
      if (suggestion.type === "warning") {
        return;
      }

      e.preventDefault();

      if (suggestion.type === "coordinates") {
        this.$emit("set-position", {
          ...this.position,
          marker: suggestion.coordinates,
          center: suggestion.coordinates,
          zoom: 19,
          flyTo: true,
        });
        this.query = suggestion.weergavenaam;
        this.showSuggestions = false;

        return;
      }

      try {
        const centeroide = /POINT\(([\d.]+) ([\d.]+)\)/.exec(suggestion.centroide_rd);
        const parsedCenteroide = [parseFloat(centeroide[1]), parseFloat(centeroide[2])];

        this.$emit("set-position", {
          ...this.position,
          marker: parsedCenteroide,
          center: parsedCenteroide,
          zoom: 19,
          flyTo: true,
        });

        this.query = suggestion.weergavenaam;
        this.showSuggestions = false;
      } catch (e) {
        console.error(e);
        this.globalStore.setAlert("Er is een fout opgetreden, controleer de verbinding en probeer het opnieuw.");
      }
    },
    async selectFirstAvailable(e) {
      if (!this.results.length) {
        return;
      }

      await this.onNavigate(e, this.results[0]);
    },
    parseCoordinateQuery() {
      // If the query contains any alphabetic character the user is searching for an address instead of coordinates.
      if (/[a-z]/i.test(this.query)) {
        return;
      }
      // Remove whitespace and parentheses and split the query on "," and ";".
      const coordinates = this.query.replace(/[() ]/g, "").split(/[\s,;]+/);
      // Next map the strings to integers.
      const intCoordinates = coordinates.map((c) => +c);

      // Check if there are 2 coordinates found.
      if (intCoordinates.length === 2) {
        if (!this.checkCoordinateRange(intCoordinates)) {
          const coordinateResult = {
            type: "warning",
            weergavenaam: "De ingevoerde coördinaten liggen buiten het beschikbare bereik.",
          };
          this.results.push(coordinateResult);
          return;
        }

        const coordinateResult = {
          type: "coordinates",
          coordinates: intCoordinates,
          weergavenaam: `${intCoordinates.join(", ")}`,
        };
        this.results.push(coordinateResult);
      }
    },
    checkCoordinateRange(coordinates) {
      const xCoordinate = coordinates[0];
      const yCoordinate = coordinates[1];
      // For now this is the condition to check whether the given coordinates are in the available zone
      // i.e. EPSG:28992. For reference see: https://epsg.io/28992
      if (
        EPSG28992Bounds.minX <= xCoordinate &&
        EPSG28992Bounds.maxX >= xCoordinate &&
        EPSG28992Bounds.minY <= yCoordinate &&
        EPSG28992Bounds.maxY >= yCoordinate
      ) {
        return true;
      }
      return false;
    },
  },
};
</script>

<style scoped>
.wrapper {
  width: var(--width-detail);
  max-width: 100%;
}

.search-address {
  width: 100%;
  padding-left: 16px;
  text-overflow: ellipsis;
}

::-webkit-search-cancel-button {
  display: none;
}
</style>
