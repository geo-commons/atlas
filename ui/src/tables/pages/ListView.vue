<template>
  <div>
    <span v-if="!table">Kan deze tabel niet vinden</span>
    <div v-if="table">
      <SearchForm
        v-if="table.search_fields.length > 0"
        :table="table"
        @submit="onSearch"
      />
      <div v-if="error">{{ error }}</div>
      <table v-if="rows && rows.length > 0">
        <tr>
          <th v-for="field in table.list_headings" :key="field">
            {{ field }}
          </th>
        </tr>
        <tr v-for="(row, i) in rows" :key="i">
          <td v-for="field in table.list_fields" :key="field">
            {{ renderString(field, row) }}
          </td>
        </tr>
      </table>
      <div v-if="!error && (!rows || rows.length == 0)">
        Er zijn geen resultaten gevonden.
      </div>
    </div>
  </div>
</template>

<script>
import nunjucks from "nunjucks";
import { mapState } from "vuex";
import fetchDot from "fetch-dot";
import SearchForm from "../components/SearchForm";

export default {
  name: "ListView",
  components: {
    SearchForm,
  },
  data() {
    return {
      searchFields: {},
      error: null,
      rows: [],
    };
  },
  computed: {
    ...mapState({
      tables: (state) => state.tables,
    }),
    table() {
      const results = this.tables.filter(
        (table) => table.slug == this.$route.params.tableSlug
      );

      return results.length > 0 ? results[0] : null;
    },
  },
  methods: {
    async onSearch(searchFields) {
      this.searchFields = searchFields;
      this.data = [];
      this.error = null;

      const url = new URL(this.table.source.url + this.table.endpoint);
      const result = await fetch(url.toString(), {
        method: this.table.method,
        body: this.table.method !== "GET" ? JSON.stringify(searchFields) : null,
      });

      if (!result.ok) {
        this.error =
          "Er is een fout opgetreden tijdens het ophalen van de gegevens.";
      }

      const data = await result.json();
      this.rows = fetchDot(this.table.list_query, data);
    },
    renderString(template, context) {
      return nunjucks.renderString(template, context);
    },
  },
};
</script>
