<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Categorieën</h1>
        <button class="button __primary __normal" @click="openFormModal">
          <AddIcon class="icon __white" />
          Nieuwe categorie
        </button>
      </div>

      <div class="search-wrapper">
        <SearchIcon class="icon" />
        <input id="categories-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek categorie" />
      </div>
    </div>

    <div v-if="visibleCategories.length > 0" class="padding-bottom">
      <PaginationComponent
        :items="visibleCategories"
        :nr-of-records="nrOfRecords"
        @page-change="(pageNumber) => (currentPageNumber = pageNumber)"
        @records-change="(value) => (nrOfRecords = value)"
      >
        <template #default>
          <table class="category-table">
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
                <th></th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="category in paginatedData" :key="category.id" class="table-border">
                <td class="first-column-padding">
                  <router-link class="category-title-link" :to="`/categories/update/${category.id}`">
                    {{ category.title }}
                  </router-link>
                </td>
                <td>
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round"
                    aria-label="Wijzig laag"
                    content="Wijzig"
                    type="button"
                  >
                    <router-link class="category-link-btn" :to="`/categories/update/${category.id}`">
                      <EditIcon class="icon" />
                    </router-link>
                  </button>
                </td>
                <td>
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round"
                    aria-label="Verwijder categorie"
                    content="Verwijder"
                    type="button"
                    @click="deleteCategory(category)"
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
      <template #header><h3>Configureer nieuwe laag</h3> </template>
      <template #body>
        <validation-observer v-slot="{ handleSubmit }">
          <form v-if="newCategoryData" class="form-model-container" @submit.prevent="handleSubmit(saveCategory)">
            <AdminFormSections
              :sections="sections"
              :initial-values="newCategoryData"
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
  </div>
</template>

<script>
import Cookies from "js-cookie";
import PaginationComponent from "@/components/Pagination.vue";
import FormModal from "@/components/FormModal.vue";
import { ValidationObserver } from "vee-validate";
import SortableTableHeaderItem from "@/components/SortableTableHeaderItem.vue";
import { sortAlphabetically } from "@/utils/table-sort-helpers";
import TrashIcon from "../../assets/icons/trash-icon.svg";
import EditIcon from "../../assets/icons/edit-icon.svg";
import AddIcon from "../../assets/icons/add-icon.svg";
import SearchIcon from "../../assets/icons/search-icon.svg";
import AdminFormSections from "@/admin/components/AdminFormSections.vue";

export default {
  name: "CategoryList",
  components: {
    AdminFormSections,
    SortableTableHeaderItem,
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
      categories: [],
      newCategoryData: null,
      searchQuery: "",
      currentPageNumber: 1,
      nrOfRecords: 20,
      showFormModal: false,
      sortKey: "",
      sortAscending: true,
      sections: {},
    };
  },
  computed: {
    sortedCategories() {
      if (this.sortKey && this.categories) {
        return this.categories.slice(0).sort((a, b) => {
          const textA = a[this.sortKey].toLowerCase();
          const textB = b[this.sortKey].toLowerCase();
          return sortAlphabetically(textA, textB, this.sortAscending);
        });
      }

      return this.categories;
    },
    visibleCategories() {
      if (!this.searchQuery) {
        return this.sortedCategories;
      }

      return this.sortedCategories.filter(
        (category) => category.title.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1
      );
    },
    paginatedData() {
      const start = (this.currentPageNumber - 1) * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.visibleCategories.slice(start, end);
    },
  },
  created() {
    this.getCategories();

    this.sections = this.getSections();
  },
  methods: {
    async getCategories() {
      const result = await fetch("/atlas/api/v1/categories/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch categories");
      }

      this.categories = await result.json();
    },
    async saveCategory() {
      let result;

      result = await fetch(`/atlas/api/v1/categories/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify(this.newCategoryData),
      });

      // todo: think about what to do if the result is not ok.
      if (result.ok) {
        this.closeFormModal();
        await this.getCategories();
      }
    },
    async deleteCategory(category) {
      const acknowledged = confirm("Weet je zeker dat je de categorie wilt verwijderen?");
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/categories/${category.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getCategories();
      }
    },

    openFormModal() {
      this.newCategoryData = {
        title: "",
        authenticate: false,
      };

      this.showFormModal = true;
    },
    closeFormModal() {
      this.showFormModal = false;
    },
    updateCurrentValues(newValues) {
      this.newCategoryData = newValues;
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
  padding: 0 0 0 48px;
  border: 1px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
}

@media (max-width: 576px) {
  .page-title-wrapper {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-wrapper {
    width: 100%;
  }

  .top-menu-container {
    gap: 16px;
  }
}

.category-title-link {
  text-decoration: none;
  color: var(--color-black);
}

.category-title-link:hover {
  text-decoration: underline;
}

.category-link-btn {
  color: var(--color-black);
  display: flex;
}

.form-model-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.padding-bottom {
  padding-bottom: 40px;
}

.category-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-white);
}

tbody > tr:hover {
  background-color: var(--color-primary-hover);
}

.category-table thead tr th {
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
