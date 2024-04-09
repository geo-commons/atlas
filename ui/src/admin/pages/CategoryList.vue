<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Categorieën</h1>
        <div class="top-menu-button-container">
          <router-link
            :to="{
              name: 'sort',
              params: { parentRoute: 'categories' },
            }"
            class="button __secondary_admin __normal"
            type="button"
            aria-label="Ga naar sortering pagina"
            ><SortIcon class="icon" />Sortering</router-link
          >
          <button class="button __primary_admin __normal" type="button" @click="openFormModal">
            <AddIcon class="icon __white" />
            Nieuwe categorie
          </button>
        </div>
      </div>
    </div>

    <div class="admin-content-wrapper">
      <div v-if="!loading" class="admin-search-wrapper">
        <SearchIcon class="icon" />
        <input id="categories-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek categorie" />
      </div>

      <PaginationComponent
        :items="visibleCategories"
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
                  <router-link
                    class="admin-title-link"
                    type="button"
                    :aria-label="`${category.title} configureren`"
                    :to="`/categories/update/${category.id}`"
                  >
                    {{ category.title }}
                  </router-link>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    :aria-label="`${category.title} configureren`"
                    content="Wijzig"
                    type="button"
                    @click="$router.push(`/categories/update/${category.id}`)"
                  >
                    <EditIcon class="icon" />
                  </button>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
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

    <FormModal v-if="showFormModal" :toggle-modal="showFormModal" @close="closeFormModal">
      <template #header><h3>Configureer nieuwe categorie</h3></template>
      <template #body>
        <AdminFormSections
          ref="formSections"
          :sections="sections"
          :initial-values="newCategoryData"
          :create-view="true"
          :form-object="'categories'"
          :object-specific-save="saveCategory"
          @close="closeFormModal"
        />
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
import SortIcon from "../../assets/icons/sort-icon.svg";

export default {
  name: "CategoryList",
  components: {
    SortIcon,
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
      categories: [],
      newCategoryData: null,
      searchQuery: "",
      currentPageNumber: 1,
      nrOfRecords: 20,
      showFormModal: false,
      sortKey: "",
      sortAscending: true,
      sections: {},
      loading: false,
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
        (category) => category.title.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1,
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
      this.loading = true;

      const result = await fetch("/atlas/api/v1/categories/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch categories");
      }

      this.categories = await result.json();

      this.loading = false;
    },
    async saveCategory(currentValues, continueEditing = false) {
      const url = "/atlas/api/v1/categories/";

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "POST", currentValues);

        if (result.ok) {
          this.closeFormModal();

          if (continueEditing) {
            const response = await result.json();
            this.$router.push(`/categories/update/${response.id}`);
          }

          await this.getCategories();
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
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
              infoText: "Een uniek kort kenmerk voor de categorie in Atlas.",
            },
          ],
        },
      };
    },
  },
};
</script>
