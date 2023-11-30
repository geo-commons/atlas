<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Categorie wijzigen</h1>
    <validation-observer v-slot="{ handleSubmit }">
      <form @submit.prevent="handleSubmit(saveCategory)">
        <AdminFormSections
          :sections="sections"
          :initial-values="initialValues"
          :create-view="true"
          @update="(newValues) => updateCurrentValues(newValues)"
        />
        <div class="config-btn-wrapper">
          <router-link to="/categories" class="button __tertiary" type="button">Annuleer</router-link>
          <button class="button __primary" type="submit">Opslaan</button>
        </div>
      </form>
    </validation-observer>
  </div>
</template>

<script>
import { ValidationObserver } from "vee-validate";

import Cookies from "js-cookie";
import AdminFormSections from "@/admin/components/AdminFormSections.vue";

export default {
  name: "CategoryCreateUpdate",
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
    async saveCategory() {
      let result;

      result = await fetch(`/atlas/api/v1/categories/${this.$route.params.id}/`, {
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
          `Error occurred while saving category with category id: ${this.currentValues.id} and title: ${this.currentValues.title}`
        );
      }

      this.$router.push(`/categories`);
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

<style scoped>
.config-btn-wrapper {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
  padding: 30px 0;
}
</style>
