<template>
  <div class="overlay">
    <button class="background" @click="closeModal" />
    <div class="modal">
      <EmbedCode
        :position="position"
        :layers="layers"
        @close-modal="closeModal"
      />
    </div>
  </div>
</template>

<script>
import EmbedCode from "./EmbedCode";

export default {
  name: "EmbedModal",
  components: {
    EmbedCode,
  },
  props: {
    position: Object,
    layers: Array,
  },
  methods: {
    closeModal() {
      this.$emit("toggle-modal", "");
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

.iconbutton {
  width: var(--width-button-normal);
  height: var(--width-button-normal);
  border-top-left-radius: var(--radius-normal);
  border-top-right-radius: var(--radius-normal);
  background: white;
  box-shadow: var(--shadow-normal);
}

.modal {
  position: relative;
  margin-bottom: 41px;
  background-color: white;
  border-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);
  width: 600px;
  max-width: 100%;
  overflow: hidden;
}
</style>
