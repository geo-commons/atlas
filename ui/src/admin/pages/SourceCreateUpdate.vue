<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Bron wijzigen</h1>
    <AdminFormSections
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :compact-layout="true"
      :form-object="'sources'"
      :object-specific-save="saveSource"
    />
  </div>
</template>

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";

export default {
  name: "SourceCreateUpdate",
  components: {
    AdminFormSections,
  },
  data() {
    return {
      sections: {},
      initialValues: {},
      currentValues: {},
    };
  },
  created() {
    this.getSource();
    this.sections = this.getSections();
  },
  methods: {
    async getSource() {
      const result = await fetch(`/atlas/api/v1/sources/${this.$route.params.id}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch source");
      }

      this.initialValues = await result.json();
    },
    async saveSource(currentValues) {
      const url = `/atlas/api/v1/sources/${this.$route.params.id}/`;

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          this.$router.push(`/sources`);
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
              label: "URL",
              id: "url",
              name: "URL",
              type: "url",
              required: true,
            },
            {
              label: "Verstuur authenticatie-informatie naar bron",
              id: "authenticate",
              name: "Authenticate",
              type: "checkbox",
              required: false,
            },
          ],
        },
      };
    },
  },
};
</script>
