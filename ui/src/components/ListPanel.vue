<template>
  <PanelDisplay
    :title="layerDisplayName ? layerDisplayName : 'Lijstweergave'"
    :loading="loading"
    @hide-panel="hidePanel"
  >
    <p v-if="!layer" class="info-text">De lijstweergave is nog niet geconfigureerd.</p>

    <ul v-if="layer">
      <li v-for="feature in features" :key="feature.id" class="list-item" @click="showFeatureOnMap(feature)">
        <div class="header">
          <span class="name">
            <MarkdownTemplate :source="titleTemplate" :data="feature.properties" />
          </span>
        </div>
        <div class="address">
          <MarkdownTemplate :source="shortDescriptionTemplate" :data="feature.properties" />
        </div>
      </li>
    </ul>
  </PanelDisplay>
</template>

<script>
import MarkdownTemplate from "./MarkdownTemplate";
import PanelDisplay from "./PanelDisplay";
import { useMapStore } from "@/stores/map_store";
import { getFetchParameters } from "@/utils/auth";
import { getLayerCqlFilter } from "@/utils/layer-filter-cql";
import { getWfsTimeCqlFilter } from "@/utils/wms-time";
import { WKT } from "ol/format";

export default {
  name: "ListPanel",
  components: {
    PanelDisplay,
    MarkdownTemplate,
  },
  props: {
    layer: Object,
    titleTemplate: String,
    shortDescriptionTemplate: String,
    mapId: String,
    selectedArea: Object,
    user: Object,
  },
  emits: ["hidePanel", "show-feature-on-map"],
  data() {
    return {
      features: [],
      error: false,
      loading: false,
      store: null,
    };
  },
  computed: {
    layerDisplayName() {
      return this.layer ? this.layer.title : "";
    },
    currentLayerFilter() {
      return this.layer ? this.store?.layerFilters?.[this.layer.id] : null;
    },
  },
  watch: {
    layer: "fetchFeatures",
    selectedArea: "fetchFeatures",
    currentLayerFilter: {
      handler: "fetchFeatures",
      deep: true,
    },
    "store.selectedTimeSliderLayerId": "fetchFeatures",
    "store.timeSliderDisplayMode": "fetchFeatures",
    "store.timeSliderStepSize": "fetchFeatures",
    "store.timeSliderReferenceDate": "fetchFeatures",
    "store.timeSliderPeriodDates": {
      handler: "fetchFeatures",
      deep: true,
    },
    "store.timeSliderMinDate": "fetchFeatures",
    "store.timeSliderMaxDate": "fetchFeatures",
    "store.timeSliderCapabilitiesLoading": "fetchFeatures",
    "store.timeSliderCapabilitiesError": "fetchFeatures",
  },
  created() {
    this.store = useMapStore(this.mapId);
  },
  mounted() {
    if (this.layer) {
      this.fetchFeatures();
    }
  },
  methods: {
    showFeatureOnMap(feature) {
      this.$emit("show-feature-on-map", feature, this.layer);
    },
    hidePanel() {
      this.$emit("hidePanel");
    },
    async fetchFeatures() {
      if (!this.layer) {
        this.features = [];
        return;
      }

      this.loading = true;
      this.error = false;

      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "1.0.0"],
        ["request", "GetFeature"],
        ["typename", this.layer.name],
        ["outputFormat", "application/json"],
        ["maxFeatures", "5000"],
      ]);

      const filters = [];
      const layerCqlFilter = getLayerCqlFilter(this.store.layerFilters, this.layer.id);

      if (layerCqlFilter) {
        filters.push(`(${layerCqlFilter})`);
      }

      if (this.selectedArea) {
        const wkt = new WKT();
        const geom = wkt.writeGeometry(this.selectedArea);
        const fullFilter = `WITHIN(geom,${geom})`;

        if (encodeURIComponent(fullFilter).length <= 32000) {
          filters.push(fullFilter);
        } else {
          this.error = true;
          this.features = [];
          this.loading = false;
          return;
        }
      }

      const timeFilter = getWfsTimeCqlFilter(this.store, this.layer);

      if (timeFilter) {
        filters.push(timeFilter);
      }

      if (filters.length > 0) {
        params.set("cql_filter", filters.join(" AND "));
      }

      try {
        const url = new URL(this.layer.url);
        url.search = params.toString();

        const result = await fetch(url.toString(), getFetchParameters(this.layer, this.user));

        if (!result.ok) {
          throw new Error("failed fetching features");
        }

        const data = await result.json();

        this.features = data.features || [];
      } catch (e) {
        console.error(e);
        this.error = true;
        this.features = [];
      }

      this.loading = false;
    },
  },
};
</script>

<style scoped>
.list-item {
  display: block;
  padding: 12px 16px;
}

.list-item:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-20);
}

.list-item:not([disabled]) {
  cursor: pointer;
}

.list-item:not([disabled]):hover {
  background: var(--color-hover);
}

.list-item:not([disabled]):active {
  background: var(--color-active);
}

.list-item:not([disabled]):hover .name,
.list-item:not([disabled]):active .name {
  text-decoration: underline;
}

.header {
  display: flex;
}

.name {
  color: var(--color-primary);
}

.type img {
  margin-left: 5px;
}

.address {
  margin-top: 4px;
  font-size: var(--font-size-small);
}

.info-text {
  margin: 30px 20px;
}
</style>
