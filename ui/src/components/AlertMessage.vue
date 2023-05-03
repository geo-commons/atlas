<template>
  <div v-if="alert" class="wrapper">
    <div class="message">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        height="24px"
        viewBox="0 0 24 24"
        width="24px"
        fill="currentColor"
      >
        <path
          d="M11 15h2v2h-2v-2zm0-8h2v6h-2V7zm.99-5C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"
        />
      </svg>
      <span>{{ alert }}</span>
      <button
        v-tippy
        class="iconbutton"
        type="button"
        content="Sluit"
        aria-label="Sluit"
        @click="onClose"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 0 24 24"
          width="24px"
          fill="#000000"
        >
          <polygon
            id="Path"
            fill-rule="nonzero"
            points="15.59 7 12 10.59 8.41 7 7 8.41 10.59 12 7 15.59 8.41 17 12 13.41 15.59 17 17 15.59 13.41 12 17 8.41"
          ></polygon>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "AlertMessage",
  props: {
    alert: String,
  },
  methods: {
    onClose() {
      this.$store.commit("setAlert", "");
    },
  },
};
</script>

<style scoped>
.wrapper {
  position: fixed;
  left: 0;
  right: 0;
  bottom: var(--padding-screen);
  display: flex;
  justify-content: center;
  z-index: 2;
  pointer-events: none;
}

.message {
  display: flex;
  align-items: center;
  height: var(--width-button-normal);
  padding: 0 4px;
  color: var(--color-alert);
  background-color: white;
  border-radius: var(--width-button-normal);
  box-shadow: var(--shadow-normal);
  pointer-events: auto;
}

.wrapper span {
  margin-left: 4px;
}

.iconbutton {
  width: var(--width-button-small);
  height: var(--width-button-small);
  border-radius: var(--width-button-small);
  margin: 0 2px;
}
</style>
