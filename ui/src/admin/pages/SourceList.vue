<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Bronnen</h1>
        <button class="button __primary __normal __full-width-mobile" @click="openFormModal">
          <AddIcon class="icon __white" />
          Nieuwe bron
        </button>
      </div>
    </div>

    <div class="admin-content-wrapper">
      <div v-if="!loading" class="admin-search-wrapper">
        <SearchIcon class="icon" />
        <input id="source-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek bron" />
      </div>

      <PaginationComponent
        :items="visibleSources"
        :nr-of-records="nrOfRecords"
        :loading="loading"
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
              <tr v-for="source in paginatedData" :key="source.id" class="table-border">
                <td class="first-column-padding">
                  <router-link class="admin-title-link" :to="`/sources/update/${source.id}`">
                    {{ source.title }}
                  </router-link>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __alt_hover"
                    aria-label="Wijzig bron"
                    content="Wijzig"
                    type="button"
                    @click="$router.push(`/sources/update/${source.id}`)"
                  >
                    <EditIcon class="icon" />
                  </button>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __alt_hover"
                    aria-label="Verwijder bron"
                    content="Verwijder"
                    type="button"
                    @click="deleteSource(source)"
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
      <template #header><h3>Configureer nieuwe bron</h3></template>
      <template #body>
        <AdminFormSections
          ref="formSections"
          :sections="sections"
          :initial-values="newSourceData"
          :create-view="true"
          :form-object="'sources'"
          :object-specific-save="saveSource"
          @close="closeFormModal"
        />
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

export default {
  name: "SourceList",
  components: {
    SearchIcon,
    PaginationComponent,
    TrashIcon,
    EditIcon,
    SortableTableHeaderItem,
    AdminFormSections,
    FormModal,
    AddIcon,
  },
  data() {
    return {
      sources: [],
      showFormModal: false,
      newSourceData: {},
      searchQuery: "",
      sections: {},
      currentPageNumber: 1,
      nrOfRecords: 20,
      sortAscending: true,
      sortKey: "",
      loading: false,
    };
  },
  computed: {
    sortedSources() {
      if (this.sortKey && this.sources) {
        return this.sources.slice(0).sort((a, b) => {
          const textA = a[this.sortKey].toLowerCase();
          const textB = b[this.sortKey].toLowerCase();
          return sortAlphabetically(textA, textB, this.sortAscending);
        });
      }

      return this.sources;
    },
    visibleSources() {
      if (!this.searchQuery) {
        return this.sortedSources;
      }

      return this.sortedSources.filter(
        (source) => source.title.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1
      );
    },
    paginatedData() {
      const start = (this.currentPageNumber - 1) * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.visibleSources.slice(start, end);
    },
  },
  created() {
    this.getSources();
    this.sections = this.getSections();
  },
  methods: {
    async getSources() {
      this.loading = true;
      const result = await fetch("/atlas/api/v1/sources/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch sources");
      }

      this.sources = await result.json();
      this.loading = false;
    },
    async deleteSource(source) {
      const acknowledged = confirm("Weet je zeker dat je de bron wilt verwijderen?");
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/sources/${source.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getSources();
      }
    },
    async saveSource(currentValues, continueEditing = false) {
      const url = "/atlas/api/v1/sources/";

      try {
        const result = await this.$refs.formSections.sendSaveRequest(url, "POST", currentValues);

        if (result.ok) {
          this.closeFormModal();

          if (continueEditing) {
            const response = await result.json();
            this.$router.push(`/sources/update/${response.id}`);
          }

          await this.getSources();
        }
      } catch (e) {
        console.error("An unexpected error occurred:", e);
      }
    },
    openFormModal() {
      this.newSourceData = {
        title: "",
        url: "",
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
              maxLength: 50,
              infoText: "Een uniek kort kenmerk voor de bron in Atlas.",
            },
            {
              label: "URL",
              id: "url",
              name: "Url",
              type: "url",
              required: true,
            },
          ],
        },
      };
    },
  },
};
</script>
