<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Tabel wijzigen</h1>
    <Spinner v-if="loading" style-type="'admin'" />
    <AdminFormSections
      v-else
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :compact-layout="false"
      :form-object="'tables'"
      :object-specific-save="saveTable"
    />
  </div>
</template>

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import Spinner from "@/components/Spinner.vue";
import { getAllObjects } from "@/utils/api-helpers";

export default {
  name: "TableCreateUpdate",
  components: {
    Spinner,
    AdminFormSections,
  },
  data() {
    return {
      sources: [],
      sections: {},
      initialValues: {},
      currentValues: {},
      endpointMethods: [],
      loading: false,
    };
  },
  created() {
    this.loading = true;

    this.endpointMethods = [
      { id: "GET", label: "GET" },
      { id: "POST", label: "POST" },
    ];

    Promise.all([this.getTable(), this.getSources()]).then(() => {
      this.sections = this.getSections();
      this.loading = false;
    });
  },
  methods: {
    async getTable() {
      const result = await fetch(`/atlas/api/v1/tables/${this.$route.params.id}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch table");
      }

      this.initialValues = await result.json();
      this.initialValues.search_fields = JSON.stringify(this.initialValues.search_fields, null, 2);
      return result;
    },
    async getSources() {
      const url = getAllObjects("/atlas/api/v1/sources/");
      const result = await fetch(url, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch sources");
      }

      const response = await result.json();

      this.sources = response.results.map((source) => {
        return { id: source.id, label: source.title };
      });

      return response;
    },
    async saveTable(currentValues, continueEditing = false) {
      const url = `/atlas/api/v1/tables/${this.$route.params.id}/`;

      currentValues.search_fields = JSON.parse(currentValues.search_fields);

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          if (!continueEditing) {
            this.$router.push(`/tables`);
          }

          this.$toast.add({
            severity: "success",
            summary: "Tabel opgeslagen",
            detail: "De tabel is succesvol opgeslagen.",
            life: 3000,
          });
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    getSections() {
      return {
        general: {
          label: "Algemene gegevens",
          questions: [
            {
              label: "Titel",
              id: "title",
              name: "Title",
              type: "text",
              required: true,
            },
            {
              label: "Kort kenmerk",
              id: "slug",
              name: "Slug",
              type: "text",
              required: true,
            },
          ],
        },
        source: {
          label: "Bron",
          questions: [
            {
              label: "Bron",
              id: "source",
              name: "Source",
              type: "dropdown",
              required: true,
              placeholder: "bron",
              options: this.sources,
            },
            {
              label: "Endpoint",
              id: "endpoint",
              name: "Endpoint",
              type: "text",
              required: true,
            },
            {
              label: "Bron Methode",
              id: "method",
              name: "SourceMethod",
              type: "dropdown",
              required: true,
              placeholder: "Bron Methode",
              options: this.endpointMethods,
            },
          ],
        },
        table: {
          label: "Tabel Instellingen",
          questions: [
            {
              label: "Veldnaam van lijst",
              id: "list_query",
              name: "ListQuery",
              type: "text",
              required: false,
            },
            {
              label: "Veldnaam van pagina",
              id: "page_attribute",
              name: "PageAttribute",
              type: "text",
              required: false,
            },
            {
              label: "Veldnaam van items per pagina",
              id: "items_per_page_attribute",
              name: "ItemsPerPageAttribute",
              type: "text",
              required: false,
            },
            {
              label: "Veldnaam van totaal aantal items",
              id: "total_items_page_attribute",
              name: "TotalItemsPageAttribute",
              type: "text",
              required: false,
            },
            {
              label: "Template van foutmelding",
              id: "error_template",
              name: "ErrorTemplate",
              type: "text",
              required: false,
            },
            {
              label: "Kopjes in lijstweergave",
              id: "list_headings",
              name: "ListHeadings",
              type: "text",
              multiLine: true,
              required: false,
              isNested: true,
              infoText: "Voer één veld per regel in.",
            },
            {
              label: "Velden in lijstweergave",
              id: "list_fields",
              name: "ListFields",
              type: "text",
              multiLine: true,
              required: false,
              isNested: true,
              infoText: "Voer één veld per regel in de volgende notatie {{ veld_naam }}",
            },
            {
              label: "Velden waarop gezocht kan worden",
              id: "search_fields",
              name: "SearchFields",
              type: "text",
              json: true,
              required: false,
              isNested: true,
            },
            {
              label: "Sortering",
              id: "ordering",
              name: "Ordering",
              type: "decimal",
              required: false,
              step: 1,
            },
          ],
        },
        access: {
          label: "Toegang",
          questions: [
            {
              label: "Alleen intern zichtbaar",
              id: "only_internal",
              name: "ClosedDataset",
              type: "checkbox",
              required: false,
              infoText: "Laag is alleen zichtbaar binnen interne omgeving.",
            },
            {
              label: "Vereis inlog voor deze dataset",
              id: "login_required",
              name: "LoginRequired",
              type: "checkbox",
              required: false,
              infoText: "De inhoud van deze dataset kan alleen bekeken worden door ingelogde gebruikers.",
            },
          ],
        },
      };
    },
  },
};
</script>
