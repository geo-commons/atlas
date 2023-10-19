<template>
  <div class="buttonviewer">
    <div>
      <a :href="src" class="button __primary" target="_blank" rel="nofollow">Open viewer in nieuw tabblad</a>
    </div>
  </div>
</template>

<script>
import nunjucks from "nunjucks";
import { transform } from "ol/proj";
import { register } from "ol/proj/proj4";
import { getDefinitions } from "../utils/projections";

// Register EPSG:28992 projection
register(getDefinitions());

nunjucks.configure({ autoescaping: true });

export default {
  name: "ButtonViewer",
  props: {
    position: Object,
    url: String,
  },
  computed: {
    src() {
      const latlong = transform(this.position.marker, "EPSG:28992", "EPSG:4326");

      const properties = {
        lat: latlong[1],
        lon: latlong[0],
        x: this.position.marker[0],
        y: this.position.marker[1],
      };

      return nunjucks.renderString(this.url, properties);
    },
  },
  methods: {
    resize() {
      // iframe resize is not required
    },
  },
};
</script>

<style scoped>
.buttonviewer {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
