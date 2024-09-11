<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Autorisatie wijzigen</h1>
    <AdminFormSections
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :form-object="'authorizations'"
      :object-specific-save="saveAuthorization"
    >
      <template #custom>
        <div id="reorder_instructions" aria-live="assertive" class="sr-only" v-text="assistiveText" />

        <div class="group-list-wrapper">
          <div class="available-groups">
            <label class="question-label" for="list1">Beschikbare groepen</label>
            <draggable
              v-bind="dragOptions"
              v-model="availableGroups"
              tag="ul"
              item-key="id"
              group="groups"
              role="listbox"
            >
              <template #item="{ element }">
                <li
                  :key="element.id"
                  class="groups-list-item"
                  tabindex="0"
                  @keydown.enter.prevent="moveGroup(element, availableGroups, selectedGroups)"
                >
                  {{ element.name }}
                </li>
              </template>
            </draggable>
          </div>
          <div class="selected-groups">
            <label class="question-label" for="list1">Geselecteerde groepen</label>
            <draggable
              v-bind="dragOptions"
              v-model="selectedGroups"
              tag="ul"
              item-key="id"
              group="groups"
              role="listbox"
            >
              <template #item="{ element }">
                <li
                  :key="element.id"
                  class="groups-list-item"
                  tabindex="0"
                  aria-describedby="reorder_instructions"
                  @keydown.enter.prevent="moveGroup(element, selectedGroups, availableGroups)"
                >
                  {{ element.name }}
                </li>
              </template>
            </draggable>
          </div>
        </div>
      </template>
    </AdminFormSections>
  </div>
</template>

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import draggable from "vuedraggable";

draggable.compatConfig = { MODE: 3 };

export default {
  name: "AuthorizationCreateUpdate",
  components: {
    draggable,
    AdminFormSections,
  },
  data() {
    return {
      sources: {},
      groups: [],
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
    Promise.all([this.getAuthorization(), this.getGroups()]).then(() => {
      this.selectedGroups = this.groups.filter((group) => this.initialValues.atlas_groups.includes(group.id));
      this.availableGroups = this.groups.filter((group) => !this.initialValues.atlas_groups.includes(group.id));
    });

    this.sections = this.getSections();
  },
  methods: {
    async getAuthorization() {
      const result = await fetch(`/atlas/api/v1/authorizations/${this.$route.params.id}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch authorization");
        return;
      }

      const response = await result.json();
      this.initialValues = response;
    },
    async saveAuthorization(currentValues) {
      currentValues.atlas_groups = this.selectedGroups.map((group) => group.id);

      const url = `/atlas/api/v1/authorizations/${this.$route.params.id}/`;

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          this.$router.push(`/authorizations`);
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
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
        return { id: source.id, label: source.title, url: source.url, type: source.source_type };
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
              label: "Bron",
              id: "source",
              name: "Source",
              type: "dropdown",
              required: true,
              placeholder: "bron",
              options: this.getSources,
            },
            {
              label: "Resource",
              id: "resource",
              name: "Resource",
              type: "text",
              required: true,
              infoText: "Naam van de laag of de resource",
            },
            {
              label: "Beschrijving",
              id: "description",
              name: "Description",
              type: "text",
              required: true,
              multiLine: true,
              infoText: "Een beschrijvende tekst voor beheerders",
            },
            {
              label: "Sortering",
              id: "ordering",
              name: "Ordering",
              type: "decimal",
              required: false,
              step: 1,
            },
          ],
        },
        access: {
          label: "Toegang",
          questions: [
            {
              label: "Vereis inlog van gebruiker",
              id: "login_required",
              name: "LoginRequired",
              type: "checkbox",
              required: false,
            },
            {
              label: "Alleen intern zichtbaar",
              id: "only_internal",
              name: "OnlyInternal",
              type: "checkbox",
              required: false,
              infoText: "Alleen zichtbaar binnen interne omgeving",
            },
            {
              label: "Audit log",
              id: "audit_log",
              name: "AuditLog",
              type: "checkbox",
              required: false,
              infoText: "Voeg verzoeken toe aan de audit log",
            },
            {
              type: "custom",
            },
            {
              label: "Response filter",
              id: "response_filter",
              name: "ResponseFilter",
              type: "text",
              multiLine: true,
              required: false,
              isNested: true,
              infoText: "Maak veldnamen vriendelijk.",
            },
          ],
        },
      };
    },
  },
};
</script>

<style scoped>
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
  background-color: var(--color-admin-primary-hover);
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

.admin-list > li {
  display: flex;
  align-items: center;
  background: var(--color-white);
  padding: 4px 12px;
}

.admin-list > li:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-60);
}

.admin-list-buttons button:hover {
  background-color: var(--color-backdrop);
}
</style>
