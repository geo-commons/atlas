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
    />
  </div>
</template>

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";

export default {
  name: "SourceCreateUpdate",
  components: {
    AdminFormSections,
  },
  data() {
    return {
      sections: {},
      initialValues: {},
      currentValues: {},
      groups: [],
    };
  },
  created() {
    Promise.all([this.getSource(), this.getGroups()]).then(() => {
      this.setAtlasGroups();
      this.sections = this.getSections();
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

      currentValues.atlas_groups = currentValues.atlas_groups[1].map((group) => group.id);

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
