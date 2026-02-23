<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Thema wijzigen</h1>
    <Spinner v-if="loading" style-type="'admin'" />
    <AdminFormSections
      v-else
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :compact-layout="true"
      :form-object="'themes'"
      :object-specific-save="saveTheme"
    />
  </div>
</template>

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import Spinner from "@/components/Spinner.vue";
import { useQueryCache } from "@pinia/colada";

export default {
  name: "ThemeCreateUpdate",
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

    Promise.all([this.getTheme()]).then(() => {
      this.sections = this.getSections();
      this.loading = false;
    });
  },
  methods: {
    async getTheme() {
      const result = await fetch(`/atlas/api/v1/themes/${this.$route.params.id}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch theme");
        return;
      }

      this.initialValues = await result.json();
    },
    async saveTheme(currentValues, continueEditing = false) {
      const url = `/atlas/api/v1/themes/${this.$route.params.id}/`;

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          await this.queryCache.invalidateQueries(["themes"]);

          if (!continueEditing) {
            this.$router.push(`/themes`);
          }

          this.$toast.add({
            severity: "success",
            summary: "Thema opgeslagen",
            detail: "Het thema is succesvol opgeslagen.",
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
              label: "Naam",
              id: "title",
              name: "Title",
              type: "text",
              required: true,
            },
          ],
        },
      };
    },
  },
};
</script>
