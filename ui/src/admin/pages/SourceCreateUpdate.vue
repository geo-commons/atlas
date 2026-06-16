<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Bron wijzigen</h1>
    <Spinner v-if="loading" style-type="'admin'" />
    <AdminFormSections
      v-else
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
import Spinner from "@/components/Spinner.vue";
import { useQueryCache } from "@pinia/colada";
import { useGroupList } from "@/admin/queries";

export default {
  name: "SourceCreateUpdate",
  components: {
    Spinner,
    AdminFormSections,
  },
  setup() {
    const queryCache = useQueryCache();
    const { groupsState, refresh: refreshGroups } = useGroupList();
    return { queryCache, groupsState, refreshGroups };
  },
  data() {
    return {
      initialValues: {},
      loading: false,
      sourceTypes: [
        { id: "OWS", label: "OWS" },
        { id: "WMTS", label: "WMTS" },
        { id: "REST", label: "REST" },
      ],
    };
  },
  computed: {
    sections() {
      return this.getSections();
    },
  },
  created() {
    this.loading = true;

    this.getSource()
      .then(() => this.setAtlasGroups())
      .finally(() => {
        this.loading = false;
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
    async saveSource(currentValues, continueEditing = false) {
      const url = `/atlas/api/v1/sources/${this.$route.params.id}/`;

      currentValues.atlas_groups = currentValues.atlas_groups?.[1]?.map((group) => group.id) || [];

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          await this.queryCache.invalidateQueries(["sources"]);

          if (!continueEditing) {
            this.$router.push(`/sources`);
          }

          this.$toast.add({
            severity: "success",
            summary: "Bron opgeslagen",
            detail: "De bron is succesvol opgeslagen.",
            life: 3000,
          });
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    async setAtlasGroups() {
      await this.refreshGroups();
      const groups = this.groupsState.data || [];
      const selectedGroups = groups.filter((group) => this.initialValues.atlas_groups.includes(group.id));
      const availableGroups = groups.filter((group) => !this.initialValues.atlas_groups.includes(group.id));
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
              label: "Kort kenmerk",
              id: "slug",
              name: "Slug",
              type: "text",
              required: false,
              infoText: "Een uniek kort kenmerk voor de bron in Atlas.",
            },
            {
              label: "URL",
              id: "url",
              name: "URL",
              type: "text",
              required: true,
            },
            {
              label: "Type bron",
              id: "source_type",
              name: "SourceType",
              type: "dropdown",
              required: true,
              placeholder: "type bron",
              options: this.sourceTypes,
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
              label: "Verstuur authenticatie-informatie naar bron",
              id: "authenticate",
              name: "Authenticate",
              type: "checkbox",
              required: false,
              infoText: "Configureer dit alleen voor vertrouwde bronnen",
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
