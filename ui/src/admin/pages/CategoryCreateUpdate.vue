<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Categorie wijzigen</h1>
    <AdminFormSections
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :compact-layout="true"
      :form-object="'categories'"
      :object-specific-save="saveCategory"
    />
  </div>
</template>

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";

export default {
  name: "CategoryCreateUpdate",
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
    this.getCategory();

    this.sections = this.getSections();
  },
  methods: {
    async getCategory() {
      const result = await fetch(`/atlas/api/v1/categories/${this.$route.params.id}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch category");
        return;
      }

      this.initialValues = await result.json();
    },
    async saveCategory(currentValues) {
      const url = `/atlas/api/v1/categories/${this.$route.params.id}/`;

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          this.$router.push(`/categories`);
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
              infoText: "Een uniek kort kenmerk voor de categorie in Atlas.",
            },
          ],
        },
      };
    },
  },
};
</script>
