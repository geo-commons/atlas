<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Kaartlagen</h1>
        <div class="top-menu-button-container">
          <button class="button __secondary_admin __normal" type="button" @click="toggleAdvance">
            <CogIcon class="icon" />
            {{ advanceSettings ? "Minder" : "Meer" }} opties
          </button>
          <router-link
            :to="{
              name: 'sort',
              params: { parentRoute: 'layers' },
            }"
            class="button __secondary_admin __normal"
            type="button"
            aria-label="Ga naar sortering pagina"
          >
            <SortIcon class="icon" />
            Sortering
          </router-link>
          <button class="button __primary_admin __normal" type="button" @click="openFormModal('newLayer')">
            <AddIcon class="icon __white" />
            Nieuwe laag
          </button>
        </div>
      </div>
    </div>

    <div class="admin-content-wrapper">
      <div v-show="!loading" class="search-filter-container">
        <div class="admin-search-wrapper">
          <SearchIcon class="icon" />
          <input id="layers-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek laag" />
        </div>
        <div class="filter-wrapper">
          <FilterSelect
            v-if="categories.length > 0"
            :filter-options="categories"
            :field-filters="selectedLayerFilters"
            :filter-property="categoryFilterProperty"
            :filter-property-display-name="'Categorie'"
            @onFilterChange="(v) => setTableFilters(v)"
          />
          <FilterSelect
            :filter-options="status"
            :field-filters="selectedLayerFilters"
            :filter-property="statusFilterProperty"
            :filter-property-display-name="'Status'"
            @onFilterChange="(v) => setTableFilters(v)"
          />
        </div>
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
        :items="visibleLayers"
        :loading="loading"
        :nr-of-records="nrOfRecords"
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
                <th>
                  <SortableTableHeaderItem
                    :header-text="'Categorie'"
                    :property="categoryFilterProperty"
                    :sort-key="sortKey"
                    :sort-ascending="sortAscending"
                    @sort="(column) => sortColumn(column)"
                  />
                </th>
                <th>
                  <SortableTableHeaderItem
                    :header-text="'Status'"
                    :property="statusFilterProperty"
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
              <tr v-for="layer in paginatedData" :key="layer.id" class="table-border">
                <td v-if="advanceSettings" class="first-column-padding">
                  <input type="checkbox" :checked="checkedRows.includes(layer.id)" @change="onCheckRow(layer.id)" />
                </td>
                <td :class="{ 'first-column-padding': !advanceSettings }">
                  <router-link
                    class="admin-title-link"
                    type="button"
                    :aria-label="`${layer.title} configureren`"
                    :to="`/layers/update/${layer.id}`"
                  >
                    {{ layer.title }}
                  </router-link>
                </td>
                <td>
                  {{ layer.category?.title }}
                </td>
                <td>
                  {{ layer.status }}
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    :aria-label="`${layer.title} configureren`"
                    content="Wijzig"
                    type="button"
                    @click="$router.push(`/layers/update/${layer.id}`)"
                  >
                    <EditIcon class="icon" />
                  </button>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    aria-label="Verwijder laag"
                    content="Verwijder"
                    type="button"
                    @click="deleteLayer(layer)"
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

    <FormModal v-show="showFormModal" :toggle-modal="showFormModal" @close="closeFormModal">
      <template #header>
        <h3 v-if="modalType === 'newLayer'">Configureer nieuwe kaartlaag</h3>
        <h3 v-else-if="modalType === 'import'">Importeer bestaande kaartlaag</h3>
        <h3 v-else-if="modalType === 'export'">Exporteer bestaande kaartlagen</h3>
      </template>
      <template #body>
        <AdminFormSections
          v-if="modalType === 'newLayer'"
          ref="formSections"
          :sections="sections"
          :initial-values="newLayerData"
          :create-view="true"
          :form-object="'layers'"
          :object-specific-save="saveLayer"
          @close="closeFormModal"
        />
        <div v-else-if="modalType === 'import'">
          <AdminFileImport :object-name="'kaartlagen'" @import-successful="getLayers" @close="closeFormModal" />
        </div>
        <div v-else-if="modalType === 'export'">
          <AdminFileExport :object-name="'kaartlagen'" :selected-rows="selectedItems" @close="closeFormModal" />
        </div>
      </template>
    </FormModal>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import PaginationComponent from "@/components/Pagination.vue";
import FormModal from "@/components/FormModal.vue";
import FilterSelect from "@/components/FilterSelect.vue";
import SortableTableHeaderItem from "@/components/SortableTableHeaderItem.vue";
import { sortAlphabetically } from "@/utils/table-sort-helpers";
import TrashIcon from "../../assets/icons/trash-icon.svg";
import EditIcon from "../../assets/icons/edit-icon.svg";
import AddIcon from "../../assets/icons/add-icon.svg";
import ArrowUpTrayIcon from "../../assets/icons/arrow-up-tray-icon.svg";
import ArrowDownTrayIcon from "../../assets/icons/arrow-down-tray-icon.svg";
import CogIcon from "../../assets/icons/cog-icon.svg";
import SearchIcon from "../../assets/icons/search-icon.svg";
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import SortIcon from "@/assets/icons/sort-icon.svg";
import AdminFileExport from "@/admin/components/AdminFileExport.vue";
import AdminFileImport from "@/admin/components/AdminFileImport.vue";

export default {
  name: "LayerList",
  components: {
    AdminFileImport,
    AdminFileExport,
    SortIcon,
    AdminFormSections,
    SortableTableHeaderItem,
    FilterSelect,
    FormModal,
    PaginationComponent,
    TrashIcon,
    EditIcon,
    AddIcon,
    ArrowUpTrayIcon,
    ArrowDownTrayIcon,
    CogIcon,
    SearchIcon,
  },
  data() {
    return {
      layers: [],
      categories: [],
      status: [],
      categoryFilterProperty: "category",
      statusFilterProperty: "status",
      newLayerData: null,
      searchQuery: "",
      currentPageNumber: 1,
      nrOfRecords: 20,
      showFormModal: false,
      selectedLayerFilters: {},
      sortKey: "",
      sortAscending: true,
      sections: {},
      loading: false,
      advanceSettings: false,
      checkedRows: [],
      selectedItems: null,
      modalType: null,
    };
  },
  computed: {
    sortedLayers() {
      if (this.sortKey && this.layers) {
        return this.layers.slice(0).sort((a, b) => {
          const textA = this.getSortValue(a);
          const textB = this.getSortValue(b);
          return sortAlphabetically(textA, textB, this.sortAscending);
        });
      }

      return this.layers;
    },
    filteredLayers() {
      const nrOfFilters = Object.keys(this.selectedLayerFilters).length;

      // Check if any filters are selected.
      if (nrOfFilters === 0) {
        return this.sortedLayers;
      }

      if (nrOfFilters === 1 && this.selectedLayerFilters[this.categoryFilterProperty]) {
        return this.sortedLayers.filter(this.checkCategory);
      }

      if (nrOfFilters === 1 && this.selectedLayerFilters[this.statusFilterProperty]) {
        return this.sortedLayers.filter(this.checkStatus);
      }

      return this.sortedLayers.filter(this.checkCategory).filter(this.checkStatus);
    },
    visibleLayers() {
      if (!this.searchQuery) {
        return this.filteredLayers;
      }

      return this.filteredLayers.filter(
        (layer) => layer.title.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1,
      );
    },
    paginatedData() {
      const start = (this.currentPageNumber - 1) * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.visibleLayers.slice(start, end);
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
    this.getLayers();
    this.getCategories();
    this.status = ["Gepubliceerd", "Concept"];

    this.sections = this.getSections();
  },
  methods: {
    async getLayers() {
      this.loading = true;

      const result = await fetch("/atlas/api/v1/layers/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layers");
      }

      this.layers = await result.json();
      this.loading = false;

      if (this.layers) {
        this.setLayerStatus();
      }
    },
    async saveLayer(currentValues, continueEditing = false) {
      const url = "/atlas/api/v1/layers/";

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "POST", currentValues);

        if (result.ok) {
          this.closeFormModal();

          if (continueEditing) {
            const response = await result.json();
            this.$router.push(`/layers/update/${response.id}`);
          }

          await this.getLayers();
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    async deleteLayer(layer) {
      const acknowledged = confirm("Weet je zeker dat je de laag wilt verwijderen?");
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/layers/${layer.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getLayers();
      }
    },
    async getCategories() {
      const result = await fetch("/atlas/api/v1/categories/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch categories");
      }

      const response = await result.json();

      this.categories = response.map((category) => category.title);

      return response.map((category) => {
        return { id: category.id, label: category.title };
      });
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
    setLayerStatus() {
      this.layers.forEach((layer) => {
        layer.status = layer.published ? "Gepubliceerd" : "Concept";
      });
    },
    openFormModal(modalType) {
      if (modalType === "newLayer") {
        this.newLayerData = {
          title: "",
          authenticate: false,
          metadata: { name: "", description: "", organization: "", updated: "", link: "", lineage: "", contact: "" },
        };
      }

      if (modalType === "export") {
        this.selectedItems = this.layers.filter((layer) => this.checkedRows.includes(layer.id));
      }

      this.modalType = modalType;
      this.showFormModal = true;
    },
    closeFormModal() {
      this.showFormModal = false;
      this.modalType = null;
    },
    setTableFilters(v) {
      this.selectedLayerFilters = v;
    },
    checkCategory(layer) {
      if (!this.selectedLayerFilters[this.categoryFilterProperty]) {
        return true;
      }
      return this.selectedLayerFilters[this.categoryFilterProperty].includes(layer.category?.title);
    },
    checkStatus(layer) {
      if (!this.selectedLayerFilters[this.statusFilterProperty]) {
        return true;
      }

      return this.selectedLayerFilters[this.statusFilterProperty].includes(layer.status);
    },
    sortColumn(prop) {
      if (this.sortKey !== prop) {
        this.sortKey = prop;
        this.sortAscending = true;
      } else {
        this.sortAscending = !this.sortAscending;
      }
    },
    getSortValue(sortItem) {
      if (this.sortKey === this.categoryFilterProperty) {
        return sortItem[this.sortKey] ? sortItem[this.sortKey]?.title.toLowerCase() : "";
      }

      if (this.sortKey === this.statusFilterProperty) {
        return sortItem.status;
      }

      return sortItem[this.sortKey].toLowerCase();
    },
    toggleAdvance() {
      this.advanceSettings = !this.advanceSettings;
    },
    onCheckRow(id, checkAll = false) {
      if (id === null && checkAll) {
        this.allChecked = !this.allChecked;

        if (this.allChecked) {
          this.visibleLayers.forEach((layer) => {
            this.checkedRows.push(layer.id);
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
              label: "Categorie",
              id: "category_id",
              name: "Category",
              type: "dropdown",
              required: false,
              placeholder: "categorie",
              options: this.getCategories,
            },
          ],
        },
        source: {
          label: "Bron",
          questions: [
            {
              label: "Bron",
              id: "source_id",
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

<style scoped>
.search-filter-container {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.filter-wrapper {
  display: flex;
  gap: 12px;
}

@media (max-width: 576px) {
  .search-filter-container,
  .filter-wrapper {
    flex-direction: column;
    align-items: flex-start;
  }

  .filter-wrapper {
    width: 100%;
  }
}
</style>
