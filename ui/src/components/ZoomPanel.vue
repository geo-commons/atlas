<template>
  <div class="wrapper">
    <button
      v-tippy="{ placement: 'left' }"
      class="iconbutton"
      content="Zoom in"
      aria-label="Zoom in"
      @click="zoomIn"
    >
      <svg
        width="10px"
        height="10px"
        viewBox="0 0 10 10"
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
      >
        <g
          id="Symbols"
          stroke="none"
          stroke-width="1"
          fill="none"
          fill-rule="evenodd"
        >
          <polygon
            id="Path"
            fill="#000000"
            points="4 10 6 10 6 6 10 6 10 4 6 4 6 0 4 0 4 4 0 4 0 6 4 6"
          ></polygon>
        </g>
      </svg>
    </button>
    <button
      v-tippy="{ placement: 'left' }"
      class="iconbutton"
      content="Zoom uit"
      aria-label="Zoom uit"
      @click="zoomOut"
    >
      <svg
        width="10px"
        height="2px"
        viewBox="0 0 10 2"
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
      >
        <g
          id="Symbols"
          stroke="none"
          stroke-width="1"
          fill="none"
          fill-rule="evenodd"
        >
          <polygon
            id="Path"
            fill="#000000"
            points="10 2 10 0 0 0 0 2"
          ></polygon>
        </g>
      </svg>
    </button>
  </div>
</template>

<script>
export default {
  name: "ZoomPanel",
  props: {
    position: Object,
  },
  methods: {
    zoomIn() {
      this.$emit("set-position", {
        ...this.position,
        zoom: this.position.zoom + 1,
      });
    },
    zoomOut() {
      this.$emit("set-position", {
        ...this.position,
        zoom: this.position.zoom - 1,
      });
    },
  },
};
</script>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: var(--radius-normal);
  overflow: hidden;
  box-shadow: var(--shadow-normal);
}

.iconbutton {
  width: var(--width-button-normal);
  height: var(--width-button-normal);
}

.iconbutton:not(:last-child) {
  box-sizing: content-box;
  border-bottom: 1px solid var(--color-grey-50);
}
</style>
