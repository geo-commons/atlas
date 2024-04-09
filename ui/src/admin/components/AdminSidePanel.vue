<template>
  <aside class="admin-side-panel">
    <div class="header">
      <slot name="header"></slot>
    </div>

    <div class="content">
      <slot v-if="!loading"></slot>
      <Spinner v-else style-type="'admin'" />
    </div>
  </aside>
</template>

<script>
import Spinner from "@/components/Spinner.vue";

export default {
  name: "AdminSidePanel",
  components: {
    Spinner,
  },
  props: {
    loading: Boolean,
  },
};
</script>

<style scoped>
.admin-side-panel {
  font-family: var(--font-family-admin);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  position: relative;
  width: var(--width-detail);
  z-index: 1;
  box-shadow: var(--shadow-normal);
}

:slotted(.admin-side-panel h1) {
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-bold);
  display: flex;
  flex-grow: 1;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

:slotted(.admin-side-panel h2) {
  margin: 24px 0 8px;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-bold);
}

:slotted(.admin-side-panel .margin-content) {
  margin: 0 12px;
}

.header {
  display: flex;
  align-items: center;
  flex: 0 1 auto;
  width: 100%;
  padding: var(--padding-screen);
  border-bottom: 1px solid var(--color-grey-60);
}

.content {
  position: relative;
  overflow-y: auto;
  flex: 1 1 auto;
  height: 100%;
  padding-bottom: var(--padding-screen);
}
</style>
