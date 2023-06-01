<template>
  <PanelDisplay :title="layerDisplayName" @hidePanel="hidePanel">
    <p v-if="!layer" class="info-text">
      De lijstweergave is nog niet geconfigureerd.
    </p>

    <ul v-if="layer">
      <li
        v-for="feature in filteredFeatures"
        :key="feature.id"
        class="list-item"
        @click="selectFeature(feature)"
      >
        <div class="header">
          <span class="name">
            <MarkdownTemplate
              :source="titleTemplate"
              :data="feature.properties"
            />
          </span>
        </div>
        <div class="address">
          <MarkdownTemplate
            :source="shortDescriptionTemplate"
            :data="feature.properties"
          />
        </div>
      </li>
    </ul>
  </PanelDisplay>
</template>

<script>
import MarkdownTemplate from "./MarkdownTemplate";
import GeoJSON from "ol/format/GeoJSON";

import PanelDisplay from "./PanelDisplay";

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
    filters: Object,
  },
  data() {
    return {
      features: [],
      error: false,
      loading: false,
    };
  },
  computed: {
    filteredFeatures() {
      const filters = this.filters[this.layer.id];
      if (!filters || Object.keys(filters).length === 0) {
        return this.features;
      }

      return this.features.filter((feature) => {
        let isVisible = true;
        Object.keys(filters).map((key) => {
          if (filters[key].length === 0) {
            return;
          }

          if (!filters[key].includes(feature.properties[key])) {
            isVisible = false;
          }
        });

        return isVisible;
      });
    },
    layerDisplayName() {
      return this.layer ? this.layer.title : "";
    },
  },
  watch: {
    layer: "fetchFeatures",
  },
  mounted() {
    if (this.layer) {
      this.fetchFeatures();
    }
  },
  methods: {
    selectFeature(feature) {
      const geometry = new GeoJSON().readFeature(feature).getGeometry();
      this.$emit("on-fit", geometry.getExtent());
    },
    hidePanel() {
      this.$emit("hidePanel");
    },
    async fetchFeatures() {
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

      try {
        const url = new URL(this.layer.url);
        url.search = params.toString();

        const result = await fetch(url.toString());
        const data = await result.json();

        this.features = data.features;
      } catch (e) {
        console.error(e);
        this.error = true;
        this.features = [];
      }

      this.loading = false;
    },
    formatLength(length) {
      if (length > 1000) {
        return Math.round(length / 1000) + " " + "km";
      }

      return Math.round(length) + " " + "m";
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

.type {
  display: flex;
  align-content: center;
  font-size: var(--font-size-small);
  color: var(--color-text-grey);
  margin-top: 2px;
}

.type img {
  margin-left: 5px;
}

.distance {
  margin-left: auto;
  flex-shrink: 0;
  color: var(--color-text-grey);
  font-size: var(--font-size-small);
}

.address {
  margin-top: 4px;
  font-size: var(--font-size-small);
}

.info-text {
  margin: 30px 20px;
}
</style>
