<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Tabel wijzigen</h1>
    <AdminFormSections
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

export default {
  name: "TableCreateUpdate",
  components: {
    AdminFormSections,
  },
  data() {
    return {
      sections: {},
      initialValues: {},
      currentValues: {},
      endpointMethods: [],
    };
  },
  created() {
    this.endpointMethods = [
      { id: "GET", label: "GET" },
      { id: "POST", label: "POST" },
    ];

    this.getTable();
    this.sections = this.getSections();
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
      this.initialValues.search_fields = JSON.stringify(this.initialValues.search_fields);
    },
    async getSources() {
      const result = await fetch("/atlas/api/v1/sources/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch sources");
      }

      const response = await result.json();

      return response.map((source) => {
        return { id: source.id, label: source.title };
      });
    },
    async saveTable(currentValues) {
      const url = `/atlas/api/v1/tables/${this.$route.params.id}/`;

      currentValues.search_fields = JSON.parse(currentValues.search_fields);

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          this.$router.push(`/tables`);
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
              options: this.getSources,
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
              multiLine: true,
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
