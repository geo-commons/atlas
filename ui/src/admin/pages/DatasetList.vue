<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Datasets</h1>
        <div class="top-menu-button-container">
          <button class="button __secondary_admin __normal" type="button" @click="toggleAdvance">
            <CogIcon class="icon" />
            {{ advanceSettings ? "Minder" : "Meer" }} opties
          </button>
          <button class="button __primary_admin __normal" type="button" @click="openFormModal('newDataset')">
            <AddIcon class="icon __white" />
            Nieuwe dataset
          </button>
        </div>
      </div>
    </div>

    <div class="admin-content-wrapper">
      <div v-if="!loading" class="admin-search-wrapper">
        <SearchIcon class="icon" />
        <input id="datasets-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek dataset" />
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
        :items="visibleDatasets"
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
                <th :class="{ 'first-column-padding': !advanceSettings }">
                  <SortableTableHeaderItem
                    :header-text="'Categorie'"
                    :property="categorySortProperty"
                    :sort-key="sortKey"
                    :sort-ascending="sortAscending"
                    @sort="(column) => sortColumn(column)"
                  />
                </th>
                <th :class="{ 'first-column-padding': !advanceSettings }">
                  <SortableTableHeaderItem
                    :header-text="`Thema's`"
                    :property="themesSortProperty"
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
              <tr v-for="dataset in paginatedData" :key="dataset.id" class="table-border">
                <td v-if="advanceSettings" class="first-column-padding">
                  <input type="checkbox" :checked="checkedRows.includes(dataset.id)" @change="onCheckRow(dataset.id)" />
                </td>
                <td :class="{ 'first-column-padding': !advanceSettings }">
                  <router-link
                    class="admin-title-link"
                    type="button"
                    :aria-label="`${dataset.title} configureren`"
                    :to="`/datasets/update/${dataset.id}`"
                  >
                    {{ dataset.title }}
                  </router-link>
                </td>
                <td :class="{ 'first-column-padding': !advanceSettings }">
                  {{ dataset.dataset_category !== null ? dataset.dataset_category.title : "-" }}
                </td>
                <td :class="{ 'first-column-padding': !advanceSettings }">
                  <span v-if="dataset.themes.length > 0">
                    <div v-for="theme in dataset.themes" :key="theme.id">
                      {{ theme.title }}
                    </div>
                  </span>
                  <span v-else> - </span>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    :aria-label="`${dataset.title} configureren`"
                    content="Wijzig"
                    type="button"
                    @click="$router.push(`/datasets/update/${dataset.id}`)"
                  >
                    <EditIcon class="icon" />
                  </button>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    aria-label="Verwijder dataset"
                    content="Verwijder"
                    type="button"
                    @click="deleteDataset(dataset)"
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
        <h3 v-if="modalType === 'newDataset'">Configureer nieuwe dataset</h3>
        <h3 v-else-if="modalType === 'import'">Importeer bestaande datasets</h3>
        <h3 v-else-if="modalType === 'export'">Exporteer bestaande datasets</h3>
      </template>
      <template #body>
        <AdminFormSections
          v-if="modalType === 'newDataset'"
          ref="formSections"
          :sections="sections"
          :initial-values="newDatasetData"
          :create-view="true"
          :form-object="'datasets'"
          :object-specific-save="saveDataset"
          @close="closeFormModal"
        />
        <div v-else-if="modalType === 'import'">
          <AdminFileImport :object-name="'datasets'" @import-successful="getDatasets" @close="closeFormModal" />
        </div>
        <div v-else-if="modalType === 'export'">
          <AdminFileExport :object-name="'datasets'" :selected-rows="selectedItems" @close="closeFormModal" />
        </div>
      </template>
    </FormModal>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import PaginationComponent from "@/components/Pagination.vue";
import FormModal from "@/components/FormModal.vue";
import SortableTableHeaderItem from "@/components/SortableTableHeaderItem.vue";
import { sortAlphabetically } from "@/utils/table-sort-helpers";
import TrashIcon from "../../assets/icons/trash-icon.svg";
import EditIcon from "../../assets/icons/edit-icon.svg";
import AddIcon from "../../assets/icons/add-icon.svg";
import SearchIcon from "../../assets/icons/search-icon.svg";
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import CogIcon from "@/assets/icons/cog-icon.svg";
import ArrowDownTrayIcon from "@/assets/icons/arrow-down-tray-icon.svg";
import ArrowUpTrayIcon from "@/assets/icons/arrow-up-tray-icon.svg";
import AdminFileImport from "@/admin/components/AdminFileImport.vue";
import AdminFileExport from "@/admin/components/AdminFileExport.vue";
import slugify from "slugify";

export default {
  name: "DatasetList",
  components: {
    AdminFileExport,
    AdminFileImport,
    ArrowUpTrayIcon,
    ArrowDownTrayIcon,
    CogIcon,
    AdminFormSections,
    SortableTableHeaderItem,
    FormModal,
    PaginationComponent,
    TrashIcon,
    EditIcon,
    AddIcon,
    SearchIcon,
  },
  data() {
    return {
      datasets: [],
      newDatasetData: null,
      searchQuery: "",
      currentPageNumber: 1,
      nrOfRecords: 20,
      showFormModal: false,
      sortKey: "",
      sortAscending: true,
      sections: {},
      loading: false,
      advanceSettings: false,
      checkedRows: [],
      selectedItems: null,
      modalType: null,
      categorySortProperty: "dataset_category",
      themesSortProperty: "themes",
    };
  },
  computed: {
    sortedDatasets() {
      if (this.sortKey && this.datasets) {
        return this.datasets.slice(0).sort((a, b) => {
          const textA = this.getSortValue(a);
          const textB = this.getSortValue(b);
          return sortAlphabetically(textA, textB, this.sortAscending);
        });
      }

      return this.datasets;
    },
    visibleDatasets() {
      if (!this.searchQuery) {
        return this.sortedDatasets;
      }

      return this.sortedDatasets.filter(
        (dataset) => dataset.title.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1,
      );
    },
    paginatedData() {
      const start = (this.currentPageNumber - 1) * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.visibleDatasets.slice(start, end);
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
    this.getDatasets();

    this.sections = this.getSections();
  },
  methods: {
    async getDatasets() {
      this.loading = true;

      const result = await fetch("/atlas/api/v1/datasets/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch datasets");
      }

      this.datasets = await result.json();

      this.loading = false;
    },
    async saveDataset(currentValues, continueEditing = false) {
      const url = "/atlas/api/v1/datasets/";

      currentValues.themes = [];
      currentValues.slug = slugify(currentValues.title);

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "POST", currentValues);

        if (result.ok) {
          this.closeFormModal();

          if (continueEditing) {
            const response = await result.json();
            this.$router.push(`/datasets/update/${response.id}`);
          }

          await this.getDatasets();
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    async deleteDataset(dataset) {
      const acknowledged = confirm("Weet je zeker dat je deze dataset wilt verwijderen?");
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/datasets/${dataset.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getDatasets();
      }
    },
    getSortValue(sortItem) {
      if (this.sortKey === this.categorySortProperty) {
        return sortItem[this.sortKey] ? sortItem[this.sortKey]?.title.toLowerCase() : "";
      }

      if (this.sortKey === this.themesSortProperty) {
        return sortItem[this.sortKey] ? sortItem[this.sortKey]?.[0]?.title.toLowerCase() : "";
      }

      return sortItem[this.sortKey].toLowerCase();
    },
    openFormModal(modalType) {
      if (modalType === "newDataset") {
        this.newDatasetData = {
          title: "",
          authenticate: false,
        };
      }

      if (modalType === "export") {
        this.selectedItems = this.datasets.filter((dataset) => this.checkedRows.includes(dataset.id));
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
    sortColumn(prop) {
      if (this.sortKey !== prop) {
        this.sortKey = prop;
        this.sortAscending = true;
      } else {
        this.sortAscending = !this.sortAscending;
      }
    },
    onCheckRow(id, checkAll = false) {
      if (id === null && checkAll) {
        this.allChecked = !this.allChecked;

        if (this.allChecked) {
          this.datasets.forEach((dataset) => {
            this.checkedRows.push(dataset.id);
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
              label: "Naam",
              id: "title",
              name: "Title",
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
