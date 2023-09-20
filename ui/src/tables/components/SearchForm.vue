<template>
  <validation-observer v-slot="{ handleSubmit }">
    <form method="POST" @submit.prevent="handleSubmit(onSearch)">
      <validation-provider
        v-for="searchField in table.search_fields"
        :key="searchField"
        v-slot="{ errors }"
        name="Titel"
      >
        <label :for="searchField">{{ searchField }}</label
        ><input
          v-model="searchFields[searchField]"
          type="text"
          :name="searchField"
        />
        <span>{{ errors[0] }}</span>
      </validation-provider>

      <button type="submit">Zoek</button>
    </form>
  </validation-observer>
</template>

<script>
import { ValidationObserver, ValidationProvider } from "vee-validate";

export default {
  name: "SearchForm",
  components: {
    ValidationObserver,
    ValidationProvider,
  },
  props: {
    table: Object,
  },
  data() {
    return {
      searchFields: {},
    };
  },
  methods: {
    onSearch() {
      this.$emit("submit", this.searchFields);
    },
  },
};
</script>
