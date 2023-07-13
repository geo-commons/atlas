<template>
  <div v-if="false"></div>
</template>

<script>
import Select from "ol/interaction/Select";
import VectorLayer from "ol/layer/Vector";
import { bbox as bboxStrategy } from "ol/loadingstrategy";
import GeoJSON from "ol/format/GeoJSON";
import VectorSource from "ol/source/Vector";
import { Style, Fill, Stroke, Circle } from "ol/style";
import OpenLayersParser from "geostyler-openlayers-parser";

const olParser = new OpenLayersParser();

const DEFAULT_STYLE = [
  new Style({
    stroke: new Stroke({
      color: "blue",
      width: 3,
    }),
    fill: new Fill({
      color: "rgba(0, 0, 255, 0.1)",
    }),
  }),
  new Style({
    image: new Circle({
      radius: 10,
      fill: new Fill({
        color: "blue",
      }),
    }),
  }),
];

export default {
  name: "WfsLayer",
  inject: ["map"],
  props: {
    id: String,
    name: String,
    url: String,
    layer: String,
    isVisible: Boolean,
    isSelectable: Boolean,
    selectedFeatures: Array,
    opacity: Number,
    clientStyle: Object,
    zIndex: Number,
    filters: Object,
    minZoom: Number,
    maxZoom: Number,
  },
  watch: {
    url(value) {
      this.source.set("url", value);
    },
    name(value) {
      this.tileLayer.set("name", value);
    },
    isVisible(value) {
      this.tileLayer.set("visible", value);
    },
    opacity(value) {
      this.tileLayer.set("opacity", value);
    },
    clientStyle(value) {
      this.applyStyle(value);
    },
    filters(value) {
      if (!value[this.id]) {
        return;
      }

      const cqlFilters = [];

      Object.keys(value[this.id]).forEach((key) => {
        if (value[this.id][key].length == 0) {
          return;
        }

        const values = value[this.id][key]
          .map((value) => `'${value}'`)
          .join(",");
        cqlFilters.push(`${key} IN (${values})`);
      });

      this.source.updateParams({
        ...this.source.getParams(),
        CQL_FILTER: cqlFilters.length > 0 ? cqlFilters.join(" AND ") : null,
      });

      this.source.refresh();
    },
    selectedFeatures(features) {
      if (this.select && features && features.length === 0) {
        this.select.getFeatures().clear();
      }
    },
  },
  async created() {
    this.source = new VectorSource({
      format: new GeoJSON(),
      strategy: bboxStrategy,
      url: (extent) => {
        const params = new URLSearchParams([
          ["service", "WFS"],
          ["version", "1.0.0"],
          ["request", "GetFeature"],
          ["typename", this.name],
          ["outputFormat", "application/json"],
          ["srsname", "EPSG:28992"],
          ["bbox", extent.join(",")],
        ]);

        const url = new URL(this.url);
        url.search = params.toString();

        return url.toString();
      },
    });

    this.tileLayer = new VectorLayer({
      name: this.name,
      visible: this.isVisible,
      source: this.source,
      opacity: this.opacity,
      zIndex: this.zIndex,
      selectable: this.isSelectable,
      minZoom: this.minZoom ? this.minZoom - 1 : undefined,
      maxZoom: this.maxZoom ? this.maxZoom : undefined,
    });

    this.map.addLayer(this.tileLayer);

    const style = await this.getStyle(
      this.clientStyle && this.clientStyle["default"]
        ? this.clientStyle["default"]
        : this.clientStyle
    );
    this.tileLayer.setStyle(style);

    if (this.isSelectable) {
      const activeStyle = await this.getStyle(
        this.clientStyle && this.clientStyle["active"]
          ? this.clientStyle["active"]
          : this.clientStyle
      );

      this.select = new Select({
        layers: [this.tileLayer],
        style: activeStyle,
      });

      this.select.on("select", this.onSelectFeatures);
      this.map.addInteraction(this.select);
    }
  },
  destroyed() {
    if (this.select) {
      this.map.removeInteraction(this.select);
    }

    this.map.removeLayer(this.tileLayer);
  },
  methods: {
    async getStyle(inputStyle) {
      if (!inputStyle) {
        return DEFAULT_STYLE;
      }

      try {
        const olStyle = await olParser.writeStyle(inputStyle);
        return olStyle.output;
      } catch (e) {
        console.error("Unable to parse style", e);
      }

      return DEFAULT_STYLE;
    },
    onSelectFeatures(e) {
      const features = e.target.getFeatures().getArray();
      if (features.length === 0) {
        return;
      }

      this.$emit("features-selected", features);
    },
  },
};
</script>

<style scoped></style>
