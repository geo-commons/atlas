<template>
  <div v-if="false"></div>
</template>

<script>
import Select from "ol/interaction/Select";

import { mapState } from "vuex";
import Projection from "ol/proj/Projection";
import TileLayer from "ol/layer/Tile";
import VectorTileLayer from "ol/layer/VectorTile";
import TileWMSSource from "ol/source/TileWMS";
import VectorTileSource from "ol/source/VectorTile";
import MVTFormat from "ol/format/MVT";
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

const rdProjection = new Projection({
  code: "EPSG:28992",
  units: "m",
});

/*const authenticatedTileLoader = (token) => {
  return (tile, src) => {
    const client = new XMLHttpRequest();
    client.open("GET", src);
    client.setRequestHeader("Authorization", `Bearer ${token}`);

    client.onload = () => {
      tile.getImage().src = src;
    };

    client.send();
  };
};*/

export default {
  name: "WmsLayer",
  inject: ["map"],
  props: {
    id: String,
    name: String,
    url: String,
    layer: String,
    isVisible: Boolean,
    sendTokenWithRequest: Boolean,
    opacity: Number,
    zIndex: Number,
    format: String,
    serverStyle: String,
    filters: Object,
    minZoom: Number,
    maxZoom: Number,
    tooltip: String,
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
  },
  async created() {
    const sourceOptions = {
      url: this.url,
      params: {
        LAYERS: this.name,
        FORMAT: this.format,
        TILED: true,
      },
      serverType: "geoserver",
      hidpi: false,
      transition: 0,
      projection: rdProjection,
    };

    this.source = new TileWMSSource(sourceOptions);

    if (this.format == "application/vnd.mapbox-vector-tile") {
      this.mvtVectorSource = new VectorTileSource({
        ...this.sourceOptions,
        projection: rdProjection,
        url: undefined,
        format: new MVTFormat({ layername: "_layer_" }),
        tileUrlFunction: (tileCoord, pixelRatio, projection) => {
          return this.source.tileUrlFunction(tileCoord, pixelRatio, projection);
        },
      });
    }

    if (this.format === "application/vnd.mapbox-vector-tile") {
      this.tileLayer = new VectorTileLayer({
        name: this.name,
        visible: this.isVisible,
        opacity: this.opacity,
        source: this.mvtVectorSource,
        projection: rdProjection,
        selectable: true,
        tooltip: this.tooltip,
        zIndex: this.zIndex,
        minZoom: this.minZoom ? this.minZoom - 1 : undefined,
        maxZoom: this.maxZoom ? this.maxZoom : undefined,
      });

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
    } else {
      this.tileLayer = new TileLayer({
        name: this.name,
        visible: this.isVisible,
        opacity: this.opacity,
        source: this.source,
        zIndex: this.zIndex,
        minZoom: this.minZoom ? this.minZoom - 1 : undefined,
        maxZoom: this.maxZoom ? this.maxZoom : undefined,
      });
    }

    this.map.addLayer(this.tileLayer);
  },
  destroyed() {
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
  },
  computed: mapState({
    user: (state) => state.user,
  }),
};
</script>

<style scoped></style>
