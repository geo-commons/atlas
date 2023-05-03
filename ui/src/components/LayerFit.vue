<template>
  <div>
    <button
      v-tippy="{ placement: 'right' }"
      class="iconbutton"
      content="Zoom naar laag"
      aria-label="Zoom naar laag"
      @click="onClick"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        height="18px"
        viewBox="0 0 24 24"
        width="18px"
        fill="#000000"
      >
        <path d="M0 0h24v24H0V0z" fill="none" />
        <path
          d="M3 5v4h2V5h4V3H5c-1.1 0-2 .9-2 2zm2 10H3v4c0 1.1.9 2 2 2h4v-2H5v-4zm14 4h-4v2h4c1.1 0 2-.9 2-2v-4h-2v4zm0-16h-4v2h4v4h2V5c0-1.1-.9-2-2-2z"
        />
      </svg>
    </button>
  </div>
</template>

<script>
export default {
  name: "LayerFit",
  components: {},
  props: {
    layer: Object,
  },
  methods: {
    onClick(e) {
      this.$emit("click", e);
    },
  },
};
</script>

<style scoped>
.iconbutton {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  opacity: 0;
}

.layer:hover .iconbutton,
.sublayer:hover .iconbutton,
.tippy-active > .iconbutton,
.keyboard-user .iconbutton:focus {
  opacity: 1;
}
</style>
