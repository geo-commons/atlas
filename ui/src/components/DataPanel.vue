<template>
  <SidePanel large :show-panel="showDataPanel">
    <template #search>
      <div class="flexer">
        <button
          v-tippy
          class="iconbutton close-button"
          type="button"
          content="Sluit paneel"
          aria-label="Sluit paneel"
          @click="toggleDataPanel"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24"
            viewBox="0 0 24 24"
            width="24"
          >
            <path d="M0 0h24v24H0z" fill="none" />
            <path
              d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
            />
          </svg>
        </button>
        <SearchForm
          :show-border="true"
          :has-visible-layers="visibleLayers.length > 0"
          class="data-search"
          @on-submit="onSearch"
        >
          <template #default>
            <input
              ref="queryInput"
              type="search"
              name="search"
              placeholder="Zoek data"
              autocomplete="off"
            />
          </template>
        </SearchForm>
      </div>
    </template>

    <template #default>
      <FeatureTable
        v-for="visibleLayer in visibleLayers"
        :key="visibleLayer.id"
        :is-open="visibleLayers.length === 1"
        :is-filterable="true"
        :layer="visibleLayer"
        :position="position"
        :selected-area="selectedArea"
        :query="query"
        :user="user"
        @set-position="setPosition"
        @on-fit="onFit"
      />
    </template>
  </SidePanel>
</template>

<script>
import SidePanel from "./SidePanel";
import FeatureTable from "./FeatureTable";
import SearchForm from "./SearchForm";

const visibleSourceTypes = ["WMS_WFS", "WFS"];

export default {
  name: "DataPanel",
  components: {
    SidePanel,
    FeatureTable,
    SearchForm,
  },
  props: {
    position: Object,
    layers: Array,
    showDataPanel: Boolean,
    selectedArea: Object,
    user: Object,
  },
  data() {
    return {
      query: "",
    };
  },
  computed: {
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
    onSearch() {
      this.query = this.$refs.queryInput.value;
    },
    toggleDataPanel() {
      this.$emit("toggle-data-panel");
    },
    setPosition(value) {
      this.$emit("set-position", value);
    },
    onFit(value) {
      this.$emit("on-fit", value);
    },
  },
};
</script>

<style scoped>
.close-button {
  width: var(--width-button-large);
  height: var(--width-button-large);
  border-radius: var(--radius-normal);
  border: 1px solid var(--color-grey-60);
  margin-right: 12px;
}

.flexer {
  display: flex;
}

@media (min-width: 576px) {
  .data-search {
    margin: 0 auto;
    max-width: var(--width-detail);
  }

  .flexer {
    padding-right: calc(var(--width-button-large) + 12px);
  }
}
</style>
