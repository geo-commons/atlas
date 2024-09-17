<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Dataset wijzigen</h1>
    <AdminFormSections
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :form-object="'datasets'"
      :object-specific-save="saveDataset"
    />
  </div>
</template>

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import slugify from "slugify";

export default {
  name: "DatasetCreateUpdate",
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
    this.getDataset();

    this.sections = this.getSections();
  },
  methods: {
    async getDataset() {
      const result = await fetch(`/atlas/api/v1/datasets/${this.$route.params.id}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch dataset");
        return;
      }

      this.initialValues = await result.json();

      this.initialValues.last_updated = this.initialValues.last_updated
        ? this.initialValues.last_updated.split("T")[0]
        : "";

      this.initialValues.dataset_category = this.initialValues.dataset_category
        ? this.initialValues.dataset_category.id
        : "";
    },

    async saveDataset(currentValues) {
      const url = `/atlas/api/v1/datasets/${this.$route.params.id}/`;

      currentValues.themes = currentValues.themes.map((theme) => theme.id);
      currentValues.slug = slugify(currentValues.title);

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          this.$router.push(`/datasets`);
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    async getCategories() {
      const result = await fetch("/atlas/api/v1/categories/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch categories");
      }

      const response = await result.json();

      return response.map((category) => {
        return { id: category.id, label: category.title };
      });
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
            {
              label: "Beschrijving",
              id: "description",
              name: "Description",
              type: "textarea",
              required: false,
            },
            {
              label: "Organisatie",
              id: "organization",
              name: "Organization",
              type: "text",
              required: false,
            },
            {
              label: "Categorie",
              id: "dataset_category",
              name: "Category",
              type: "dropdown",
              placeholder: "categorie",
              required: false,
              options: this.getCategories,
            },
            {
              label: "Bron Beschrijving",
              id: "source_description",
              name: "Source Description",
              type: "text",
              required: false,
              multiLine: true,
            },
            {
              label: "Dataset doel",
              id: "purpose_of_manufacture",
              name: "Purpose of Manufacture",
              type: "textarea",
              required: false,
            },
            {
              label: "Contactgegevens",
              id: "contact",
              name: "Contact",
              type: "text",
              required: false,
            },
            {
              label: "Gegevensbeheerder",
              id: "data_owner",
              name: "Data Owner",
              type: "text",
              required: false,
            },
            {
              label: "Verwerkingsverantwoordelijke",
              id: "data_controller",
              name: "Data Controller",
              type: "text",
              required: false,
            },
            {
              label: "Laatst bijgewerkt",
              id: "last_updated",
              name: "Last Updated",
              type: "date",
              required: false,
            },
            {
              label: "Updatefrequentie",
              id: "update_frequency",
              name: "Update Frequency",
              type: "text",
              required: false,
            },
          ],
        },
        themes: {
          label: "Thema's",
          questions: [
            {
              label: "Thema's",
              id: "themes",
              name: "Themes",
              type: "theme-select",
              required: false,
            },
          ],
        },
      };
    },
  },
};
</script>
