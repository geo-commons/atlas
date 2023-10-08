<template>
  <div class="search-form">
    <validation-observer v-slot="{ handleSubmit }">
      <form method="POST" @submit.prevent="handleSubmit(onSearch)">
        <div class="grid">
          <div v-for="searchField in table.search_fields" :key="searchField" class="item">
            <validation-provider v-slot="{ errors }" name="Titel">
              <label :for="searchField.name">{{ searchField.label }}</label
              ><input
                :id="searchField.name"
                v-model="searchFields[searchField.name]"
                :type="searchField.type ? searchField.type : 'text'"
                :name="searchField.name"
              />
              <span>{{ errors[0] }}</span>
            </validation-provider>
          </div>
        </div>
        <button type="submit" class="button __primary">Zoek</button>
      </form>
    </validation-observer>
  </div>
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
