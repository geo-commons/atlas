<template>
  <ExpandButton :title="template.title" class="template">
    <p v-if="error">{{ error }}</p>
    <div v-if="!error && template.headers.length > 0" class="table-wrapper">
      <table class="template-table">
        <thead>
          <tr>
            <th v-for="(heading, key) in template.headers" :key="key" class="template-table-header">
              {{ heading }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(record, key) in fetchedData" :key="key">
            <td v-for="(field, key) in template.fields" :key="key" class="template-table-cell">
              <RichValue :data-key="field" :data-value="renderString(field, record)" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <markdown
      v-if="!error && template.headers.length === 0"
      :inline="false"
      :source="renderString(template.template, fetchedData)"
    />
  </ExpandButton>
</template>

<script>
import nunjucks from "nunjucks";
import fetchDot from "fetch-dot";

import ExpandButton from "./ExpandButton";
import Markdown from "./Markdown";
import { useGlobalStore } from "@/stores";
import { mapState } from "pinia";
import RichValue from "@/components/RichValue.vue";

nunjucks.configure({ autoescaping: true });

export default {
  name: "FeatureInfoTemplate",
  components: {
    RichValue,
    ExpandButton,
    Markdown,
  },
  props: {
    layer: Object,
    template: Object,
    feature: Object,
  },
  data() {
    return {
      fetchedData: [],
      error: "",
    };
  },
  mounted() {
    this.fetchData();
  },
  computed: {
    ...mapState(useGlobalStore, ["user"]),
  },
  methods: {
    async fetchData() {
      const fullUrl = this.template.source.url + this.template.endpoint;
      const renderedUrl = nunjucks.renderString(fullUrl, this.feature.properties);
      const url = new URL(renderedUrl);

      let params = {};
      if (this.template.method === "POST") {
        params = Object.fromEntries(url.searchParams.entries());
        url.search = "";
      }

      try {
        const result = await fetch(url.toString(), {
          ...this.getFetchParameters(),
          method: this.template.method,
          body: this.template.method === "POST" ? JSON.stringify(params) : null,
          headers: this.template.method === "POST" ? { "Content-Type": "application/json" } : {},
        });

        if (!result.ok) {
          if (result.status === 401) {
            this.error = "U moet ingelogd zijn om deze data te bekijken.";
          } else if (result.status === 403) {
            this.error = "U heeft geen rechten om deze data te bekijken.";
          } else if (result.status === 502 || result.status === 504) {
            this.error = "De databron kan niet bereikt worden. Probeer het later opnieuw.";
          } else {
            this.error = "Onbekende fout opgetreden. Probeer het later opnieuw.";
          }

          return;
        }

        const data = await result.json();

        if (this.template.list) {
          this.fetchedData = fetchDot(this.template.list, data);
        } else {
          this.fetchedData = data;
        }
      } catch (error) {
        console.error("Caught error", error);

        this.error = "Kan de data niet ophalen door een verbindingsprobleem. Probeer het later opnieuw.";
      }
    },
    getFetchParameters() {
      if (this.template.source.authenticate && this.user && this.user.token) {
        return {
          headers: { Authorization: `Bearer ${this.user.token}` },
        };
      }

      return {};
    },
    renderString(field, record) {
      return nunjucks.renderString(field, record);
    },
  },
};
</script>

<style scoped>
.table-wrapper {
  word-wrap: break-word;
  overflow: auto;
  flex: 1 1 auto;
}

.template-table {
  font-size: var(--font-size-small);
  overflow-x: auto;
  border-collapse: collapse;
  width: 100%;
}

.template-table-cell {
  padding: 4px;
  text-align: left;
  height: 30px;
  border-bottom: 1px solid var(--color-grey-60);
}

.template-table tbody tr:hover {
  background-color: var(--color-grey-40);
}

.template-table-header {
  font-weight: var(--font-weight-normal);
  color: var(--color-text-grey);
  padding: 8px 4px;
  border-bottom: 1px solid var(--color-grey-60);
  text-align: left;
}
</style>
