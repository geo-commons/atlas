<template>
  <button
    v-tippy="{ placement: 'bottom' }"
    class="iconbutton toggle-button"
    :class="{ isActive: showDataPanel }"
    type="button"
    :content="showDataPanel ? 'Verberg data' : 'Toon data'"
    :aria-label="showDataPanel ? 'Verberg data' : 'Toon data'"
    @click="toggleDataPanel"
  >
    <FormIcon />
  </button>
  <transition name="fade">
    <div v-if="activeFilters > 0" class="counter visible-layer-counter">{{ activeFilters }}</div>
  </transition>
</template>

<script>
import FormIcon from "../assets/icons/form-icon.svg";
import { useMapStore } from "@/stores/map_store";

export default {
  name: "DataPanelButton",
  components: {
    FormIcon,
  },
  props: {
    showDataPanel: Boolean,
    mapId: String,
  },
  emits: ["show-data-panel"],
  data() {
    return {
      store: null,
    };
  },
  computed: {
    activeFilters() {
      return this.store.getActiveLayersWithFilterCount;
    },
  },
  created() {
    this.store = useMapStore(this.mapId);
  },
  methods: {
    toggleDataPanel() {
      this.$emit("show-data-panel");
    },
  },
};
</script>

<style scoped>
.toggle-button {
  width: var(--width-button-large);
  border-right: 1px solid var(--color-grey-50);
  position: relative;
}

.iconbutton:not([disabled]):hover:before {
  background: var(--color-grey-40);
}

.iconbutton:not([disabled]):active:before {
  background: var(--color-grey-50);
}

.counter {
  flex-shrink: 0;
  height: 18px;
  min-width: 18px;
  border-radius: 9px;
  border: 2px solid var(--color-primary);
  padding: 0 3px;
  background: white;
  color: var(--color-primary);
  font-size: 11px;
  font-weight: var(--font-weight-bold);
  line-height: 14px;
  text-align: center;
  white-space: nowrap;
  user-select: none;
  z-index: 50;
}

.visible-layer-counter {
  position: absolute;
  left: 30px;
  top: 2px;
}
</style>
