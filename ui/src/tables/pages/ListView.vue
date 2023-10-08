<template>
  <div class="container">
    <div class="section">
      <SearchForm v-if="table.search_fields.length > 0" :table="table" @submit="onSearch" />
    </div>
    <div class="section">
      <span v-if="!table">Kan deze tabel niet vinden</span>
      <div v-if="table">
        <div v-if="error">{{ error }}</div>
        <table v-if="rows && rows.length > 0" class="table">
          <thead>
            <tr>
              <th v-for="field in table.list_headings" :key="field">
                {{ field }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, i) in rows" :key="i">
              <td v-for="field in table.list_fields" :key="field">
                {{ renderString(field, row) }}
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="!loading && !error && rows && rows.length == 0">Er zijn geen resultaten gevonden.</div>
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
      rows: null,
      loading: false,
    };
  },
  computed: {
    ...mapState({
      tables: (state) => state.tables,
    }),
    table() {
      const results = this.tables.filter((table) => table.slug == this.$route.params.tableSlug);

      return results.length > 0 ? results[0] : null;
    },
  },
  methods: {
    async onSearch(searchFields) {
      this.searchFields = searchFields;
      this.rows = [];
      this.error = null;
      this.loading = true;

      const url = new URL(this.table.source.url + this.table.endpoint);

      if (this.table.method == "GET") {
        const params = new URLSearchParams(searchFields);
        url.search = params.toString();
      }

      const result = await fetch(url.toString(), {
        method: this.table.method,
        body: this.table.method !== "GET" ? JSON.stringify(searchFields) : null,
      });

      if (!result.ok) {
        this.error = "Er is een fout opgetreden tijdens het ophalen van de gegevens.";
      }

      const data = await result.json();
      this.rows = fetchDot(this.table.list_query, data);
      this.loading = false;
    },
    renderString(template, context) {
      return nunjucks.renderString(template, context);
    },
  },
};
</script>

<style scoped>
.section {
  padding: 30px 0 0 0;
}
.table {
  width: 100%;
  border: solid 1px var(--color-grey-60);
  border-radius: 6px;
}

.table thead tr {
  background: var(--color-grey-50);
  border: 0;
}

.table thead tr th {
  text-align: left;
  font-weight: var(--font-weight-normal);
  padding: 12px 4px;
}

.table tbody td {
  padding: 12px 4px;
}
</style>
