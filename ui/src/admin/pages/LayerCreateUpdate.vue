<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Kaartlaag wijzigen</h1>
    <validation-observer v-slot="{ handleSubmit }">
      <form @submit.prevent="handleSubmit(saveLayer)">
        <AdminFormSections
          :sections="sections"
          :initial-values="initialValues"
          @update="(newValues) => updateCurrentValues(newValues)"
        >
          <template #custom>
            <div id="reorder_instructions" aria-live="assertive" class="sr-only" v-text="assistiveText" />

            <div class="group-list-wrapper">
              <div class="available-groups">
                <label class="question-label" for="list1">Beschikbare groepen</label>
                <draggable
                  v-model="availableGroups"
                  tag="ul"
                  item-key="id"
                  group="groups"
                  v-bind="dragOptions"
                  role="listbox"
                >
                  <li
                    v-for="item in availableGroups"
                    :key="item.id"
                    class="groups-list-item"
                    tabindex="0"
                    @keydown.enter.prevent="moveGroup(item, availableGroups, selectedGroups)"
                  >
                    {{ item.name }}
                  </li>
                </draggable>
              </div>
              <div class="selected-groups">
                <label class="question-label" for="list1">Geselecteerde groepen</label>
                <draggable
                  v-model="selectedGroups"
                  tag="ul"
                  item-key="id"
                  group="groups"
                  v-bind="dragOptions"
                  role="listbox"
                >
                  <li
                    v-for="item in selectedGroups"
                    :key="item.id"
                    class="groups-list-item"
                    tabindex="0"
                    aria-describedby="reorder_instructions"
                    @keydown.enter.prevent="moveGroup(item, selectedGroups, availableGroups)"
                  >
                    {{ item.name }}
                  </li>
                </draggable>
              </div>
            </div>
          </template>
        </AdminFormSections>
        <div class="config-btn-wrapper">
          <router-link to="/layers" class="button __tertiary" type="button">Annuleer</router-link>
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
import draggable from "vuedraggable";

export default {
  name: "LayerCreateUpdate",
  components: {
    draggable,
    AdminFormSections,
    ValidationObserver,
  },
  data() {
    return {
      categories: {},
      sources: {},
      sourceTypes: [],
      groups: [],
      formats: [],
      sections: {},
      initialValues: {},
      currentValues: {},
      availableGroups: [],
      selectedGroups: [],
      assistiveText: "Verplaats een group met behulp van de enter toets",
    };
  },
  computed: {
    dragOptions() {
      return {
        animation: 0,
        group: "description",
        disabled: false,
        ghostClass: "ghost",
      };
    },
  },
  created() {
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

    Promise.all([this.getLayer(), this.getGroups()]).then(() => {
      this.selectedGroups = this.groups.filter((group) => this.initialValues.atlas_groups.includes(group.id));
      this.availableGroups = this.groups.filter((group) => !this.initialValues.atlas_groups.includes(group.id));
    });

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

      const response = await result.json();
      this.initialValues = response;
      this.initialValues.category_id = response.category?.id;
      this.initialValues.source_id = response.source.id;

      // Internal fields used for v-model binding
      this.initialValues.metadata_name = response.metadata.name;
      this.initialValues.metadata_description = response.metadata.description;
      this.initialValues.metadata_organization = response.metadata.organization;
      this.initialValues.metadata_updated = response.metadata.updated;
      this.initialValues.metadata_lineage = response.metadata.lineage;
      this.initialValues.metadata_contact = response.metadata.contact;

      return result;
    },
    async saveLayer() {
      let result;

      // Convert internal fields back to layer model.
      this.currentValues.metadata.name = this.currentValues.metadata_name;
      this.currentValues.metadata.description = this.currentValues.metadata_description;
      this.currentValues.metadata.organization = this.currentValues.metadata_organization;
      this.currentValues.metadata.updated = this.currentValues.metadata_updated;
      this.currentValues.metadata.lineage = this.currentValues.metadata_lineage;
      this.currentValues.metadata.contact = this.currentValues.metadata_contact;
      this.currentValues.atlas_groups = this.selectedGroups.map((group) => group.id);

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
    async getGroups() {
      const result = await fetch("/atlas/api/v1/groups/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch groups");
      }

      this.groups = await result.json();

      return result;
    },
    updateCurrentValues(newValues) {
      this.currentValues = newValues;
    },
    moveGroup(item, fromArray, toArray) {
      const arrayAriaText = toArray === this.availableGroups ? "Beschikbare groepen" : "Geselecteerde groepen";
      this.assistiveText = `${item.name}, verplaatst naar ${arrayAriaText}`;

      fromArray.splice(fromArray.indexOf(item), 1);
      toArray.push(item);
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
              maxLength: 50,
              infoText: "Een uniek kenmerk voor de laag in Atlas. Dit kenmerk komt terug in links naar de laag.",
            },
            {
              label: "Categorie",
              id: "category_id",
              name: "Category",
              type: "dropdown",
              placeholder: "categorie",
              required: false,
              options: this.getCategories,
            },
            {
              label: "Gepubliceerd",
              id: "published",
              name: "Published",
              type: "checkbox",
              required: false,
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
              infoText: "De naam van de laag op de geoserver.",
            },
            {
              label: "Brontype",
              id: "source_type",
              name: "SourceType",
              type: "dropdown",
              required: false,
              placeholder: "brontype",
              options: this.sourceTypes,
              infoText:
                '"WMS en WFS" en WFS is zichtbaar in zowel het datapaneel als op de kaart. WMS en WMTS toont alleen op de kaart.',
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
              minValue: 0,
              maxValue: 1,
              step: 0.1,
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
              label: "Naam",
              id: "metadata_name",
              name: "Name",
              type: "text",
              required: false,
              isNested: true,
            },
            {
              label: "Omschrijving",
              id: "metadata_description",
              name: "metadataDescription",
              type: "text",
              required: false,
              multiLine: true,
              isNested: true,
              infoText: "Het is mogelijk om tekst op te maken met Markdown in dit veld.",
            },
            {
              label: "Organisatie",
              id: "metadata_organization",
              name: "metadataOrganisation",
              type: "text",
              required: false,
              isNested: true,
            },
            {
              label: "Contactpersoon",
              id: "metadata_contact",
              name: "metadataContact",
              type: "text",
              required: false,
              isNested: true,
            },
            {
              label: "Herkomst data",
              id: "metadata_lineage",
              name: "metadataLineage",
              type: "text",
              multiLine: true,
              required: false,
              isNested: true,
              infoText:
                "Beschrijft de herkomst van de dataset. Het is mogelijk om tekst op te maken met Markdown in dit veld.",
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
          questions: [
            {
              label: "Alleen intern zichtbaar",
              id: "closed_dataset",
              name: "ClosedDataset",
              type: "checkbox",
              required: false,
              infoText: "Laag is alleen zichtbaar binnen interne omgeving.",
            },
            {
              label: "Vereis inlog voor deze dataset",
              id: "login_required",
              name: "LoginRequired",
              type: "checkbox",
              required: false,
              infoText: "De inhoud van deze dataset kan alleen bekeken worden door ingelogde gebruikers.",
            },
            {
              type: "custom",
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

.available-groups {
  grid-area: available-groups;
}

.selected-groups {
  grid-area: selected-groups;
}

.group-list-wrapper {
  display: grid;
  grid-template-areas: "available-groups selected-groups";
  grid-template-columns: 1fr 1fr;
  column-gap: 100px;
  padding-bottom: 50px;
}

.groups-list-item {
  background: var(--color-white);
  padding: 10px 20px;
  word-break: break-word;
}

.groups-list-item:hover {
  background-color: var(--color-primary-hover);
  cursor: move;
}

.groups-list-item:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-50);
}

@media (max-width: 768px) {
  .group-list-wrapper {
    grid-template-areas:
      "available-groups"
      "selected-groups";
    grid-template-columns: 1fr;
    row-gap: 30px;
  }
}
</style>
