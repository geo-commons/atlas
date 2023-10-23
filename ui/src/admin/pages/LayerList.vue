<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Kaartlagen</h1>
        <button class="button __primary __normal" @click="openFormModal">
          <AddIcon class="icon __white" />
          Nieuwe laag
        </button>
      </div>

      <div class="search-filter-container">
        <div class="search-wrapper">
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
    </div>

    <FormModal v-show="showFormModal" @close="closeFormModal">
      <template #header><h3>Configureer nieuwe laag</h3> </template>
      <template #body>
        <validation-observer v-slot="{ handleSubmit }">
          <form v-if="newLayerData" class="form-model-container" @submit.prevent="handleSubmit(saveLayer)">
            <AdminFormSections
              :sections="sections"
              :initial-values="newLayerData"
              :create-view="true"
              @update="(newValues) => updateCurrentValues(newValues)"
            />
            <div class="flexer">
              <button class="button __tertiary" @click="closeFormModal">Annuleer</button>
              <button class="button __primary" type="submit">Opslaan</button>
            </div>
          </form>
        </validation-observer>
      </template>
    </FormModal>

    <div v-if="visibleLayers.length > 0">
      <PaginationComponent
        :items="visibleLayers"
        :nr-of-records="nrOfRecords"
        @page-change="(pageNumber) => (currentPageNumber = pageNumber)"
        @records-change="(value) => (nrOfRecords = value)"
      >
        <template #default>
          <table class="layer-table">
            <thead>
              <tr class="table-border">
                <th class="first-column-padding">
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
                <td class="first-column-padding">
                  <router-link class="layer-title-link" :to="`/layers/update/${layer.id}`">
                    {{ layer.title }}
                  </router-link>
                </td>
                <td>
                  {{ layer.category?.title }}
                </td>
                <td>
                  {{ layer.status }}
                </td>
                <td>
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round"
                    aria-label="Wijzig laag"
                    content="Wijzig"
                    type="button"
                  >
                    <router-link class="layer-link-btn" :to="`/layers/update/${layer.id}`">
                      <EditIcon class="icon" />
                    </router-link>
                  </button>
                </td>
                <td>
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round"
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
  </div>
</template>

<script>
import Cookies from "js-cookie";
import PaginationComponent from "@/components/Pagination.vue";
import FormModal from "@/components/FormModal.vue";
import { ValidationObserver } from "vee-validate";
import FilterSelect from "@/components/FilterSelect.vue";
import SortableTableHeaderItem from "@/components/SortableTableHeaderItem.vue";
import { sortAlphabetically } from "@/utils/table-sort-helpers";
import TrashIcon from "../../assets/icons/trash-icon.svg";
import EditIcon from "../../assets/icons/edit-icon.svg";
import AddIcon from "../../assets/icons/add-icon.svg";
import SearchIcon from "../../assets/icons/search-icon.svg";
import AdminFormSections from "@/admin/components/AdminFormSections.vue";

export default {
  name: "LayerList",
  components: {
    AdminFormSections,
    SortableTableHeaderItem,
    FilterSelect,
    FormModal,
    PaginationComponent,
    ValidationObserver,
    TrashIcon,
    EditIcon,
    AddIcon,
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
        (layer) => layer.title.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1
      );
    },
    paginatedData() {
      const start = (this.currentPageNumber - 1) * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.visibleLayers.slice(start, end);
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
      const result = await fetch("/atlas/api/v1/layers/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layers");
      }

      this.layers = await result.json();

      if (this.layers) {
        this.setLayerStatus();
      }
    },
    async saveLayer() {
      let result;

      result = await fetch(`/atlas/api/v1/layers/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify(this.newLayerData),
      });

      // todo: think about what to do if the result is not ok.
      if (result.ok) {
        this.closeFormModal();
        await this.getLayers();
      }
    },
    async deleteLayer(layer) {
      const acknowledged = confirm("Weet je zeker dat je de laag wil verwijderen?");
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
    openFormModal() {
      this.newLayerData = {
        title: "",
        authenticate: false,
        metadata: { name: "", description: "", organization: "", updated: "", link: "" },
      };

      this.showFormModal = true;
    },
    closeFormModal() {
      this.showFormModal = false;
    },
    updateCurrentValues(newValues) {
      this.newLayerData = newValues;
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
              required: true,
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
.top-menu-container {
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.page-title-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.search-filter-container {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.search-wrapper {
  width: clamp(300px, 35%, 400px);
  height: 48px;
  position: relative;
}

.search-wrapper svg {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 16px;
  margin: auto 0;
  pointer-events: none;
}

.search-wrapper input {
  width: 100%;
  height: 100%;
  border: 1px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
  padding: 0 0 0 48px;
}

.filter-wrapper {
  display: flex;
  gap: 12px;
}

@media (max-width: 576px) {
  .page-title-wrapper,
  .search-filter-container,
  .filter-wrapper {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-wrapper,
  .filter-wrapper {
    width: 100%;
  }

  .search-filter-container {
    gap: 8px;
  }

  .top-menu-container {
    gap: 16px;
  }
}

.layer-title-link {
  text-decoration: none;
  color: var(--color-black);
}

.layer-title-link:hover {
  text-decoration: underline;
}

.layer-link-btn {
  color: var(--color-black);
  display: flex;
}

.form-model-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.layer-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-white);
}

tbody > tr:hover {
  background-color: var(--color-grey-40);
}

.layer-table thead tr th {
  text-align: left;
  font-weight: var(--font-weight-normal);
  color: var(--color-text-grey);
  padding-top: 10px;
  padding-bottom: 10px;
}

tr.table-border:not(:last-child) > td,
th {
  border-bottom: 1px solid var(--color-grey-60);
}

tr > td:not(:nth-last-child(-n + 2)) {
  padding-right: 8px;
}

.first-column-padding {
  padding-left: 12px;
}
</style>
