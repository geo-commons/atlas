<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Groep wijzigen</h1>
    <Spinner v-if="loading" style-type="'admin'" />
    <AdminFormSections
      v-else
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
import Spinner from "@/components/Spinner.vue";
import { useQueryCache } from "@pinia/colada";

export default {
  name: "GroupCreateUpdateComponent",
  components: { Spinner, AdminFormSections },
  props: {},
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

    Promise.all([this.getGroup()]).then(() => {
      this.sections = this.getSections();
      this.loading = false;
    });
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
    async saveGroup(currentValues, continueEditing = false) {
      const url = `/atlas/api/v1/groups/${this.$route.params.id}/`;

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          await this.queryCache.invalidateQueries(["groups"]);

          if (!continueEditing) {
            this.$router.push(`/groups`);
          }

          this.$toast.add({
            severity: "success",
            summary: "Groep opgeslagen",
            detail: "De groep is succesvol opgeslagen.",
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
              required: false,
              infoText:
                "Het unieke kenmerk van de groep volgens de inlogbron. Alleen invullen als synchronisatie met inlogbron gewenst is.",
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
