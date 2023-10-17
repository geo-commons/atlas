<template>
  <div class="container">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Kaartlagen</h1>
        <button class="button __primary __normal" @click="openFormModal">
          <add-icon />
          Nieuwe laag
        </button>
      </div>

      <div class="search-filter-container">
        <div class="search-wrapper">
          <svg
            width="18px"
            height="18px"
            viewBox="0 0 18 18"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
          >
            <g id="Admin" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
              <g id="Kaart---Lagen" transform="translate(-45.000000, -183.000000)" fill="#000000" fill-rule="nonzero">
                <g id="search_black_24dp" transform="translate(42.000000, 180.000000)">
                  <path
                    id="Shape"
                    d="M15.5,14 L14.71,14 L14.43,13.73 C15.41,12.59 16,11.11 16,9.5 C16,5.91 13.09,3 9.5,3 C5.91,3 3,5.91 3,9.5 C3,13.09 5.91,16 9.5,16 C11.11,16 12.59,15.41 13.73,14.43 L14,14.71 L14,15.5 L19,20.49 L20.49,19 L15.5,14 Z M9.5,14 C7.01,14 5,11.99 5,9.5 C5,7.01 7.01,5 9.5,5 C11.99,5 14,7.01 14,9.5 C14,11.99 11.99,14 9.5,14 Z"
                  ></path>
                </g>
              </g>
            </g>
          </svg>
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
            <div>
              <validation-provider v-slot="{ errors }" name="Titel">
                <label for="title">Titel</label>
                <input id="title" v-model="newLayerData.title" type="text" required />
                <span>{{ errors[0] }}</span>
              </validation-provider>
            </div>
            <div>
              <validation-provider v-slot="{ errors }" name="Titel">
                <label for="title">Laagnaam</label>
                <input id="title" v-model="newLayerData.layer_name" type="text" required />
                <span>{{ errors[0] }}</span>
              </validation-provider>
            </div>

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
                    aria-label="Verwijder laag"
                    content="Verwijder"
                    type="button"
                    @click="deleteLayer(layer)"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      height="24px"
                      viewBox="0 0 24 24"
                      width="24px"
                      fill="#000000"
                    >
                      <path d="M0 0h24v24H0V0z" fill="none" />
                      <path
                        d="M16 9v10H8V9h8m-1.5-6h-5l-1 1H5v2h14V4h-3.5l-1-1zM18 7H6v12c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7z"
                      />
                    </svg>
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
import AddIcon from "../../icons/AddIcon.vue";
import Cookies from "js-cookie";
import PaginationComponent from "@/components/Pagination.vue";
import FormModal from "@/components/FormModal.vue";
import { ValidationObserver, ValidationProvider } from "vee-validate";
import FilterSelect from "@/components/FilterSelect.vue";
import SortableTableHeaderItem from "@/components/SortableTableHeaderItem.vue";
import { sortAlphabetically } from "@/utils/table-sort-helpers";

export default {
  name: "LayerList",
  components: {
    SortableTableHeaderItem,
    FilterSelect,
    FormModal,
    PaginationComponent,
    AddIcon,
    ValidationObserver,
    ValidationProvider,
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

      if (result.ok) {
        this.$router.push(`/layers`);
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

      let resultJson = await result.json();
      this.categories = resultJson.map((category) => category.title);
    },
    setLayerStatus() {
      this.layers.forEach((layer) => {
        layer.status = layer.published ? "Gepubliceerd" : "Concept";
      });
    },
    openFormModal() {
      this.newLayerData = {
        title: "",
        url: "",
        authenticate: false,
      };

      this.showFormModal = true;
    },
    closeFormModal() {
      this.showFormModal = false;
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
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
}

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
  border: 1px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
  background: var(--color-white);
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
  height: 48px;
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

.button {
  max-width: 300px;
}

.layer-title-link {
  text-decoration: none;
  color: var(--color-black);
}
.layer-title-link:hover {
  text-decoration: underline;
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

tr > td:not(:last-child) {
  padding-right: 8px;
}

.first-column-padding {
  padding-left: 12px;
}
</style>
