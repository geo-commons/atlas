<template>
  <vue-tippy
    :arrow="false"
    placement="bottom-start"
    theme="popover"
    trigger="click"
    :onShown="() => $refs.valueInput.focus()"
    :distance="8"
    :delay="[0, 0]"
    :a11y="false"
  >
    <template v-slot:trigger>
      <button class="iconbutton">
        {{
          layer.friendly_fields && layer.friendly_fields[property]
            ? layer.friendly_fields[property]
            : property
        }}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="20px"
          width="20px"
          viewBox="0 96 960 960"
        >
          <path d="M480 711 240 471l43-43 197 198 197-197 43 43-240 239Z" />
        </svg>
      </button>
      {{ fieldFilters && fieldFilters[property] ? fieldFilters[property] : "" }}
    </template>
    <div class="container">
      <form method="POST" @submit="updateFilter">
        <input ref="valueInput" type="text" v-model="value" placeholder="Filter op waarde" />
        <button type="submit">Opslaan</button>
      </form>
    </div>
  </vue-tippy>
</template>

<script>
export default {
  name: "FilterTooltip",
  props: {
    layer: Object,
    property: String,
    fieldFilters: Object,
  },
  data() {
    return {
      value: this.FieldFilters && this.fieldFilters[this.property] ? this.fieldFilters[this.property] : "",
    };
  },
  watch: {
    fieldFilters(newValue) {
      console.log(newValue)
    }
  },
  methods: {
    updateFilter(e) {
      e.preventDefault()

      if (this.value) {
        this.$emit('change', {
            ...this.fieldFilters,
            [this.property]: this.value,
          })
        return
      }

      const newFieldFilter = { ...this.fieldFilters }
      delete newFieldFilter[this.property]
      this.$emit('change', newFieldFilter)
    },
  },
};
</script>

<style scoped>
.container {
  padding: 10px 16px;
}
</style>