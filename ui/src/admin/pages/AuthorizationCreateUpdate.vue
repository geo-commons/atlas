<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Autorisatie wijzigen</h1>
    <Spinner v-if="loading" style-type="'admin'" />
    <AdminFormSections
      v-else
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :form-object="'authorizations'"
      :object-specific-save="saveAuthorization"
    />
  </div>
</template>

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import Spinner from "@/components/Spinner.vue";

export default {
  name: "AuthorizationCreateUpdate",
  components: {
    Spinner,
    AdminFormSections,
  },
  data() {
    return {
      sources: [],
      groups: [],
      sections: {},
      initialValues: {},
      currentValues: {},
      availableGroups: [],
      selectedGroups: [],
      loading: false,
    };
  },
  created() {
    this.loading = true;

    Promise.all([this.getAuthorization(), this.getGroups(), this.getSources()]).then(() => {
      this.setAtlasGroups();
      this.sections = this.getSections();
      this.loading = false;
    });
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
      return response;
    },
    async saveAuthorization(currentValues) {
      currentValues.atlas_groups = currentValues.atlas_groups[1].map((group) => group.id);

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

      this.sources = response.map((source) => {
        return { id: source.id, label: source.title, url: source.url, type: source.source_type };
      });
      console.log(this.sources);
      return response;
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
    setAtlasGroups() {
      const selectedGroups = this.groups.filter((group) => this.initialValues.atlas_groups.includes(group.id));
      const availableGroups = this.groups.filter((group) => !this.initialValues.atlas_groups.includes(group.id));
      this.initialValues.atlas_groups = [availableGroups, selectedGroups];
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
              options: this.sources,
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
            {
              label: "Groepen",
              objectDisplayName: "groepen",
              id: "atlas_groups",
              name: "atlasGroups",
              type: "picklist",
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
