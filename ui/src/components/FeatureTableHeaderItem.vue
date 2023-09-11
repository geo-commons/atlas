<template>
  <div class="flex flex-column">
    <div class="table-header-container">
      <span class="header-text" @click="() => sortColumn()">
        {{ headerText }}
      </span>
      <button
        v-tippy="{ placement: 'bottom' }"
        aria-label="Sorteer kolom"
        content="Sorteer"
        class="flex-center"
        @click="() => sortColumn()"
      >
        <span class="icon-min-width flex-center">
          <ArrowUpIcon v-if="property === sortKey && sortAscending" />
          <ArrowDownIcon v-if="property === sortKey && !sortAscending" />
        </span>
      </button>
    </div>
  </div>
</template>

<script>
import ArrowDownIcon from "../icons/ArrowDownIcon.vue";
import ArrowUpIcon from "../icons/ArrowUpIcon.vue";

export default {
  name: "FeatureTableHeaderItem",
  components: {
    ArrowUpIcon,
    ArrowDownIcon,
  },
  props: {
    layer: Object,
    property: String,
    sortKey: String,
    sortAscending: Boolean,
  },
  computed: {
    headerText() {
      return this.layer.friendly_fields &&
        this.layer.friendly_fields[this.property]
        ? this.layer.friendly_fields[this.property]
        : this.property;
    },
  },
  methods: {
    sortColumn() {
      this.$emit("sort", this.property);
    },
  },
};
</script>

<style scoped>
.table-header-container {
  display: flex;
  font-weight: var(--font-weight-normal);
  gap: 3px;
  text-transform: capitalize;
  justify-content: flex-start;
}

.header-text {
  cursor: pointer;
}

.icon-min-width {
  min-width: 24px;
}
</style>
