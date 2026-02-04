<template>
  <div class="wrapper">
    <div class="header">
      <input ref="input" type="text" name="embedCode" class="input" :value="embedCode" readonly="readonly" />
      <button class="iconbutton" type="button" :aria-label="buttonText" @click="copyHTML">
        <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
          <path d="M0 0h24v24H0V0z" fill="none" />
          <path
            d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"
          />
        </svg>
      </button>
      <button class="iconbutton" aria-label="Sluiten" @click="closeModal">
        <svg
          width="14px"
          height="14px"
          viewBox="0 0 14 14"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
        >
          <title>Path</title>
          <g id="Wireframes" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
            <g id="streetview" transform="translate(-985.000000, -413.000000)" fill="#000000" fill-rule="nonzero">
              <g id="Group-5" transform="translate(976.000000, 404.000000)">
                <polygon
                  id="Path"
                  points="23 10.41 21.59 9 16 14.59 10.41 9 9 10.41 14.59 16 9 21.59 10.41 23 16 17.41 21.59 23 23 21.59 17.41 16"
                ></polygon>
              </g>
            </g>
          </g>
        </svg>
      </button>
    </div>
    <iframe
      :src="staticIframeSrc"
      width="100%"
      height="450"
      frameborder="0"
      style="border: 0"
      allowfullscreen=""
      aria-hidden="false"
      tabindex="0"
    ></iframe>
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";

export default {
  name: "EmbedCode",
  components: {},
  props: {
    position: Object,
    layers: Array,
    mapId: String,
  },
  emits: ["close-modal"],
  data() {
    return {
      buttonText: "HTML kopiëren",
      currentPosition: this.position,
      currentLayers: this.layers,
      staticIframeSrc: "",
    };
  },
  computed: {
    ...mapState(useGlobalStore, ["map"]),
    embedUrl() {
      const baseLayer = this.currentLayers.filter((l) => l.is_visible && l.is_base).map((l) => l.id);
      const urlPrefix = this.mapId !== "primary" ? `/atlas/maps/${this.mapId}/` : "/atlas/";

      return `${encodeURI(window.location.origin)}${urlPrefix}@${encodeURIComponent(
        this.currentPosition.center[0],
      )},${encodeURIComponent(this.currentPosition.center[1])},${encodeURIComponent(
        Math.round(this.currentPosition.zoom * 100) / 100,
      )}z/layers=${this.visibleLayers.map((l) => encodeURIComponent(l.id)).join(",")}/base=${
        baseLayer.length > 0 ? baseLayer[0] : ""
      }/is_embed=true`;
    },
    embedCode() {
      return `<iframe src="${this.embedUrl}" width="560" height="450" frameborder="0" style="border:0;" allowfullscreen="" aria-hidden="false" tabindex="0"></iframe>`;
    },
    visibleLayers() {
      return this.currentLayers.filter((layer) => layer.is_visible && !layer.is_base);
    },
  },
  mounted() {
    // Set the static iframe src once on mount, based on initial props
    const baseLayer = this.layers.filter((l) => l.is_visible && l.is_base).map((l) => l.id);
    const urlPrefix = this.mapId !== "primary" ? `/atlas/maps/${this.mapId}/` : "/atlas/";
    const visibleLayers = this.layers.filter((layer) => layer.is_visible && !layer.is_base);

    this.staticIframeSrc = `${encodeURI(window.location.origin)}${urlPrefix}@${encodeURIComponent(
      this.position.center[0],
    )},${encodeURIComponent(this.position.center[1])},${encodeURIComponent(
      Math.round(this.position.zoom * 100) / 100,
    )}z/layers=${visibleLayers.map((l) => encodeURIComponent(l.id)).join(",")}/base=${
      baseLayer.length > 0 ? baseLayer[0] : ""
    }/is_embed=true`;

    window.addEventListener("message", this.handleIframeMessage);
  },
  unmounted() {
    window.removeEventListener("message", this.handleIframeMessage);
  },
  methods: {
    handleIframeMessage(event) {
      // Verify the message is from our iframe
      if (event.origin !== window.location.origin) {
        return;
      }

      if (event.data.type === "map-state-update") {
        if (event.data.position) {
          this.currentPosition = event.data.position;
        }
        if (event.data.layers) {
          this.currentLayers = event.data.layers;
        }
      }
    },
    closeModal() {
      this.$emit("close-modal");
    },
    copyHTML() {
      if (!this.$refs.input) {
        return;
      }

      this.$refs.input.select();

      try {
        document.execCommand("copy");

        this.buttonText = "Gekopieerd!";
        setTimeout(() => {
          this.buttonText = "HTML kopiëren";
        }, 2000);
      } catch {
        console.error("Could not copy text");
      }
    },
  },
};
</script>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  border-bottom: 1px solid var(--color-grey-50);
}

.iconbutton {
  width: var(--width-button-large);
  height: var(--width-button-large);
  border-left: 1px solid var(--color-grey-50);
}

.input {
  height: var(--width-button-large);
  padding: 0 0 0 12px;
  width: 100%;
  font-size: var(--font-size-small);
}
</style>
