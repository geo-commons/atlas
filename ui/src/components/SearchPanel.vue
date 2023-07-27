<template>
  <div class="wrapper">
    <SearchForm
      :show-suggestions="showSuggestions"
      :has-visible-layers="visibleLayers.length > 0"
      :features="features"
      @show-data-panel="toggleDataPanel"
      @on-submit="onSearch"
    >
      <template #default>
        <input
          v-model="query"
          type="search"
          name="search"
          placeholder="Zoek adres"
          autocomplete="off"
          aria-autocomplete="list"
          role="combobox"
          aria-owns="search-results"
          :aria-expanded="showSuggestions && results.length"
          @keyup="onSearch"
        />
      </template>

      <template #suggestions>
        <div v-if="showSuggestions && results.length" class="results">
          <ul id="search-results" class="list" role="listbox">
            <li
              v-for="result in results"
              :key="result.id"
              role="option"
              tabindex="-1"
              aria-selected="false"
              @click="(e) => onNavigate(e, result.id)"
            >
              <a href="#">{{ result.weergavenaam }}</a>
            </li>
          </ul>
        </div>
      </template>
    </SearchForm>
  </div>
</template>

<script>
import SearchForm from "./SearchForm";

const suggestEndpoint =
  "https://api.pdok.nl/bzk/locatieserver/search/v3_1/suggest";
const freeEndpoint = "https://api.pdok.nl/bzk/locatieserver/search/v3_1/free";

const visibleSourceTypes = ["WMS_WFS", "WFS"];

export default {
  name: "SearchPanel",
  components: {
    SearchForm,
  },
  props: {
    position: Object,
    layers: Array,
    features: Object,
  },
  data() {
    return {
      showSuggestions: false,
      results: [],
    };
  },
  computed: {
    query: {
      get() {
        return this.$store.state.searchQuery;
      },
      set(value) {
        this.$store.commit("setSearchQuery", value);
      },
    },
    visibleLayers() {
      return this.layers.filter(
        (layer) =>
          layer.is_visible &&
          !layer.is_base &&
          visibleSourceTypes.includes(layer.source_type)
      );
    },
  },
  methods: {
    toggleDataPanel() {
      this.$emit("toggle-data-panel");
    },
    async onSearch() {
      this.results = [];

      if (!this.query) {
        this.$emit("set-position", { ...this.position, marker: null });
        this.showSuggestions = false;
        return;
      }

      try {
        const result = await fetch(
          `${suggestEndpoint}?fq=gemeentenaam:(${encodeURIComponent(
            this.$store.state.config.suggest_municipalities
          )})&q=${encodeURIComponent(this.query)}`
        );
        const data = await result.json();

        this.showSuggestions = true;
        this.results = data.response.docs;
      } catch (e) {
        console.error(e);
        this.$store.commit(
          "setAlert",
          "Er is een fout opgetreden, controleer de verbinding en probeer het opnieuw."
        );
      }
    },
    async onNavigate(e, id) {
      e.preventDefault();

      try {
        const result = await fetch(
          `${freeEndpoint}?q=${encodeURIComponent("id:" + id)}`
        );

        const data = await result.json();
        if (!data.response.docs) {
          return;
        }

        const object = data.response.docs[0];

        const centeroide = /POINT\(([\d.]+) ([\d.]+)\)/.exec(
          object.centroide_rd
        );
        const parsedCenteroide = [
          parseFloat(centeroide[1]),
          parseFloat(centeroide[2]),
        ];

        this.$emit("set-position", {
          ...this.position,
          marker: parsedCenteroide,
          center: parsedCenteroide,
          zoom: 19,
        });

        this.query = object.weergavenaam;
        this.showSuggestions = false;
      } catch (e) {
        console.error(e);
        this.$store.commit(
          "setAlert",
          "Er is een fout opgetreden, controleer de verbinding en probeer het opnieuw."
        );
      }
    },
  },
};
</script>

<style scoped>
.wrapper {
  width: var(--width-detail);
  max-width: 100%;
}

@media (min-width: 576px) {
  .showDataPanel .wrapper {
    display: none;
  }
}
</style>
