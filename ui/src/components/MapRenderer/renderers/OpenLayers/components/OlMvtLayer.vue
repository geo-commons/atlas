<template>
  <div v-if="false"></div>
</template>

<script>
import Projection from "ol/proj/Projection";
import { Style, Fill, Stroke, Circle } from "ol/style";
import VectorTileLayer from "ol/layer/VectorTile";
import VectorTileSource from "ol/source/VectorTile";
import WMTSCapabilities from "ol/format/WMTSCapabilities";
import MVT from "ol/format/MVT";
import WMTSSource, { optionsFromCapabilities } from "ol/source/WMTS";
import OpenLayersParser from "geostyler-openlayers-parser";

const olParser = new OpenLayersParser();

const rdProjection = new Projection({
  code: "EPSG:28992",
  units: "m",
});

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

const matrixIds = new Array(15);
for (var i = 0; i < 15; ++i) {
  matrixIds[i] = i;
}

export default {
  name: "MvtLayer",
  inject: ["map"],
  props: {
    name: String,
    url: String,
    layer: String,
    isVisible: Boolean,
    opacity: Number,
    zIndex: Number,
    minZoom: Number,
    maxZoom: Number,
    clientStyle: Object,
  },
  watch: {
    url() {
      this.setSource(this.url, this.name);
    },
    name(value) {
      this.tileLayer.set("name", value);
      this.setSource(this.url, this.name);
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
  },
  created() {
    this.tileLayer = new VectorTileLayer({
      name: this.name,
      visible: this.isVisible,
      opacity: this.opacity,
      zIndex: this.zIndex,
      source: null,
      selectable: true,
      minZoom: this.minZoom ? this.minZoom - 1 : undefined,
      maxZoom: this.maxZoom ? this.maxZoom : undefined,
    });

    this.map.addLayer(this.tileLayer);

    this.setSource(this.url, this.name);
    this.applyStyle(this.clientStyle);
  },
  destroyed() {
    this.map.removeLayer(this.tileLayer);
  },
  methods: {
    async setSource(url, name) {
      const response = await fetch(`${url}?REQUEST=GetCapabilities`);
      const body = await response.text();
      const caps = new WMTSCapabilities().read(body);
      const wmts = new WMTSSource(
        optionsFromCapabilities(caps, {
          layer: name,
          matrixSet: "EPSG:28992",
          format: "application/vnd.mapbox-vector-tile",
        })
      );

      this.tileLayer.setSource(
        new VectorTileSource({
          projection: rdProjection,
          format: new MVT(),
          tileGrid: wmts.getTileGrid(),
          tileUrlFunction: wmts.getTileUrlFunction(),
          tileLoadFunction: (tile, url) => {
            tile.setLoader((extent, resolution, projection) => {
              fetch(url).then((response) => {
                response.arrayBuffer().then((data) => {
                  const format = tile.getFormat();
                  const features = format.readFeatures(data, {
                    extent: extent,
                    featureProjection: projection,
                  });
                  tile.setFeatures(features);
                });
              });
            });
          },
        })
      );
    },
    async applyStyle(inputStyle) {
      if (!inputStyle) {
        return this.tileLayer.setStyle(DEFAULT_STYLE);
      }

      try {
        const olStyle = await olParser.writeStyle(inputStyle);
        this.tileLayer.setStyle(olStyle.output);
      } catch (e) {
        console.error("Unable to parse style", e);
      }
    },
  },
};
</script>

<style scoped></style>
