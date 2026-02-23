<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Categorie wijzigen</h1>
    <Spinner v-if="loading" style-type="'admin'" />
    <AdminFormSections
      v-else
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
import Spinner from "@/components/Spinner.vue";
import { useQueryCache } from "@pinia/colada";

export default {
  name: "CategoryCreateUpdate",
  components: {
    Spinner,
    AdminFormSections,
  },
  setup() {
    const queryCache = useQueryCache();
    return { queryCache };
  },
  data() {
    return {
      sections: {},
      initialValues: {},
      loading: false,
    };
  },
  created() {
    this.loading = true;

    Promise.all([this.getCategory()]).then(() => {
      this.sections = this.getSections();
      this.loading = false;
    });
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
    async saveCategory(currentValues, continueEditing = false) {
      const url = `/atlas/api/v1/categories/${this.$route.params.id}/`;

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          await this.queryCache.invalidateQueries(["categories"]);

          if (!continueEditing) {
            this.$router.push(`/categories`);
          }

          this.$toast.add({
            severity: "success",
            summary: "Categorie opgeslagen",
            detail: "De categorie is succesvol opgeslagen.",
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
              infoText: "Een uniek kort kenmerk voor de categorie in Atlas.",
            },
          ],
        },
      };
    },
  },
};
</script>
