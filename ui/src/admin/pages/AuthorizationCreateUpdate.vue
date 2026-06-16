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
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";
import { useQueryCache } from "@pinia/colada";
import { useGroupList, useSourceList } from "@/admin/queries";

export default {
  name: "AuthorizationCreateUpdate",
  components: {
    Spinner,
    AdminFormSections,
  },
  setup() {
    const queryCache = useQueryCache();
    const { sourcesState } = useSourceList();
    const { groupsState, refresh: refreshGroups } = useGroupList();
    return { queryCache, sourcesState, groupsState, refreshGroups };
  },
  data() {
    return {
      initialValues: {},
      loading: false,
    };
  },
  computed: {
    ...mapState(useGlobalStore, ["config"]),
    sections() {
      return this.getSections();
    },
  },
  created() {
    this.loading = true;

    this.getAuthorization()
      .then(() => this.setAtlasGroups())
      .finally(() => {
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
    async saveAuthorization(currentValues, continueEditing = false) {
      currentValues.atlas_groups = currentValues.atlas_groups?.[1]?.map((group) => group.id) || [];
      currentValues.atlas_write_groups = currentValues.atlas_write_groups?.[1]?.map((group) => group.id) || [];

      const url = `/atlas/api/v1/authorizations/${this.$route.params.id}/`;

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          await this.queryCache.invalidateQueries(["authorizations"]);

          if (!continueEditing) {
            this.$router.push(`/authorizations`);
          }

          this.$toast.add({
            severity: "success",
            summary: "Autorisatie opgeslagen",
            detail: "De autorisatie is succesvol opgeslagen.",
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
      const selectedWritableGroups = groups.filter((group) => this.initialValues.atlas_write_groups.includes(group.id));
      const availableWritableGroups = groups.filter(
        (group) => !this.initialValues.atlas_write_groups.includes(group.id),
      );
      this.initialValues.atlas_groups = [availableGroups, selectedGroups];
      this.initialValues.atlas_write_groups = [availableWritableGroups, selectedWritableGroups];
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
              options: this.sourcesState.data,
            },
            {
              label: "Resource",
              id: "resource",
              name: "Resource",
              type: "text",
              required: true,
              infoText: "Naam van de laag of de resource",
              contains_colon: true,
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
              label: "Ingelogde gebruikers kunnen resource of laag bewerken",
              id: "authenticated_can_mutate",
              name: "AuthenticatedCanMutate",
              type: "checkbox",
              required: false,
              infoText:
                "Alle ingelogde gebruikers kunnen wanneer deze optie aanstaat de resource of laag muteren voor kaarten waar de CRUD-functionaliteit is ingeschakeld.",
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
              label: "Lees groepen",
              objectDisplayName: "lees groepen",
              id: "atlas_groups",
              name: "atlasGroups",
              type: "picklist",
            },
            {
              label: "Schrijf groepen",
              objectDisplayName: "schrijf groepen",
              id: "atlas_write_groups",
              name: "atlasWriteGroups",
              type: "picklist",
            },
          ],
        },
      };
    },
  },
};
</script>
