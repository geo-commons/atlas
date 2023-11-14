<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Groep wijzigen</h1>
    <validation-observer v-slot="{ handleSubmit }">
      <form @submit.prevent="handleSubmit(saveGroup)">
        <AdminFormSections
          :sections="sections"
          :initial-values="initialValues"
          @update="(newValues) => updateCurrentValues(newValues)"
        />
        <div class="config-btn-wrapper">
          <router-link to="/groups" class="button __tertiary" type="button">Annuleer</router-link>
          <button class="button __primary" type="submit">Opslaan</button>
        </div>
      </form>
    </validation-observer>
  </div>
</template>

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import { ValidationObserver } from "vee-validate";
import Cookies from "js-cookie";

export default {
  name: "GroupCreateUpdateComponent",
  components: { AdminFormSections, ValidationObserver },
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
    async saveGroup() {
      let result;

      result = await fetch(`/atlas/api/v1/groups/${this.$route.params.id}/`, {
        method: "PATCH",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify(this.currentValues),
      });

      if (!result.ok) {
        console.error(
          `Error occurred while saving group with group id: ${this.currentValues.id} and name: ${this.currentValues.name}`
        );
      }

      this.$router.push(`/groups`);
    },

    updateCurrentValues(newValues) {
      this.currentValues = newValues;
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
      };
    },
  },
};
</script>

<style scoped>
.config-btn-wrapper {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
  padding: 30px 0;
}
</style>
