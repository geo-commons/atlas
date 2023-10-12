<template>
  <transition name="modal-fade">
    <div class="modal-backdrop">
      <div class="modal" role="dialog">
        <header class="modal-header">
          <slot name="header"></slot>
          <button type="button" class="iconbutton __normal __round" aria-label="Close Modal" @click="close"><close-icon-large /></button>
        </header>

        <main class="modal-body">
          <slot name="body"></slot>
        </main>
      </div>
    </div>
  </transition>
</template>

<script>
import CloseIconLarge from "@/icons/CloseIconLarge.vue";

export default {
  name: "FormModal",
  components: { CloseIconLarge },
  props: {},
  data() {
    return {};
  },
  computed: {},
  mounted() {},
  methods: {
    close() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: var(--color-white);
  box-shadow: var(--shadow-normal);
  overflow-x: auto;
  display: flex;
  flex-direction: column;
  width: 80%;
}

.modal-header {
  position: relative;
  padding: 0 15px;
  display: flex;
  border-bottom: 1px solid var(--color-grey-60);
  justify-content: space-between;
  align-items: center;
}

.modal-body {
  padding: 20px 15px;
}

.modal-fade-enter,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
</style>
