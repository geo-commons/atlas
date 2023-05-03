<template>
  <div ref="viewer" class="google-maps"></div>
</template>

<script>
import { transform } from "ol/proj";
import { getDefinitions } from "../utils/projections";
import { register } from "ol/proj/proj4";

// Register EPSG:28992 projection
register(getDefinitions());

export default {
  name: "GoogleMaps",
  props: {
    position: Object,
    viewer: Object,
  },
  watch: {
    position(value) {
      if (!value.marker) {
        return;
      }

      const latlong = transform(value.marker, "EPSG:28992", "EPSG:4326");
      this.streetview.setPosition({ lat: latlong[1], lng: latlong[0] });
    },
  },
  mounted() {
    const latlong = transform(this.position.marker, "EPSG:28992", "EPSG:4326");
    // eslint-disable-next-line no-undef
    this.streetview = new google.maps.StreetViewPanorama(this.$refs.viewer, {
      position: {
        lat: latlong[1],
        lng: latlong[0],
      },
      zoom: this.position.zoom,
      fullscreenControl: false,
    });
  },
  methods: {
    resize() {
      // eslint-disable-next-line no-undef
      google.maps.event.trigger(this.streetview, "resize");
    },
  },
};
</script>

<style scoped>
.google-maps {
  width: 100%;
  height: 100%;
}
</style>
