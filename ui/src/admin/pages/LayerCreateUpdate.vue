<template>
  <div class="container">
    <h1 class="font-weight-normal">Kaartlaag wijzigen</h1>
    <validation-observer v-slot="{ handleSubmit }">
      <form @submit.prevent="handleSubmit(saveLayer)">
        <AdminFormSections
          :sections="sections"
          :initial-values="initialValues"
          @update="(newValues) => updateCurrentValues(newValues)"
        />
        <div class="config-btn-wrapper">
          <router-link to="/layers" class="button __tertiary">Annuleer</router-link>
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
  name: "LayerCreateUpdate",
  components: {
    AdminFormSections,
    ValidationObserver,
  },
  data() {
    return {
      data: null,
      formData: null,
      layersFromCapabilities: [],
      categories: {},
      sources: {},
      sourceTypes: [],
      formats: [],
      sections: {},
      initialValues: {},
      currentValues: {},
    };
  },
  created() {
    this.getLayer();

    this.sourceTypes = [
      { id: "WMS_WFS", label: "WMS en WFS" },
      { id: "WMS", label: "WMS" },
      { id: "WFS", label: "WFS" },
      { id: "WMTS", label: "WMTS" },
      { id: "XYZ", label: "XYZ" },
      { id: "MVT", label: "MVT" },
    ];

    this.formats = [
      { id: "image/png", label: "image/png" },
      { id: "image/jpeg", label: "image/jpeg" },
      { id: "image/vnd.jpeg-png", label: "image/vnd.jpeg-png" },
    ];

    this.sections = this.getSections();
  },
  methods: {
    async getLayer() {
      const result = await fetch(`/atlas/api/v1/layers/${this.$route.params.id}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layer");
        return;
      }

      this.data = await result.json();
      this.data.category_id = this.data.category.id;
      this.data.source_id = this.data.source.id;
      console.log(this.data);
      this.initialValues = this.data;
    },
    async saveLayer() {
      let result;

      result = await fetch(`/atlas/api/v1/layers/${this.$route.params.id}/`, {
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
          `Error occurred while saving layer with layer id: ${this.currentValues.id} and title: ${this.currentValues.title}`
        );
      }

      this.$router.push(`/layers`);
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
    async getSources() {
      const result = await fetch("/atlas/api/v1/sources/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch sources");
      }

      const response = await result.json();

      return response.map((source) => {
        return { id: source.id, label: source.title };
      });
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
            },
            {
              label: "Categorie",
              id: "category_id",
              name: "Category",
              type: "dropdown",
              required: true,
              placeholder: "categorie",
              options: this.getCategories,
            },
          ],
        },
        source: {
          label: "Bron",
          questions: [
            {
              label: "Bron",
              id: "source_id",
              name: "Source",
              type: "dropdown",
              required: true,
              placeholder: "bron",
              options: this.getSources,
            },
            {
              label: "Laagnaam",
              id: "layer_name",
              name: "LayerName",
              type: "text",
              required: true,
            },
            {
              label: "Brontype",
              id: "source_type",
              name: "SourceType",
              type: "dropdown",
              required: false,
              placeholder: "brontype",
              options: this.sourceTypes,
            },
            {
              label: "Projectie",
              id: "projection",
              name: "Projection",
              type: "text",
              required: false,
            },
            {
              label: "Servertype",
              id: "server_type",
              name: "ServerType",
              type: "text",
              required: false,
            },
            {
              label: "Formaat",
              id: "format",
              name: "Format",
              type: "dropdown",
              required: false,
              placeholder: "bron",
              options: this.formats,
            },
          ],
        },
        display: {
          label: "Weergave",
          questions: [
            {
              label: "Transparantie",
              id: "opacity",
              name: "Opacity",
              type: "decimal",
              required: false,
              min: 0,
              max: 1,
              step: 0.01,
            },
            {
              label: "Is basislaag",
              id: "is_base",
              name: "IsBase",
              type: "checkbox",
              required: false,
            },
            {
              label: "Is standaard zichtbaar",
              id: "is_visible",
              name: "IsVisible",
              type: "checkbox",
              required: false,
            },
            {
              label: "Is selecteerbaar",
              id: "is_selectable",
              name: "IsSelectable",
              type: "checkbox",
              required: false,
            },
            {
              label: "Zoomniveau minimum",
              id: "zoom_min",
              name: "ZoomMin",
              type: "decimal",
              required: false,
              step: 0.01,
            },
            {
              label: "Zoomniveau maximum",
              id: "zoom_max",
              name: "ZoomMax",
              type: "decimal",
              required: false,
              step: 0.01,
            },
          ],
        },
        metadata: {
          label: "Metadata",
          questions: [
            {
              label: "[todo: zit nog niet in response] Naam",
              id: "name",
              name: "Name",
              type: "text",
              required: false,
            },
            {
              label: "Omschrijving",
              id: "metadata_description",
              name: "metadataDescription",
              type: "text",
              required: false,
              multiLine: true,
            },
            {
              label: "Organisatie",
              id: "metadata_organisation",
              name: "metadataOrganisation",
              type: "text",
              required: false,
            },
            {
              label: "Laatst bijgewerkt",
              id: "metadata_updated",
              name: "metadataUpdated",
              type: "text",
              required: false,
            },
          ],
        },
        access: {
          label: "Toegang",
          questions: [],
        },
        linkedData: {
          label: "Gekoppelde data",
          questions: [],
        },
        templates: {
          label: "Templates",
          questions: [],
        },
      };
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
}

.config-btn-wrapper {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
  padding: 30px 0;
}
</style>
