<template>
  <div class="theme-field">
    <multiselect
      v-model="inputVal"
      v-bind="field"
      :options="availableThemes"
      :multiple="true"
      label="title"
      track-by="title"
      placeholder="Kies thema's"
      deselect-label="Druk op enter om te verwijderen"
      select-label="Druk op enter om te selecteren"
      selected-label="Geselecteerd"
    >
    </multiselect>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import Multiselect from "vue-multiselect";

export default defineComponent({
  name: "ThemeField",
  components: { Multiselect },
  props: {
    field: Object,
    sources: Array,
    value: Array,
  },
  emits: ["update:modelValue"],
  data() {
    return {
      availableThemes: [],
    };
  },
  computed: {
    inputVal: {
      get() {
        return Array.isArray(this.value) ? this.value : [];
      },
      set(val) {
        this.$emit("input", val);
      },
    },
  },
  created() {
    this.getThemes();
  },
  methods: {
    async getThemes() {
      const result = await fetch("/atlas/api/v1/themes/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch themes");
      }

      const response = await result.json();

      this.availableThemes = response.map((theme) => {
        return { id: theme.id, title: theme.title };
      });
    },
  },
});
</script>

<style scoped>
.theme-field :deep(.multiselect .multiselect__input) {
  padding: 0;
}

.theme-field :deep(.multiselect) {
  padding: 0px;
}

.theme-field :deep(.multiselect__tags) {
  padding: 8px 40px 0 16px;
  font-size: 16px;
}

.theme-field :deep(.multiselect__single) {
  padding: 0;
  margin-bottom: 0;
}
</style>
