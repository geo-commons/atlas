<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Tabellen</h1>
        <div class="top-menu-button-container">
          <button class="button __secondary_admin __normal" type="button" @click="toggleAdvance">
            <CogIcon class="icon" />
            {{ advanceSettings ? "Minder" : "Meer" }} opties
          </button>
          <button
            class="button __primary_admin __normal __full-width-mobile"
            type="button"
            @click="openFormModal('newTable')"
          >
            <AddIcon class="icon __white" />
            Nieuwe tabel
          </button>
        </div>
      </div>
    </div>

    <div class="admin-content-wrapper">
      <div v-if="!loading" class="admin-search-wrapper">
        <SearchIcon class="icon" />
        <input id="tables-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek tabel" />
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
        :items="visibleTables"
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
                    :header-text="'Titel'"
                    :property="'title'"
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
              <tr v-for="table in paginatedData" :key="table.id" class="table-border">
                <td v-if="advanceSettings" class="first-column-padding">
                  <input type="checkbox" :checked="checkedRows.includes(table.id)" @change="onCheckRow(table.id)" />
                </td>
                <td :class="{ 'first-column-padding': !advanceSettings }">
                  <router-link
                    class="admin-title-link"
                    type="button"
                    :aria-label="`${table.title} configureren`"
                    :to="`/tables/update/${table.id}`"
                  >
                    {{ table.title }}
                  </router-link>
                </td>
                <td class="btn-col">
                  <router-link
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    aria-label="Wijzig tabel"
                    content="Wijzig"
                    type="button"
                    :to="`/tables/update/${table.id}`"
                  >
                    <EditIcon class="icon" />
                  </router-link>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    aria-label="Verwijder tabel"
                    content="Verwijder"
                    type="button"
                    @click="deleteTable(table)"
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
        <h3 v-if="modalType === 'newTable'">Configureer nieuwe tabel</h3>
        <h3 v-else-if="modalType === 'import'">Importeer bestaande tabellen</h3>
        <h3 v-else-if="modalType === 'export'">Exporteer bestaande tabellen</h3>
      </template>
      <template #body>
        <AdminFormSections
          v-if="modalType === 'newTable'"
          ref="formSections"
          :sections="sections"
          :initial-values="newTableData"
          :create-view="true"
          :form-object="'tables'"
          :object-specific-save="saveTable"
          @close="closeFormModal"
        />
        <div v-else-if="modalType === 'import'">
          <AdminFileImport :object-name="'tables'" @import-successful="getTables" @close="closeFormModal" />
        </div>
        <div v-else-if="modalType === 'export'">
          <AdminFileExport :object-name="'tables'" :selected-rows="selectedItems" @close="closeFormModal" />
        </div>
      </template>
    </FormModal>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import SearchIcon from "@/assets/icons/search-icon.svg";
import AddIcon from "@/assets/icons/add-icon.svg";
import FormModal from "@/components/FormModal.vue";
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import EditIcon from "@/assets/icons/edit-icon.svg";
import PaginationComponent from "@/components/Pagination.vue";
import SortableTableHeaderItem from "@/components/SortableTableHeaderItem.vue";
import { sortAlphabetically } from "@/utils/table-sort-helpers";
import AdminFileImport from "@/admin/components/AdminFileImport.vue";
import AdminFileExport from "@/admin/components/AdminFileExport.vue";
import ArrowDownTrayIcon from "@/assets/icons/arrow-down-tray-icon.svg";
import ArrowUpTrayIcon from "@/assets/icons/arrow-up-tray-icon.svg";
import CogIcon from "@/assets/icons/cog-icon.svg";

export default {
  name: "TableList",
  components: {
    CogIcon,
    ArrowUpTrayIcon,
    ArrowDownTrayIcon,
    AdminFileExport,
    AdminFileImport,
    SortableTableHeaderItem,
    PaginationComponent,
    EditIcon,
    TrashIcon,
    AdminFormSections,
    FormModal,
    AddIcon,
    SearchIcon,
  },
  data() {
    return {
      tables: [],
      currentPageNumber: 1,
      nrOfRecords: 20,
      showFormModal: false,
      newTableData: {},
      searchQuery: "",
      sections: {},
      sortKey: "",
      sortAscending: true,
      loading: false,
      advanceSettings: false,
      checkedRows: [],
      selectedItems: null,
      modalType: null,
    };
  },
  computed: {
    sortedTables() {
      if (this.sortKey && this.tables) {
        return this.tables.slice(0).sort((a, b) => {
          const textA = a[this.sortKey].toLowerCase();
          const textB = b[this.sortKey].toLowerCase();
          return sortAlphabetically(textA, textB, this.sortAscending);
        });
      }

      return this.tables;
    },
    visibleTables() {
      if (!this.searchQuery) {
        return this.sortedTables;
      }

      return this.sortedTables.filter(
        (table) => table.title.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1,
      );
    },
    paginatedData() {
      const start = (this.currentPageNumber - 1) * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.visibleTables.slice(start, end);
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
    this.getTables();
    this.sections = this.getSections();
  },
  methods: {
    async getTables() {
      this.loading = true;

      const result = await fetch("/atlas/api/v1/tables/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch tables");
      }

      this.tables = await result.json();
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
        return { id: source.id, label: source.title };
      });
    },
    async saveTable(currentValues, continueEditing = false) {
      const url = "/atlas/api/v1/tables/";

      currentValues.method = "GET";
      currentValues.endpoint = "/";

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "POST", currentValues);

        if (result.ok) {
          this.closeFormModal();

          if (continueEditing) {
            const response = await result.json();
            this.$router.push(`/tables/update/${response.id}`);
          }

          await this.getTables();
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    async deleteTable(table) {
      const acknowledged = confirm("Weet je zeker dat je de tabel wilt verwijderen?");
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/tables/${table.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getTables();
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
    openFormModal(modalType) {
      if (modalType === "newTable") {
        this.newTableData = {
          title: "",
          authenticate: false,
          layers: [],
        };
      }

      if (modalType === "export") {
        this.selectedItems = this.tables.filter((table) => this.checkedRows.includes(table.id));
      }

      this.modalType = modalType;
      this.showFormModal = true;
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
          this.tables.forEach((table) => {
            this.checkedRows.push(table.id);
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
              required: true,
            },
            {
              label: "Bron",
              id: "source",
              name: "Source",
              type: "dropdown",
              required: true,
              placeholder: "bron",
              options: this.getSources,
            },
          ],
        },
      };
    },
  },
};
</script>
