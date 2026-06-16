<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Gebruiker wijzigen</h1>
    <Spinner v-if="loading" style-type="'admin'" />
    <AdminFormSections
      v-else
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :form-object="'users'"
      :object-specific-save="saveUser"
    />
  </div>
</template>

<script>
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";
import Spinner from "@/components/Spinner.vue";
import { useQueryCache } from "@pinia/colada";
import { useGroupList } from "@/admin/queries";

export default {
  name: "UserCreateUpdateComponent",
  components: { Spinner, AdminFormSections },
  setup() {
    const queryCache = useQueryCache();
    const { groupsState, refresh: refreshGroups } = useGroupList();
    return { queryCache, groupsState, refreshGroups };
  },
  data() {
    return {
      initialValues: {},
      loading: false,
    };
  },
  computed: {
    ...mapState(useGlobalStore, {
      currentUser: "user",
    }),
    editingCurrentUser() {
      return this.currentUser.id === this.initialValues.id;
    },
    sections() {
      return this.getSections();
    },
  },
  created() {
    this.loading = true;
    this.getUser()
      .then(() => this.setAtlasGroups())
      .finally(() => {
        this.loading = false;
      });
  },
  methods: {
    async getUser() {
      const result = await fetch(`/atlas/api/v1/users/${this.$route.params.id}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch user");
        return;
      }

      this.initialValues = await result.json();
      this.initialValues.is_admin = this.initialValues.is_staff && this.initialValues.is_superuser;

      return result;
    },
    async setAtlasGroups() {
      await this.refreshGroups();
      const groups = this.groupsState.data || [];
      const groupsFromInitialValues = this.initialValues.atlas_groups.map((group) => group.id);
      const selectedGroups = groups.filter((group) => groupsFromInitialValues.includes(group.id));
      const availableGroups = groups.filter((group) => !groupsFromInitialValues.includes(group.id));
      this.initialValues.atlas_groups = [availableGroups, selectedGroups];
    },
    async saveUser(currentValues, continueEditing = false) {
      currentValues.atlas_groups = currentValues.atlas_groups?.[1]?.map((group) => group.id) || [];
      currentValues.is_staff = currentValues.is_admin;
      currentValues.is_superuser = currentValues.is_admin;

      const url = `/atlas/api/v1/users/${this.$route.params.id}/`;

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          await this.queryCache.invalidateQueries(["users"]);

          if (!continueEditing) {
            this.$router.push(`/users`);
          }

          this.$toast.add({
            severity: "success",
            summary: "Gebruiker opgeslagen",
            detail: "De gebruiker is succesvol opgeslagen.",
            life: 3000,
          });
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    getSections() {
      return {
        general: {
          label: "Algemene gegevens",
          questions: [
            {
              label: "Gebruikersnaam",
              id: "username",
              name: "Username",
              type: "text",
              required: true,
              disabled: this.editingCurrentUser,
              infoText:
                "Vereist. 150 tekens of minder. Alleen letters, cijfers en de tekens @/,/+/-/_ zijn toegestaan.",
            },
            {
              label: "Externe ID",
              id: "external_id",
              name: "externalId",
              type: "label",
              infoText: "Het unieke kenmerk van de gebruiker in de inlogbron.",
            },
          ],
        },
        personal: {
          label: "Persoonlijke gegevens",
          questions: [
            {
              label: "Volledige naam",
              id: "name",
              name: "Name",
              type: "text",
              required: true,
            },
            {
              label: "E-mailadres",
              id: "email",
              name: "Email",
              type: "email",
              required: true,
            },
          ],
        },
        permissions: {
          label: "Rechten",
          questions: [
            {
              label: "Actief",
              id: "is_active",
              name: "isActive",
              type: "checkbox",
              required: false,
              disabled: this.editingCurrentUser,
              infoText:
                "Bepaalt of deze gebruiker als actief dient te worden behandeld. U kunt dit uitvinken in plaats van een gebruiker te verwijderen.",
            },
            {
              label: "Beheerder",
              id: "is_admin",
              name: "isAdmin",
              type: "checkbox",
              required: false,
              disabled: this.editingCurrentUser,
              infoText:
                "Bepaalt of de gebruiker zich op deze beheerwebsite kan aanmelden met alle bijbehorende rechten.",
            },
          ],
        },
        groups: {
          label: "Groepen",
          questions: [
            {
              label: "Groepen",
              objectDisplayName: "groepen",
              id: "atlas_groups",
              name: "atlasGroups",
              type: "picklist",
            },
          ],
        },
        dates: {
          label: "Belangrijke datums",
          questions: [
            {
              label: "Datum toegetreden",
              id: "date_joined",
              name: "dateJoined",
              type: "display_date",
            },
            {
              label: "Laatste aanmelding",
              id: "last_login",
              name: "lastJoined",
              type: "display_date",
            },
          ],
        },
      };
    },
  },
};
</script>

<style scoped></style>
