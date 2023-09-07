<template>
  <div v-if="false"></div>
</template>

<script>
import { mapState } from "vuex";
import Projection from "ol/proj/Projection";
import TileLayer from "ol/layer/Tile";
import TileWMSSource from "ol/source/TileWMS";

const rdProjection = new Projection({
  code: "EPSG:28992",
  units: "m",
});

const authenticatedTileLoader = (token) => {
  return (tile, src) => {
    const client = new XMLHttpRequest();
    client.open("GET", src);
    client.setRequestHeader("Authorization", `Bearer ${token}`);

    client.onload = () => {
      tile.getImage().src = src;
    };

    client.send();
  };
};

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
  created() {
    this.source = new TileWMSSource({
      url: this.url,
      crossOrigin: "anonymous",
      params: {
        VERSION: "1.1.1",
        FORMAT: this.format,
        LAYERS: this.name,
        STYLES: this.serverStyle ? this.serverStyle : "",
        tiled: true,
        tilesOrigin: 117000 + "," + 498000.00000000023,
      },
      projection: rdProjection,
      tileLoadFunction: this.sendTokenWithRequest
        ? authenticatedTileLoader(this.user.token)
        : null,
    });

    this.tileLayer = new TileLayer({
      name: this.name,
      visible: this.isVisible,
      opacity: this.opacity,
      source: this.source,
      zIndex: this.zIndex,
      minZoom: this.minZoom ? this.minZoom - 1 : undefined,
      maxZoom: this.maxZoom ? this.maxZoom : undefined,
    });

    this.map.addLayer(this.tileLayer);
  },
  destroyed() {
    this.map.removeLayer(this.tileLayer);
  },
  computed: mapState({
    user: (state) => state.user,
  }),
};
</script>

<style scoped></style>
