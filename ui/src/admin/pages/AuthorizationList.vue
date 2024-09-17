<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Autorisaties</h1>
        <div class="top-menu-button-container">
          <button class="button __secondary_admin __normal" type="button" @click="toggleAdvance">
            <CogIcon class="icon" />
            {{ advanceSettings ? "Minder" : "Meer" }} opties
          </button>
          <button
            class="button __primary_admin __normal __full-width-mobile"
            @click="openFormModal('newAuthorization')"
          >
            <AddIcon class="icon __white" />
            Nieuwe autorisatie
          </button>
        </div>
      </div>
    </div>

    <div class="admin-content-wrapper">
      <div v-if="!loading" class="admin-search-wrapper">
        <SearchIcon class="icon" />
        <input
          id="authorization-search"
          v-model="searchQuery"
          type="search"
          name="query"
          placeholder="Zoek autorisatie"
        />
      </div>

      <div v-if="advanceSettings" class="advance-settings-wrapper">
        <div class="advance-button-wrapper">
          <button class="button __secondary_admin __normal" type="button" @click="openFormModal('import')">
            <ArrowDownTrayIcon class="icon" />
            Importeren
          </button>
          <button class="button __secondary_admin __normal" type="button" @click="openFormModal('export')">
            <ArrowUpTrayIcon class="icon" />
            Exporteren
          </button>
        </div>
        <span>{{ selectedRowsDisplayText }}</span>
      </div>

      <PaginationComponent
        :items="visibleAuthorizations"
        :nr-of-records="nrOfRecords"
        :loading="loading"
        :style-type="'admin'"
        @page-change="(pageNumber) => (currentPageNumber = pageNumber)"
        @records-change="(value) => (nrOfRecords = value)"
      >
        <template #default>
          <table class="admin-table">
            <thead>
              <tr class="table-border">
                <th v-if="advanceSettings" class="first-column-padding">
                  <input type="checkbox" @change="onCheckRow(null, true)" />
                </th>
                <th :class="{ 'first-column-padding': !advanceSettings }">
                  <SortableTableHeaderItem
                    :header-text="'Resource'"
                    :property="'resource'"
                    :sort-key="sortKey"
                    :sort-ascending="sortAscending"
                    @sort="(column) => sortColumn(column)"
                  />
                </th>
                <th></th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="authorization in paginatedData" :key="authorization.id" class="table-border">
                <td v-if="advanceSettings" class="first-column-padding">
                  <input
                    type="checkbox"
                    :checked="checkedRows.includes(authorization.id)"
                    @change="onCheckRow(authorization.id)"
                  />
                </td>
                <td :class="{ 'first-column-padding': !advanceSettings }">
                  <router-link class="admin-title-link" :to="`/authorizations/update/${authorization.id}`">
                    {{ authorization.resource }}
                  </router-link>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    aria-label="Wijzig autorisatie"
                    content="Wijzig"
                    type="button"
                    @click="$router.push(`/authorizations/update/${authorization.id}`)"
                  >
                    <EditIcon class="icon" />
                  </button>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    aria-label="Verwijder autorisatie"
                    content="Verwijder"
                    type="button"
                    @click="deleteAuthorization(authorization)"
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
      <template #header>
        <h3 v-if="modalType === 'newAuthorization'">Configureer nieuwe autorisatie</h3>
        <h3 v-else-if="modalType === 'import'">Importeer bestaande autorisatie(s)</h3>
        <h3 v-else-if="modalType === 'export'">Exporteer bestaande autorisatie(s)</h3>
      </template>
      <template #body>
        <AdminFormSections
          v-if="modalType === 'newAuthorization'"
          ref="formSections"
          :sections="sections"
          :initial-values="newAuthorizationData"
          :create-view="true"
          :form-object="'authorizations'"
          :object-specific-save="saveAuthorization"
          @close="closeFormModal"
        />
        <div v-else-if="modalType === 'import'">
          <AdminFileImport
            :object-name="'authorizations'"
            @import-successful="getAuthorizations"
            @close="closeFormModal"
          />
        </div>
        <div v-else-if="modalType === 'export'">
          <AdminFileExport :object-name="'authorizations'" :selected-rows="selectedItems" @close="closeFormModal" />
        </div>
      </template>
    </FormModal>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import AddIcon from "@/assets/icons/add-icon.svg";
import FormModal from "@/components/FormModal.vue";
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import SortableTableHeaderItem from "@/components/SortableTableHeaderItem.vue";
import EditIcon from "@/assets/icons/edit-icon.svg";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import { sortAlphabetically } from "@/utils/table-sort-helpers";
import PaginationComponent from "@/components/Pagination.vue";
import SearchIcon from "@/assets/icons/search-icon.svg";
import CogIcon from "@/assets/icons/cog-icon.svg";
import ArrowUpTrayIcon from "../../assets/icons/arrow-up-tray-icon.svg";
import ArrowDownTrayIcon from "../../assets/icons/arrow-down-tray-icon.svg";
import AdminFileExport from "@/admin/components/AdminFileExport.vue";
import AdminFileImport from "@/admin/components/AdminFileImport.vue";

export default {
  name: "AuthorizationList",
  components: {
    SearchIcon,
    PaginationComponent,
    TrashIcon,
    EditIcon,
    SortableTableHeaderItem,
    AdminFormSections,
    FormModal,
    AddIcon,
    CogIcon,
    ArrowUpTrayIcon,
    ArrowDownTrayIcon,
    AdminFileExport,
    AdminFileImport,
  },
  data() {
    return {
      authorizations: [],
      showFormModal: false,
      newAuthorizationData: {},
      searchQuery: "",
      sections: {},
      currentPageNumber: 1,
      nrOfRecords: 20,
      sortAscending: true,
      sortKey: "",
      loading: false,
      advanceSettings: false,
      checkedRows: [],
      selectedItems: null,
      modalType: null,
    };
  },
  computed: {
    sortedAuthorizations() {
      if (this.sortKey && this.authorizations) {
        return this.authorizations.slice(0).sort((a, b) => {
          const textA = a[this.sortKey].toLowerCase();
          const textB = b[this.sortKey].toLowerCase();
          return sortAlphabetically(textA, textB, this.sortAscending);
        });
      }

      return this.authorizations;
    },
    visibleAuthorizations() {
      if (!this.searchQuery) {
        return this.sortedAuthorizations;
      }

      return this.sortedAuthorizations.filter(
        (authorization) => authorization.resource.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1,
      );
    },
    paginatedData() {
      const start = (this.currentPageNumber - 1) * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.visibleAuthorizations.slice(start, end);
    },
    selectedRowsDisplayText() {
      const nrOfRows = this.checkedRows.length;

      if (!nrOfRows) {
        return "Geen rijen geselecteerd";
      }

      if (nrOfRows === 1) {
        return "1 rij geselecteerd";
      }

      return nrOfRows + " rijen geselecteerd";
    },
  },
  created() {
    this.getAuthorizations();
    this.sections = this.getSections();
  },
  methods: {
    async getAuthorizations() {
      this.loading = true;
      const result = await fetch("/atlas/api/v1/authorizations/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch authorizations");
      }

      this.authorizations = await result.json();
      this.loading = false;
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
    async deleteAuthorization(authorization) {
      const acknowledged = confirm("Weet je zeker dat je de autorisatie wilt verwijderen?");
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/authorizations/${authorization.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getAuthorizations();
      }
    },
    async saveAuthorization(currentValues, continueEditing = false) {
      const url = "/atlas/api/v1/authorizations/";

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "POST", currentValues);

        if (result.ok) {
          this.closeFormModal();

          if (continueEditing) {
            const response = await result.json();
            this.$router.push(`/authorizations/update/${response.id}`);
          }

          await this.getAuthorizations();
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    openFormModal(modalType) {
      if (modalType === "newAuthorization") {
        this.newAuthorizationData = {
          source: "",
          resource: "",
        };
      }

      if (modalType === "export") {
        this.selectedItems = this.authorizations.filter((authorization) => this.checkedRows.includes(authorization.id));
      }

      this.showFormModal = true;
      this.modalType = modalType;
    },
    closeFormModal() {
      this.showFormModal = false;
      this.modalType = null;
    },
    toggleAdvance() {
      this.advanceSettings = !this.advanceSettings;
    },
    onCheckRow(id, checkAll = false) {
      if (id === null && checkAll) {
        this.allChecked = !this.allChecked;

        if (this.allChecked) {
          this.authorizations.forEach((authorization) => {
            this.checkedRows.push(authorization.id);
          });
        } else {
          this.checkedRows = [];
        }

        return;
      }

      if (this.checkedRows.includes(id)) {
        const index = this.checkedRows.indexOf(id);
        this.checkedRows.splice(index, 1);
        return;
      }

      this.checkedRows.push(id);
    },
    sortColumn(prop) {
      if (this.sortKey !== prop) {
        this.sortKey = prop;
        this.sortAscending = true;
      } else {
        this.sortAscending = !this.sortAscending;
      }
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
          ],
        },
      };
    },
  },
};
</script>
