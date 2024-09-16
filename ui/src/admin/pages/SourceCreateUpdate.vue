<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Bron wijzigen</h1>
    <AdminFormSections
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :compact-layout="false"
      :form-object="'sources'"
      :object-specific-save="saveSource"
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

export default {
  name: "SourceCreateUpdate",
  components: {
    draggable,
    AdminFormSections,
  },
  data() {
    return {
      sections: {},
      initialValues: {},
      currentValues: {},
      availableGroups: [],
      selectedGroups: [],
    };
  },
  created() {
    this.getSource();
    this.sections = this.getSections();

    Promise.all([this.getGroups()]).then(() => {
      this.selectedGroups = this.groups.filter((group) => this.initialValues.atlas_groups.includes(group.id));
      this.availableGroups = this.groups.filter((group) => !this.initialValues.atlas_groups.includes(group.id));
    });
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
    async saveSource(currentValues) {
      const url = `/atlas/api/v1/sources/${this.$route.params.id}/`;

      currentValues.atlas_groups = this.selectedGroups.map((group) => group.id);

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          this.$router.push(`/sources`);
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
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
        access: {
          label: "Toegang",
          questions: [
            {
              label: "Vereis inlog voor deze bron",
              id: "login_required",
              name: "LoginRequired",
              type: "checkbox",
              required: false,
              infoText: "De inhoud van deze bron kan alleen bekeken worden door ingelogde gebruikers.",
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
