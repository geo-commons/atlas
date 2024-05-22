<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Kaarten</h1>
        <div class="top-menu-button-container">
          <button class="button __secondary_admin __normal" type="button" @click="toggleAdvance">
            <CogIcon class="icon" />
            {{ advanceSettings ? "Minder" : "Meer" }} opties
          </button>
          <button
            class="button __primary_admin __normal __full-width-mobile"
            type="button"
            @click="openFormModal('newMap')"
          >
            <AddIcon class="icon __white" />
            Nieuwe kaart
          </button>
        </div>
      </div>
    </div>

    <div class="admin-content-wrapper">
      <div v-if="!loading" class="admin-search-wrapper">
        <SearchIcon class="icon" />
        <input id="maps-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek kaart" />
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
        :items="visibleMaps"
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
              <tr v-for="map in paginatedData" :key="map.id" class="table-border">
                <td v-if="advanceSettings" class="first-column-padding">
                  <input type="checkbox" :checked="checkedRows.includes(map.id)" @change="onCheckRow(map.id)" />
                </td>
                <td :class="{ 'first-column-padding': !advanceSettings }">
                  <router-link
                    class="admin-title-link"
                    type="button"
                    :aria-label="`${map.title} configureren`"
                    :to="`/maps/update/${map.id}`"
                  >
                    {{ map.title }}
                  </router-link>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    aria-label="Bekijk kaart"
                    content="Bekijk"
                    type="button"
                    @click="gotoMap(map)"
                  >
                    <ViewIcon class="icon" />
                  </button>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    aria-label="Verwijder kaart"
                    content="Verwijder"
                    type="button"
                    @click="deleteMap(map)"
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
        <h3 v-if="modalType === 'newMap'">Configureer nieuwe kaart</h3>
        <h3 v-else-if="modalType === 'import'">Importeer bestaande kaart(en)</h3>
        <h3 v-else-if="modalType === 'export'">Exporteer bestaande kaart(en)</h3>
      </template>
      <template #body>
        <AdminFormSections
          v-if="modalType === 'newMap'"
          ref="formSections"
          :sections="sections"
          :initial-values="newMapData"
          :create-view="true"
          :form-object="'maps'"
          :object-specific-save="saveMap"
          @close="closeFormModal"
        />
        <div v-else-if="modalType === 'import'">
          <AdminFileImport :object-name="'kaarten'" @import-successful="getMaps" @close="closeFormModal" />
        </div>
        <div v-else-if="modalType === 'export'">
          <AdminFileExport :object-name="'kaarten'" :selected-rows="selectedItems" @close="closeFormModal" />
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
import ViewIcon from "@/assets/icons/view-icon.svg";
import PaginationComponent from "@/components/Pagination.vue";
import SortableTableHeaderItem from "@/components/SortableTableHeaderItem.vue";
import { sortAlphabetically } from "@/utils/table-sort-helpers";
import AdminFileImport from "@/admin/components/AdminFileImport.vue";
import AdminFileExport from "@/admin/components/AdminFileExport.vue";
import ArrowDownTrayIcon from "@/assets/icons/arrow-down-tray-icon.svg";
import ArrowUpTrayIcon from "@/assets/icons/arrow-up-tray-icon.svg";
import CogIcon from "@/assets/icons/cog-icon.svg";

export default {
  name: "MapList",
  components: {
    CogIcon,
    ArrowUpTrayIcon,
    ArrowDownTrayIcon,
    AdminFileExport,
    AdminFileImport,
    SortableTableHeaderItem,
    PaginationComponent,
    ViewIcon,
    TrashIcon,
    AdminFormSections,
    FormModal,
    AddIcon,
    SearchIcon,
  },
  data() {
    return {
      maps: [],
      currentPageNumber: 1,
      nrOfRecords: 20,
      showFormModal: false,
      newMapData: {},
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
    sortedMaps() {
      if (this.sortKey && this.maps) {
        return this.maps.slice(0).sort((a, b) => {
          const textA = a[this.sortKey].toLowerCase();
          const textB = b[this.sortKey].toLowerCase();
          return sortAlphabetically(textA, textB, this.sortAscending);
        });
      }

      return this.maps;
    },
    visibleMaps() {
      if (!this.searchQuery) {
        return this.sortedMaps;
      }

      return this.sortedMaps.filter((map) => map.title.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1);
    },
    paginatedData() {
      const start = (this.currentPageNumber - 1) * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.visibleMaps.slice(start, end);
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
    this.getMaps();
    this.sections = this.getSections();
  },
  methods: {
    async getMaps() {
      this.loading = true;

      const result = await fetch("/atlas/api/v1/maps/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch maps");
      }

      this.maps = await result.json();
      this.loading = false;
    },
    gotoMap(map) {
      window.location.href = `/atlas/maps/${map.slug}`;
    },
    async saveMap(currentValues, continueEditing = false) {
      const url = "/atlas/api/v1/maps/";

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "POST", { ...currentValues, layers: [] });

        if (result.ok) {
          this.closeFormModal();

          if (continueEditing) {
            const response = await result.json();
            this.$router.push(`/maps/update/${response.id}`);
          }

          await this.getMaps();
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    async deleteMap(map) {
      const acknowledged = confirm("Weet je zeker dat je de kaart wilt verwijderen?");
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/maps/${map.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getMaps();
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
      if (modalType === "kaarten") {
        this.newMapData = {
          title: "",
          authenticate: false,
          layers: [],
        };
      }

      if (modalType === "export") {
        this.selectedItems = this.maps.filter((map) => this.checkedRows.includes(map.id));
      }

      this.modalType = modalType;
      this.showFormModal = true;
    },
    closeFormModal() {
      this.showFormModal = false;
      this.modalType = null;
    },
    updateCurrentValues(newValues) {
      this.newMapData = newValues;
    },
    toggleAdvance() {
      this.advanceSettings = !this.advanceSettings;
    },
    onCheckRow(id, checkAll = false) {
      if (id === null && checkAll) {
        this.allChecked = !this.allChecked;

        if (this.allChecked) {
          this.maps.forEach((map) => {
            this.checkedRows.push(map.id);
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
              required: false,
              infoText: "Een uniek kort kenmerk voor de kaart in Atlas.",
            },
          ],
        },
      };
    },
  },
};
</script>
