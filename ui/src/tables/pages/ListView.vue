<template>
  <div class="container">
    <div class="section">
      <SearchForm
        v-if="table.search_fields.length > 0"
        :table="table"
        :disable-data-panel-button="true"
        @submit="onSearch"
      />
    </div>
    <div class="section">
      <span v-if="!table">Kan deze tabel niet vinden</span>
      <div v-if="table">
        <div v-if="error">{{ error }}</div>
        <table v-if="rows && rows.length > 0" class="table">
          <thead>
            <tr>
              <th v-for="(field, i) in table.list_headings" :key="i">
                {{ field }}
              </th>
            </tr>
          </thead>
          <tbody v-if="rows && rows.length > 0">
            <tr v-for="(row, i) in rows" :key="i">
              <td v-for="(field, j) in table.list_fields" :key="j">
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
import fetchDot from "fetch-dot";
import SearchForm from "../components/SearchForm";
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";

export default {
  name: "ListView",
  components: {
    SearchForm,
  },
  data() {
    return {
      error: null,
      rows: null,
      loading: false,
    };
  },
  computed: {
    ...mapState(useGlobalStore, ["tables"]),
    table() {
      const results = this.tables.filter((table) => table.slug == this.$route.params.tableSlug);

      return results.length > 0 ? results[0] : null;
    },
  },
  methods: {
    async onSearch(searchFields) {
      this.rows = [];
      this.error = null;
      this.loading = true;

      const url = new URL(this.table.source.url + this.table.endpoint);

      if (this.table.method == "GET") {
        const searchFieldsWithoutUndefinedValues = Object.entries(searchFields)
          .filter(([, value]) => value !== undefined)
          .reduce((obj, [key, value]) => {
            obj[key] = value;
            return obj;
          }, {});

        const params = new URLSearchParams(searchFieldsWithoutUndefinedValues);
        url.search = params.toString();
      }

      const result = await fetch(url.toString(), {
        method: this.table.method,
        body: this.table.method === "POST" ? JSON.stringify(searchFields) : null,
        headers: this.table.method === "POST" ? { "Content-Type": "application/json" } : {},
      });

      try {
        const data = await result.json();

        if (!result.ok) {
          if (result.status == 401) {
            this.error = "U moet ingelogd zijn om deze data te bekijken.";
          } else if (result.status == 403) {
            this.error = "U heeft geen rechten om deze data te bekijken.";
          } else {
            if (this.table.error_template && data) {
              this.error =
                nunjucks.renderString(this.table.error_template, data) ||
                "Er is een fout opgetreden tijdens het ophalen van de gegevens";
            } else {
              this.error = "Er is een fout opgetreden tijdens het ophalen van de gegevens.";
            }
          }
        }

        this.rows = fetchDot(this.table.list_query, data);
      } catch (e) {
        this.error = "Er is een fout opgetreden tijdens het ophalen van de gegevens.";
      }

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
