<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Viewers</h1>
        <div class="top-menu-button-container">
          <button class="button __secondary_admin __normal" type="button" @click="toggleAdvance">
            <CogIcon class="icon" />
            {{ advanceSettings ? "Minder" : "Meer" }} opties
          </button>
          <button class="button __primary_admin __normal __full-width-mobile" @click="openFormModal('newViewer')">
            <AddIcon class="icon __white" />
            Nieuwe viewer
          </button>
        </div>
      </div>
    </div>

    <div class="admin-content-wrapper">
      <div v-if="!loading" class="admin-search-wrapper">
        <SearchIcon class="icon" />
        <input id="viewer-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek viewer" />
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
        :items="visibleViewers"
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
              <tr v-for="viewer in paginatedData" :key="viewer.id" class="table-border">
                <td v-if="advanceSettings" class="first-column-padding">
                  <input type="checkbox" :checked="checkedRows.includes(viewer.id)" @change="onCheckRow(viewer.id)" />
                </td>
                <td :class="{ 'first-column-padding': !advanceSettings }">
                  <router-link class="admin-title-link" :to="`/viewers/update/${viewer.id}`">
                    {{ viewer.label }}
                  </router-link>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    aria-label="Wijzig viewer"
                    content="Wijzig"
                    type="button"
                    @click="$router.push(`/viewers/update/${viewer.id}`)"
                  >
                    <EditIcon class="icon" />
                  </button>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    aria-label="Verwijder viewer"
                    content="Verwijder"
                    type="button"
                    @click="deleteViewer(viewer)"
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
        <h3 v-if="modalType === 'newViewer'">Configureer nieuwe viewer</h3>
        <h3 v-else-if="modalType === 'import'">Importeer bestaande viewer(s)</h3>
        <h3 v-else-if="modalType === 'export'">Exporteer bestaande viewer(s)</h3>
      </template>
      <template #body>
        <AdminFormSections
          v-if="modalType === 'newViewer'"
          ref="formSections"
          :sections="sections"
          :initial-values="newViewerData"
          :create-view="true"
          :form-object="'viewers'"
          :object-specific-save="saveViewer"
          @close="closeFormModal"
        />
        <div v-else-if="modalType === 'import'">
          <AdminFileImport :object-name="'viewers'" @import-successful="getViewers" @close="closeFormModal" />
        </div>
        <div v-else-if="modalType === 'export'">
          <AdminFileExport :object-name="'viewers'" :selected-rows="selectedItems" @close="closeFormModal" />
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
  name: "ViewerList",
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
      viewers: [],
      showFormModal: false,
      newViewerData: {},
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
    sortedViewers() {
      if (this.sortKey && this.viewers) {
        return this.viewers.slice(0).sort((a, b) => {
          const textA = a[this.sortKey].toLowerCase();
          const textB = b[this.sortKey].toLowerCase();
          return sortAlphabetically(textA, textB, this.sortAscending);
        });
      }

      return this.viewers;
    },
    visibleViewers() {
      if (!this.searchQuery) {
        return this.sortedViewers;
      }

      return this.sortedViewers.filter(
        (viewer) => viewer.label.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1,
      );
    },
    paginatedData() {
      const start = (this.currentPageNumber - 1) * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.visibleViewers.slice(start, end);
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
    this.getViewers();
    this.sections = this.getSections();
  },
  methods: {
    async getViewers() {
      this.loading = true;
      const result = await fetch("/atlas/api/v1/viewers/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch viewers");
      }

      this.viewers = await result.json();
      this.loading = false;
    },
    async deleteViewer(viewer) {
      const acknowledged = confirm("Weet je zeker dat je deze viewer wilt verwijderen?");
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/viewers/${viewer.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getViewers();
      }
    },
    async saveViewer(currentValues, continueEditing = false) {
      const url = "/atlas/api/v1/viewers/";

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "POST", currentValues);

        if (result.ok) {
          this.closeFormModal();

          if (continueEditing) {
            const response = await result.json();
            this.$router.push(`/viewers/update/${response.id}`);
          }

          await this.getViewers();
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    openFormModal(modalType) {
      if (modalType === "newViewer") {
        this.newViewerData = {
          title: "",
          url: "",
          authenticate: false,
        };
      }

      if (modalType === "export") {
        this.selectedItems = this.viewers.filter((viewer) => this.checkedRows.includes(viewer.id));
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
          this.viewers.forEach((viewer) => {
            this.checkedRows.push(viewer.id);
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
              label: "Label",
              id: "label",
              name: "Label",
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
