<template>
  <div>
    <Spinner v-if="loading" class="spinner" :style-type="'portal'" />
    <div v-if="!loading && error" class="warning-text">Er is iets fout gegaan bij het laden van de kaart</div>
    <iframe
      v-show="!loading && !error"
      class="embed-iframe"
      :src="embedUrl"
      aria-hidden="false"
      tabindex="0"
      @load="onIframeLoad"
      @error="onIframeError"
    ></iframe>
  </div>
</template>

<script>
import Spinner from "@/components/Spinner.vue";

export default {
  name: "EmbedAtlasFrame",
  components: { Spinner },
  props: { embedUrl: String },
  data() {
    return {
      loading: true,
      error: false,
    };
  },
  methods: {
    onIframeLoad() {
      this.loading = false; // Hide spinner when iframe loads
      this.error = false; // Reset error if load is successful
    },
    onIframeError() {
      this.loading = false; // Hide spinner when iframe fails
      this.error = true; // Show error message if something goes wrong
    },
  },
};
</script>

<style scoped>
.embed-iframe {
  border: 1px solid var(--color-grey-60);
  height: 300px;
  width: 100%;
}

@media (min-width: 1024px) {
  .embed-iframe {
    height: 400px;
  }
}
</style>
