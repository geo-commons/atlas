<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Kaarten</h1>
        <button class="button __primary __normal __full-width-mobile" type="button" @click="openFormModal">
          <AddIcon class="icon __white" />
          Nieuwe kaart
        </button>
      </div>
    </div>

    <div class="admin-content-wrapper">
      <div v-if="!loading" class="admin-search-wrapper">
        <SearchIcon class="icon" />
        <input id="maps-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek kaart" />
      </div>

      <PaginationComponent
        :items="visibleMaps"
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
              <tr v-for="map in paginatedData" :key="map.id" class="table-border">
                <td class="first-column-padding">
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
                    class="iconbutton __normal __round __alt_hover"
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
                    class="iconbutton __normal __round __alt_hover"
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
      <template #header><h3>Configureer nieuwe kaart</h3></template>
      <template #body>
        <AdminFormSections
          ref="formSections"
          :sections="sections"
          :initial-values="newMapData"
          :create-view="true"
          :form-object="'maps'"
          :object-specific-save="saveMap"
          @close="closeFormModal"
        />
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

export default {
  name: "MapList",
  components: {
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
        const result = await this.$refs.formSections.sendSaveRequest(url, "POST", currentValues);

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
    openFormModal() {
      this.newMapData = {
        title: "",
        authenticate: false,
        layers: [],
      };

      this.showFormModal = true;
    },
    closeFormModal() {
      this.showFormModal = false;
    },
    updateCurrentValues(newValues) {
      this.newMapData = newValues;
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
