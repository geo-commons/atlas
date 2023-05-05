<template>
  <ExpandButton :title="template.title" class="template">
    <p v-if="error">{{ error }}</p>
    <table-list v-if="!error && template.headers.length > 0" class="table">
      <table>
        <thead>
          <tr>
            <th v-for="(heading, key) in template.headers" :key="key">
              {{ heading }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(record, key) in fetchedData" :key="key">
            <td v-for="(field, key) in template.fields" :key="key">
              {{ renderString(field, record) }}
            </td>
          </tr>
        </tbody>
      </table>
    </table-list>
    <markdown
      v-if="!error && template.headers.length === 0"
      :inline="false"
      :source="renderString(template.template, fetchedData)"
    />
  </ExpandButton>
</template>

<script>
import nunjucks from "nunjucks";
import { mapState } from "vuex";
import fetchDot from "fetch-dot";

import ExpandButton from "./ExpandButton";
import TableList from "./TableList";
import Markdown from "./Markdown";

nunjucks.configure({ autoescaping: true });

export default {
  name: "FeatureInfoTemplate",
  components: {
    ExpandButton,
    TableList,
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
    ...mapState({
      user: (state) => state.user,
    }),
  },
  methods: {
    async fetchData() {
      const url = new URL(
        this.template.source.url +
          nunjucks.renderString(this.template.endpoint, this.feature.properties)
      );

      try {
        const result = await fetch(url.toString(), this.getFetchParameters());

        if (!result.ok) {
          if (result.status == 401) {
            this.error = "U moet ingelogd zijn om deze data te bekijken.";
          } else if (result.status == 403) {
            this.error = "U heeft geen rechten om deze data te bekijken.";
          } else if (result.status == 502 || result.status == 504) {
            this.error =
              "De databron kan niet bereikt worden. Probeer het later opnieuw.";
          } else {
            this.error =
              "Onbekende fout opgetreden. Probeer het later opnieuw.";
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
        console.error("Catched error", error);

        this.error =
          "Kan de data niet ophalen door een verbindingsprobleem. Probeer het later opnieuw.";
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
