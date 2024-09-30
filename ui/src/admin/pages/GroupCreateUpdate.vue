<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Groep wijzigen</h1>
    <AdminFormSections
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :compact-layout="true"
      :form-object="'groups'"
      :object-specific-save="saveGroup"
    />
  </div>
</template>

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";

export default {
  name: "GroupCreateUpdateComponent",
  components: { AdminFormSections },
  props: {},
  data() {
    return {
      sections: {},
      initialValues: {},
      currentValues: {},
    };
  },
  created() {
    this.getGroup();
    this.sections = this.getSections();
  },
  methods: {
    async getGroup() {
      const result = await fetch(`/atlas/api/v1/groups/${this.$route.params.id}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch group");
        return;
      }

      this.initialValues = await result.json();
    },
    async saveGroup(currentValues) {
      const url = `/atlas/api/v1/groups/${this.$route.params.id}/`;

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          this.$router.push(`/groups`);
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
              label: "Group",
              id: "name",
              name: "Name",
              type: "text",
              required: true,
            },
            {
              label: "Externe ID",
              id: "external_id",
              name: "ExternalId",
              type: "text",
              required: true,
              infoText: "Het unieke kenmerk van de groep in de inlogbron.",
            },
            {
              label: "Kort kenmerk",
              id: "slug",
              name: "Slug",
              type: "text",
              required: true,
              infoText: "Een uniek kort kenmerk voor de groep.",
            },
          ],
        },
      };
    },
  },
};
</script>

<style scoped></style>
