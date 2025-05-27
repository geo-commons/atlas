<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Thema wijzigen</h1>
    <AdminFormSections
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

export default {
  name: "ThemeCreateUpdate",
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
    this.getTheme();

    this.sections = this.getSections();
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
