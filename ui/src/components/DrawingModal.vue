<template>
  <div class="overlay">
    <button class="background" @click="closeModal" />
    <div class="modal">
      <div class="explanation">
        De tekening is opgeslagen. Gebruik de volgende link om de tekening te
        delen met anderen:
      </div>

      <div class="group">
        <input
          ref="input"
          type="text"
          :value="drawingUrl"
          class="input"
          readonly
        />
        <button
          class="iconbutton"
          type="button"
          aria-label="Link kopiëren"
          @click="copyLink"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24"
            viewBox="0 0 24 24"
            width="24"
          >
            <path d="M0 0h24v24H0V0z" fill="none" />
            <path
              d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DrawingModal",
  components: {},
  props: {
    drawing: String,
    layers: Array,
    position: Object,
  },
  computed: {
    drawingUrl() {
      return window.location;
    },
  },
  methods: {
    closeModal() {
      this.$emit("toggle-modal", "");
    },
    copyLink() {
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
      } catch (err) {
        console.error("Could not copy text");
      }
    },
  },
};
</script>

<style scoped>
.overlay {
  position: fixed;
  z-index: 10;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow-y: auto;
}

.background {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
}

.buttons {
  position: absolute;
  top: calc((var(--width-button-normal) + 8px) * -1);
  right: -8px;
  padding: 8px 8px 0;
  overflow: hidden;
}

.modal {
  position: relative;
  padding: var(--padding-screen);
  margin-bottom: 41px;
  background-color: #ffffff;
  border-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);
  width: 600px;
  max-width: 100%;
  overflow: hidden;
}

.group {
  display: flex;
  margin-top: 20px;
  border: 1px solid var(--color-grey-50);
  border-radius: var(--radius-normal);
}

.input {
  height: var(--width-button-large);
  padding: 0 0 0 12px;
  width: 100%;
  font-size: var(--font-size-small);
}

.iconbutton {
  width: var(--width-button-large);
  height: var(--width-button-large);
  border-left: 1px solid var(--color-grey-50);
}
</style>
