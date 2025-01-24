<template>
  <div>
    <div class="select-button-wrapper">
      <button class="select-button" :aria-controls="id" @click="onSelectItem">
        <div class="name">
          {{ title }}
          <span v-if="countOfActiveFiltersOnLayer > 0" class="active-filter">
            ({{
              countOfActiveFiltersOnLayer > 1 ? `${countOfActiveFiltersOnLayer} actieve filters` : `1 actief filter`
            }})
          </span>
        </div>
        <ChevronRightIcon class="icon __medium" />
      </button>
    </div>
  </div>
</template>

<script>
import ChevronRightIcon from "../assets/icons/chevron-right-icon.svg";
import { useMapStore } from "@/stores/map_store";

export default {
  name: "SelectButton",
  components: { ChevronRightIcon },
  props: {
    id: String,
    title: String,
    mapId: String,
  },
  data() {
    return {
      store: null,
    };
  },
  computed: {
    countOfActiveFiltersOnLayer() {
      return this.store.getActiveFilterCountForLayer(this.id);
    },
  },
  created() {
    this.store = useMapStore(this.mapId);
  },
  methods: {
    onSelectItem() {
      this.$emit("select-item", this.id);
    },
  },
};
</script>

<style scoped>
.select-button-wrapper {
  display: flex;
}

.select-button {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 14px;
  font-weight: var(--font-weight-bold);
  padding-left: var(--padding-screen);
}

.select-button:not([disabled]):hover {
  background: var(--color-grey-40);
}

.select-button:not([disabled]):active {
  background: var(--color-grey-50);
}

.name {
  padding: 6px 0;
}

.active-filter {
  color: var(--color-grey-80);
  font-weight: var(--font-weight-normal);
}
</style>
