<template>
  <ExpandButton
    v-if="features.length > 0"
    :title="featureInfoTitle"
    :is-open="isOpen"
    class="feature"
  >
    <div
      v-for="feature in features"
      :key="feature.id"
      class="border-bottom feature-select"
      @click="() => $emit('show-selected-feature', feature)"
    >
      <table-list>
        <table>
          <tbody>
            <tr
              v-for="property in filterProperties(feature.properties)"
              :key="property"
            >
              <td>
                {{
                  layer.friendly_fields && layer.friendly_fields[property]
                    ? layer.friendly_fields[property]
                    : property | capitalize
                }}
              </td>
              <td>
                <RichValue
                  :data-key="property"
                  :data-value="feature.properties[property]"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </table-list>

      <div
        v-for="(linkedData, key) in layer.linked_data"
        :key="key"
        class="linked-data"
      >
        <div v-if="features[0].properties[linkedData.source_key]">
          <b>{{ linkedData.title }}</b>
          <FeatureTableExpandable
            :layer="linkedData"
            :overall-filter="{
              key: linkedData.target_key,
              value: features[0].properties[linkedData.source_key],
            }"
            :position="position"
            @set-position="setPosition"
          />
        </div>
      </div>

      <div v-for="(template, key) in layer.templates" :key="key">
        <FeatureInfoTemplate
          :layer="layer"
          :template="template"
          :feature="feature"
          class="template"
        />
      </div>
    </div>
  </ExpandButton>
</template>

<script>
import nunjucks from "nunjucks";
import { mapState } from "vuex";
import { getForViewAndSize } from "ol/extent";
import FeatureTableExpandable from "./FeatureTableExpandable";
import TableList from "./TableList";
import TileWMS from "ol/source/TileWMS";
import View from "ol/View";
import ExpandButton from "./ExpandButton";
import RichValue from "./RichValue";
import FeatureInfoTemplate from "./FeatureInfoTemplate";

nunjucks.configure({ autoescaping: true });

export default {
  name: "FeatureInfo",
  components: {
    TableList,
    FeatureTableExpandable,
    ExpandButton,
    RichValue,
    FeatureInfoTemplate,
  },
  filters: {
    capitalize: function (value) {
      if (!value) return "";
      // Replace underscores by spaces
      value = value.toString().replace(/_/g, " ");
      // Uppercase first character
      return value.charAt(0).toUpperCase() + value.slice(1);
    },
  },
  props: {
    layer: Object,
    position: Object,
    isOpen: Boolean,
  },
  data() {
    return {
      features: [],
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
    featureInfoTitle() {
      if (this.features.length > 1) {
        return `${this.layer.title} (${this.features.length})`;
      }

      return this.layer.title;
    },
  },
  watch: {
    position: "fetchFeatures",
  },
  mounted() {
    this.fetchFeatures();
  },
  methods: {
    fetchFeatures() {
      if (
        this.layer.source_type === "WMS" ||
        this.layer.source_type === "WMS_WFS"
      ) {
        return this.fetchFeaturesFromWMS();
      }

      if (this.layer.source_type === "WFS") {
        return this.fetchFeaturesFromWFS();
      }
    },
    async fetchFeaturesFromWMS() {
      const wmsSource = new TileWMS({
        url: this.layer.url,
        servertype: this.layer.server_type,
        params: {
          LAYERS: this.layer.name,
          TILED: true,
        },
      });

      const view = new View({
        center: this.position.center,
        zoom: this.position.zoom,
      });

      const url = wmsSource.getFeatureInfoUrl(
        this.position.marker,
        view.getResolution(),
        "EPSG:28992",
        {
          info_format: "application/json",
          feature_count: 20,
        }
      );

      try {
        const result = await fetch(url, this.getFetchParameters());
        const data = await result.json();
        this.features = data.features;
      } catch (e) {
        console.error(e);
      }
    },
    async fetchFeaturesFromWFS() {
      const view = new View({
        center: this.position.center,
        zoom: this.position.zoom,
      });

      const extent = getForViewAndSize(
        this.position.marker,
        view.getResolution(),
        0,
        [1, 1]
      );

      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "2.0.0"],
        ["request", "GetFeature"],
        ["typename", this.layer.name],
        ["outputFormat", "application/json"],
        ["srsname", this.layer.projection],
        ["bbox", extent.join(",")],
        ["maxFeatures", "20"],
      ]);

      const url = new URL(this.layer.url);
      url.search = params.toString();

      const result = await fetch(url.toString(), this.getFetchParameters());
      const data = await result.json();
      this.features = data.features;
    },
    setPosition(value) {
      this.$store.commit("setPosition", value);
    },
    filterProperties(fetchedProperties) {
      if (this.layer.display_properties.length > 0) {
        return this.layer.display_properties.filter((p) =>
          Object.keys(fetchedProperties).includes(p)
        );
      }

      return Object.keys(fetchedProperties);
    },
    getFetchParameters() {
      if (
        this.layer.source &&
        this.layer.source.authenticate &&
        this.user &&
        this.user.token
      ) {
        return {
          headers: { Authorization: `Bearer ${this.user.token}` },
        };
      }

      return {};
    },
  },
};
</script>

<style scoped>
.feature:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-50);
}

.linked-data {
  padding: 0 20px;
  margin: 4px 0 8px;
}

.template {
  padding: 0 20px;
  margin: 4px 0 8px;
}

.template-title {
  display: block;
}

.table-wrapper {
  margin: 4px 0 8px;
}

.table-wrapper + .table-wrapper {
  border-top: 1px solid var(--color-grey-50);
}

.table-wrapper table {
  table-layout: fixed;
}

.table-wrapper td:first-child {
  width: 30%;
  color: var(--color-text-grey);
}

.table-wrapper td:last-child {
  width: 70%;
}

.separator-line {
  border: 0;
  border-top: 1px solid var(--color-grey-50);
  margin: 0 20px;
}

.border-bottom:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-50);
}

.feature-select:hover {
  background: var(--color-grey-40);
  cursor: pointer;
}
</style>
