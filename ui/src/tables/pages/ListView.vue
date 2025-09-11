<template>
  <div class="container">
    <div class="section">
      <SearchFormTable
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
        <div v-if="rows && rows.length > 0 && visiblePagination">
          <Paginator
            :first="page * items_per_page - 1"
            :rows="items_per_page"
            :total-records="total_items"
            :rows-per-page-options="[10, 20, 30, 40, 50]"
            @page="updatePageState"
          ></Paginator>
        </div>
        <div v-if="!loading && !error && rows && rows.length == 0">Er zijn geen resultaten gevonden.</div>
      </div>
    </div>
  </div>
</template>

<script>
import nunjucks from "nunjucks";
import fetchDot from "fetch-dot";
import SearchFormTable from "../components/SearchFormTable.vue";
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";

export default {
  name: "ListView",
  components: {
    SearchFormTable,
  },
  data() {
    return {
      error: null,
      rows: null,
      page: 1,
      items_per_page: 10,
      total_items: null,
      searchFields: {},
      loading: false,
      url: null,
    };
  },
  computed: {
    ...mapState(useGlobalStore, ["tables"]),
    table() {
      const results = this.tables.filter((table) => table.slug === this.$route.params.tableSlug);

      return results.length > 0 ? results[0] : null;
    },
    visiblePagination() {
      return !!this.page && this.total_items > this.items_per_page;
    },
  },
  mounted() {
    const fullUrl = this.table.source.url + this.table.endpoint;
    this.url = new URL(fullUrl);
  },
  methods: {
    async getTableItems(url, searchFields) {
      this.rows = [];
      this.error = null;
      this.loading = true;

      if (this.table.page_attribute && this.table.items_per_page_attribute) {
        this.url.searchParams.set(this.table.items_per_page_attribute, this.items_per_page ? this.items_per_page : 10);
        this.url.searchParams.set(this.table.page_attribute, this.page ? this.page : 1);
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

        this.rows = this.table.list_query ? fetchDot(this.table.list_query, data) : fetchDot("", data);
        this.total_items = this.table.total_items_page_attribute
          ? fetchDot(this.table.total_items_page_attribute, data)
          : null;
      } catch (e) {
        this.error = "Er is een fout opgetreden tijdens het ophalen van de gegevens.";
      }

      this.loading = false;
    },
    async onSearch(searchFields) {
      if (!this.table || this.table.method !== "GET") return;

      this.searchFields = searchFields;
      // Reset the page on search to prevent issues, such as navigating from page 4 to a new search with fewer results, which could lead to a 404 error.
      this.page = 1;

      const searchFieldsWithoutUndefinedValues = Object.entries(searchFields)
        .filter(([, value]) => value !== undefined)
        .reduce((obj, [key, value]) => {
          obj[key] = value;
          return obj;
        }, {});

      const params = new URLSearchParams(searchFieldsWithoutUndefinedValues);
      this.url.search = params.toString();

      await this.getTableItems(this.url, searchFields);
    },
    renderString(template, context) {
      return nunjucks.renderString(template, context);
    },
    async updatePageState(pageState) {
      this.page = pageState.page + 1;
      this.items_per_page = pageState.rows;

      await this.getTableItems(this.url, this.searchFields);
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
