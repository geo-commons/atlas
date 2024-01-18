<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Groepen</h1>

        <div class="top-menu-button-container">
          <button class="button __primary __normal" type="button" @click="openFormModal">
            <AddIcon class="icon __white" />
            Nieuwe groep
          </button>
        </div>
      </div>
    </div>

    <div class="admin-content-wrapper">
      <div v-if="!loading" class="admin-search-wrapper">
        <SearchIcon class="icon" />
        <input id="groups-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek groep" />
      </div>

      <PaginationComponent
        :items="visibleGroups"
        :nr-of-records="nrOfRecords"
        :loading="loading"
        @page-change="(pageNumber) => (currentPageNumber = pageNumber)"
        @records-change="(value) => (nrOfRecords = value)"
      >
        <template #default>
          <table class="admin-table">
            <thead>
              <tr class="table-border">
                <th class="first-column-padding">
                  <SortableTableHeaderItem
                    :header-text="'Groep'"
                    :property="'name'"
                    :sort-key="sortKey"
                    :sort-ascending="sortAscending"
                    @sort="(column) => sortColumn(column)"
                  />
                </th>
                <th class="btn-col"></th>
                <th class="btn-col"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="group in paginatedData" :key="group.id" class="table-border">
                <td class="first-column-padding">
                  <router-link
                    class="admin-title-link"
                    type="button"
                    :aria-label="`${group.name} configureren`"
                    :to="`/groups/update/${group.id}`"
                  >
                    {{ group.name }}
                  </router-link>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __alt_hover"
                    :aria-label="`${group.name} configureren`"
                    content="Wijzig"
                    type="button"
                    @click="$router.push(`/groups/update/${group.id}`)"
                  >
                    <EditIcon class="icon" />
                  </button>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __alt_hover"
                    aria-label="Verwijder groep"
                    content="Verwijder"
                    type="button"
                    @click="deleteGroup(group)"
                  >
                    <TrashIcon class="icon" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </template>
      </PaginationComponent>
    </div>

    <FormModal v-if="showFormModal" :toggle-modal="showFormModal" @close="closeFormModal">
      <template #header><h3>Configureer nieuwe groep</h3></template>
      <template #body>
        <AdminFormSections
          ref="formSections"
          :sections="sections"
          :initial-values="newGroupData"
          :create-view="true"
          :form-object="'groups'"
          :object-specific-save="saveGroup"
          @close="closeFormModal"
        />
      </template>
    </FormModal>
  </div>
</template>

<script>
import SearchIcon from "@/assets/icons/search-icon.svg";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import EditIcon from "@/assets/icons/edit-icon.svg";
import SortableTableHeaderItem from "@/components/SortableTableHeaderItem.vue";
import PaginationComponent from "@/components/Pagination.vue";
import { sortAlphabetically } from "@/utils/table-sort-helpers";
import Cookies from "js-cookie";
import AddIcon from "@/assets/icons/add-icon.svg";
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import FormModal from "@/components/FormModal.vue";

export default {
  name: "GroupList",
  components: {
    FormModal,
    AdminFormSections,
    AddIcon,
    TrashIcon,
    SearchIcon,
    EditIcon,
    PaginationComponent,
    SortableTableHeaderItem,
  },
  data() {
    return {
      groups: [],
      newGroupData: null,
      showFormModal: false,
      searchQuery: "",
      currentPageNumber: 1,
      nrOfRecords: 20,
      sortKey: "",
      sortAscending: true,
      loading: false,
      sections: {},
    };
  },
  computed: {
    sortedGroups() {
      if (this.sortKey && this.groups) {
        return this.groups.slice(0).sort((a, b) => {
          const textA = a[this.sortKey]?.toLowerCase();
          const textB = b[this.sortKey]?.toLowerCase();
          return sortAlphabetically(textA, textB, this.sortAscending);
        });
      }

      return this.groups;
    },
    visibleGroups() {
      if (!this.searchQuery) {
        return this.sortedGroups;
      }

      return this.sortedGroups.filter(
        (group) => group.name.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1
      );
    },
    paginatedData() {
      const start = (this.currentPageNumber - 1) * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.visibleGroups.slice(start, end);
    },
  },
  created() {
    this.getGroups();
    this.sections = this.getSections();
  },
  methods: {
    async getGroups() {
      this.loading = true;

      const result = await fetch("/atlas/api/v1/groups/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch groups");
      }

      this.groups = await result.json();
      this.loading = false;
    },
    async saveGroup(currentValues, continueEditing = false) {
      const url = "/atlas/api/v1/groups/";

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "POST", currentValues);

        if (result.ok) {
          this.closeFormModal();

          if (continueEditing) {
            const response = await result.json();
            this.$router.push(`/groups/update/${response.id}`);
          }

          await this.getGroups();
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    async deleteGroup(group) {
      const acknowledged = confirm("Weet je zeker dat je de groep wilt verwijderen?");
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/groups/${group.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getGroups();
      }
    },
    sortColumn(prop) {
      if (this.sortKey !== prop) {
        this.sortKey = prop;
        this.sortAscending = true;
      } else {
        this.sortAscending = !this.sortAscending;
      }
    },
    openFormModal() {
      this.newGroupData = {
        title: "",
        authenticate: false,
      };

      this.showFormModal = true;
    },
    closeFormModal() {
      this.showFormModal = false;
    },
    getSections() {
      return {
        general: {
          label: "Algemene gegevens",
          questions: [
            {
              label: "Groep",
              id: "name",
              name: "Name",
              type: "text",
              required: true,
            },
          ],
        },
      };
    },
  },
};
</script>

<style scoped></style>
