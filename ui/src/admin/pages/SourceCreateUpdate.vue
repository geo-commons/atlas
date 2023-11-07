<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Bron wijzigen</h1>
    <validation-observer v-slot="{ handleSubmit }">
      <form @submit.prevent="handleSubmit(saveSource)">
        <AdminFormSections
          :sections="sections"
          :initial-values="initialValues"
          :create-view="true"
          @update="(newValues) => updateCurrentValues(newValues)"
        />
        <div class="config-btn-wrapper">
          <router-link to="/sources" class="button __tertiary">Annuleer</router-link>
          <button class="button __primary" type="submit">Opslaan</button>
        </div>
      </form>
    </validation-observer>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import { ValidationObserver } from "vee-validate";
import AdminFormSections from "@/admin/components/AdminFormSections.vue";

export default {
  name: "SourceCreateUpdate",
  components: {
    AdminFormSections,
    ValidationObserver,
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
    async saveSource() {
      let result;

      result = await fetch(`/atlas/api/v1/sources/${this.$route.params.id}/`, {
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
          `Error occurred while saving source with source id: ${this.currentValues.id} and title: ${this.currentValues.title}`
        );
      }

      this.$router.push(`/sources`);
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

<style scoped>
.config-btn-wrapper {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
  padding: 30px 0;
}
</style>
