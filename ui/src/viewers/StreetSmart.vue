<template>
  <div ref="viewer" class="street-smart"></div>
</template>

<script>
export default {
  name: "StreetSmart",
  props: {
    position: Object,
    username: String,
    password: String,
    apiKey: String,
  },
  watch: {
    position(value) {
      if (!value.marker) {
        return;
      }

      this.setPosition(value.marker);
    },
  },
  mounted() {
    const options = {
      targetElement: this.$refs.viewer,
      username: this.username,
      password: this.password,
      apiKey: this.apiKey,
      srs: "EPSG:28992",
      locale: "nl",
    };

    window.StreetSmartApi.init(options).then(() => {
      this.setPosition(this.position.marker);
    });
  },
  beforeDestroy() {
    window.StreetSmartApi.destroy({
      targetElement: this.$refs.viewer,
    });
  },
  methods: {
    resize() {
      // streetsmart watches resize itself
    },
    setPosition(position) {
      const options = {
        viewerType: [window.StreetSmartApi.ViewerType.PANORAMA],
        panoramaViewer: {
          closable: false,
          maximizable: false,
        },
        obliqueViewer: {
          closable: false,
          maximizable: false,
        },
      };

      window.StreetSmartApi.open(
        `${position[0]}, ${position[1]}`,
        options
      ).then((results) => {
        if (!results || results.length === 0) {
          return;
        }

        const viewer = results[0];
        viewer.toggle3DCursor(false);
      });
    },
  },
};
</script>

<style scoped>
.street-smart {
  width: 100%;
  height: 100%;
  padding-top: 32px; /* make sure buttons of Atlas do not overlap buttons of StreetSmart */
}
</style>
