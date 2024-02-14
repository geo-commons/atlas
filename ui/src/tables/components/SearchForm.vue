<template>
  <div class="search-form">
    <vee-form @submit="onSearch">
      <div class="grid">
        <div v-for="(searchField, i) in table.search_fields" :key="i" class="item">
          <label :for="searchField.name">
            {{ searchField.label }}
          </label>
          <vee-field
            :id="searchField.name"
            v-model="searchFields[searchField.name]"
            :type="searchField.type ? searchField.type : 'text'"
            :name="searchField.name"
          />
          <span><vee-error-message :name="searchField.name" /></span>
        </div>
      </div>
      <button type="submit" class="button __primary">Zoek</button>
    </vee-form>
  </div>
</template>

<script>
import { Form as VeeForm, Field as VeeField, ErrorMessage as VeeErrorMessage } from "vee-validate";

export default {
  name: "SearchForm",
  components: {
    VeeForm,
    VeeField,
    VeeErrorMessage,
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

<style scoped>
.search-form {
  background-color: var(--color-grey-40);
  padding: 20px;
  border-radius: var(--radius-normal);
}

.grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  row-gap: 20px;
  column-gap: 20px;
}
.item {
  color: black;
}

.item label {
  font-weight: var(--font-weight-bold);
  display: block;
  margin-bottom: 5px;
}

.item input {
  background-color: white;
  width: 100%;
  padding: 5px;
  border-radius: var(--radius-small);
}

.button {
  margin-top: 20px;
}
</style>
