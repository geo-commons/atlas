<template>
  <div class="layer-field">
    <multiselect
      v-bind="field"
      v-model="inputVal"
      placeholder="Kies een laag"
      deselect-label="Druk op enter om te verwijderen"
      select-label="Druk op enter om te selecteren"
      selected-label="Geselecteerd"
      tag-placeholder="Druk op enter om nieuwe laag aan te maken"
      :options="availableLayers"
      :searchable="true"
      :taggable="true"
      @tag="addTag"
    >
    </multiselect>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import Multiselect from "vue-multiselect";
import { WMSCapabilities } from "ol/format";

export default defineComponent({
  name: "LayerField",
  components: { Multiselect },
  props: {
    field: Object,
    currentSourceId: Number,
    sources: Array,
    value: String,
  },
  emits: ["update:modelValue"],
  data() {
    return {
      availableLayers: [],
    };
  },
  computed: {
    selectedSource() {
      return this.sources.find((arr) => arr.id === this.currentSourceId);
    },
    inputVal: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
      },
    },
  },
  watch: {
    selectedSource(newValue, oldValue) {
      if (newValue !== oldValue || newValue.id !== oldValue.id) {
        this.getLayers();
      }
    },
  },
  created() {
    this.getLayers();
  },
  methods: {
    addTag(tag) {
      this.availableLayers.push(tag);
      this.currentValues["layer_name"] = tag;
    },
    async getLayers() {
      this.availableLayers = [];

      if (!this.selectedSource) {
        return;
      }

      // Don't run GetLayers for source with type REST, only for OWS
      if (this.selectedSource.type !== "OWS") {
        return;
      }

      try {
        const url = new URL(this.selectedSource.url);

        const params = new URLSearchParams({
          SERVICE: "WMS",
          REQUEST: "GetCapabilities",
          VERSION: "1.1.1",
        });

        url.search = params.toString();

        const response = await fetch(url);
        const body = await response.text();

        if (!body) {
          return;
        }

        const caps = await new WMSCapabilities().read(body);
        const layers = caps?.Capability?.Layer?.Layer.map((layer) => layer.Name);

        this.availableLayers = layers ? layers : [];
      } catch (e) {
        console.error("failed to fetch source capabilities: ", e);
      }
    },
  },
});
</script>

<style scoped>
.layer-field :deep(.multiselect .multiselect__input) {
  padding: 0;
}

.layer-field :deep(.multiselect) {
  padding: 0px;
}

.layer-field :deep(.multiselect__tags) {
  padding: 8px 40px 0 16px;
  font-size: 16px;
}

.layer-field :deep(.multiselect__single) {
  padding: 0;
  margin-bottom: 0;
}
</style>
