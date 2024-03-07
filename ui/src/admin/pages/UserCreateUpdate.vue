<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Gebruiker wijzigen</h1>
    <AdminFormSections
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :form-object="'users'"
      :object-specific-save="saveUser"
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
              v-model="selectedGroups"
              tag="ul"
              item-key="id"
              group="groups"
              v-bind="dragOptions"
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
import { mapState } from "vuex";
import draggable from "vuedraggable";
draggable.compatConfig = { MODE: 3 };

export default {
  name: "UserCreateUpdateComponent",
  components: { AdminFormSections, draggable },
  data() {
    return {
      sections: {},
      initialValues: {},
      currentValues: {},
      groups: [],
      availableGroups: [],
      selectedGroups: [],
      assistiveText: "Verplaats een group met behulp van de enter toets",
    };
  },
  computed: {
    ...mapState({
      currentUser: (state) => state.user,
    }),
    editingCurrentUser() {
      return this.currentUser.id === this.initialValues.id;
    },
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
    Promise.all([this.getUser(), this.getGroups()]).then(() => {
      this.selectedGroups = this.groups.filter((group) => this.initialValues.atlas_groups.includes(group.id));
      this.availableGroups = this.groups.filter((group) => !this.initialValues.atlas_groups.includes(group.id));

      this.sections = this.getSections();
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
    async saveUser(currentValues) {
      currentValues.atlas_groups = this.selectedGroups.map((group) => group.id);
      currentValues.is_staff = currentValues.is_admin;
      currentValues.is_superuser = currentValues.is_admin;

      const url = `/atlas/api/v1/users/${this.$route.params.id}/`;

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "PATCH", currentValues);

        if (result.ok) {
          this.$router.push(`/users`);
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
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
              required: false,
            },
            {
              label: "E-mailadres",
              id: "email",
              name: "Email",
              type: "email",
              required: false,
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
              type: "custom",
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
