<template>
  <vue-tippy
    :arrow="false"
    placement="bottom-start"
    theme="popover"
    trigger="click"
    :on-shown="() => $refs.valueInput.focus()"
    :distance="8"
    :delay="[0, 0]"
    :a11y="false"
  >
    <template v-slot:trigger>
      <button
        class="iconbutton"
        aria-label="Filter kolom"
        content="Filter"
        v-tippy="{ placement: 'bottom' }"
      >
        <FilterIcon />
      </button>
    </template>
    <div class="container">
      <form method="POST" @submit="updateFilter">
        <input
          ref="valueInput"
          type="text"
          v-model="value"
          placeholder="Filter op waarde"
        />
        <button type="submit">Toepassen</button>
      </form>
    </div>
  </vue-tippy>
</template>

<script>
import FilterIcon from "../icons/FilterIcon.vue";

export default {
  name: "FilterTooltip",
  components: {
    FilterIcon,
  },
  props: {
    layer: Object,
    property: String,
    fieldFilters: Object,
  },
  data() {
    return {
      value:
        this.FieldFilters && this.fieldFilters[this.property]
          ? this.fieldFilters[this.property]
          : "",
    };
  },
  watch: {
    fieldFilters(newValue) {
      console.log(newValue);
    },
  },
  methods: {
    updateFilter(e) {
      e.preventDefault();

      if (this.value) {
        this.$emit("change", {
          ...this.fieldFilters,
          [this.property]: this.value,
        });
        return;
      }

      const newFieldFilter = { ...this.fieldFilters };
      delete newFieldFilter[this.property];
      this.$emit("change", newFieldFilter);
    },
  },
};
</script>

<style scoped>
.container {
  padding: 10px 16px;
}
</style>
