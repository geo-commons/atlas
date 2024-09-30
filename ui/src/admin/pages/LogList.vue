<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper no-padding">
        <h1>Logs</h1>
      </div>
    </div>

    <div class="admin-content-wrapper">
      <div class="search-filter-container">
        <div v-show="!loading" class="admin-search-wrapper">
          <SearchIcon class="icon" />
          <input id="users-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek gebruiker" />
        </div>

        <div class="filter-wrapper">
          <FilterSelect
            v-if="users.length > 0"
            :filter-options="users"
            :field-filters="selectedLogsFilters"
            :filter-property="userFilterProperty"
            :filter-property-display-name="'Gebruiker'"
            :track-by="''"
            :label="''"
            :style-type="'admin'"
            @onFilterChange="(v) => setTableFilters(v)"
          />
          <FilterSelect
            v-if="resources.length > 0"
            :filter-options="resources"
            :field-filters="selectedLogsFilters"
            :filter-property="resourceFilterProperty"
            :filter-property-display-name="'Resource'"
            :track-by="''"
            :label="''"
            :style-type="'admin'"
            @onFilterChange="(v) => setTableFilters(v)"
          />
          <FilterSelect
            v-if="sources.length > 0"
            :filter-options="sources"
            :field-filters="selectedLogsFilters"
            :filter-property="sourceFilterProperty"
            :filter-property-display-name="'Bron'"
            :track-by="''"
            :label="''"
            :style-type="'admin'"
            @onFilterChange="(v) => setTableFilters(v)"
          />
        </div>
      </div>

      <PaginationComponent
        :items="visibleLogs"
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
                    :header-text="'Datum'"
                    :property="'time_created'"
                    :sort-key="sortKey"
                    :sort-ascending="sortAscending"
                    @sort="(column) => sortColumn(column)"
                  />
                </th>
                <th class="first-column-padding">
                  <SortableTableHeaderItem
                    :header-text="'Gebruikersnaam'"
                    :property="'username'"
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
              <tr v-for="log in paginatedData" :key="log.id" class="table-border">
                <td class="first-column-padding">
                  <router-link class="admin-title-link" :to="`/logs/${log.id}`">
                    {{ formatDateValue(log.time_created) }}
                  </router-link>
                </td>
                <td class="first-column-padding">
                  <router-link class="admin-title-link" :to="`/logs/${log.id}`">
                    {{ log.username }}
                  </router-link>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    aria-label="Bekijk log"
                    content="Bekijk"
                    type="button"
                    @click="$router.push(`/logs/${log.id}`)"
                  >
                    <ViewIcon class="icon" />
                  </button>
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    aria-label="Verwijder log"
                    content="Verwijder"
                    type="button"
                    @click="deleteLog(log)"
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
import SortableTableHeaderItem from "@/components/SortableTableHeaderItem.vue";
import ViewIcon from "@/assets/icons/view-icon.svg";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import { sortAlphabetically } from "@/utils/table-sort-helpers";
import PaginationComponent from "@/components/Pagination.vue";
import SearchIcon from "@/assets/icons/search-icon.svg";
import { formatDateValue } from "../../utils/date-formatter";
import FilterSelect from "@/components/FilterSelect.vue";

export default {
  name: "LogList",
  components: {
    FilterSelect,
    SearchIcon,
    PaginationComponent,
    TrashIcon,
    ViewIcon,
    SortableTableHeaderItem,
  },
  data() {
    return {
      logs: [],
      newLogData: {},
      searchQuery: "",
      currentPageNumber: 1,
      nrOfRecords: 20,
      sortAscending: true,
      sortKey: "",
      users: [],
      sources: [],
      resources: [],
      loading: false,
      checkedRows: [],
      selectedLogsFilters: {},
      userFilterProperty: "user",
      sourceFilterProperty: "source",
      resourceFilterProperty: "resource",
    };
  },
  computed: {
    sortedLogs() {
      if (this.sortKey && this.logs) {
        return this.logs.slice(0).sort((a, b) => {
          const textA = a[this.sortKey].toLowerCase();
          const textB = b[this.sortKey].toLowerCase();
          return sortAlphabetically(textA, textB, this.sortAscending);
        });
      }

      return this.logs;
    },
    filteredLogs() {
      const filters = [];

      if (this.selectedLogsFilters[this.userFilterProperty]) {
        filters.push(this.checkUser);
      }

      if (this.selectedLogsFilters[this.sourceFilterProperty]) {
        filters.push(this.checkSource);
      }

      if (this.selectedLogsFilters[this.resourceFilterProperty]) {
        filters.push(this.checkResource);
      }

      if (filters.length === 0) {
        return this.sortedLogs;
      }

      return this.sortedLogs.filter((log) => {
        return filters.every((filter) => filter.call(this, log));
      });
    },
    visibleLogs() {
      if (!this.searchQuery) {
        return this.filteredLogs;
      }

      return this.filteredLogs.filter(
        (log) => log.username.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1,
      );
    },
    paginatedData() {
      const start = (this.currentPageNumber - 1) * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.visibleLogs.slice(start, end);
    },
  },
  created() {
    this.getLogs();
    this.getUsers();
  },
  methods: {
    formatDateValue,
    async getLogs() {
      this.loading = true;
      const result = await fetch("/atlas/api/v1/logs/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch logs");
      }

      this.logs = await result.json();

      this.sources = await this.getLogSources();
      this.resources = await this.getResources();
      this.users = await this.getUsers();

      this.loading = false;
    },
    async getLogSources() {
      return Array.from(new Set(this.logs.map((log) => log.source).filter((source) => source !== null)));
    },
    async getResources() {
      return Array.from(new Set(this.logs.map((log) => log.resource).filter((resource) => resource !== null)));
    },
    async getUsers() {
      return Array.from(new Set(this.logs.map((log) => log.username).filter((username) => username !== null)));
    },
    async deleteLog(log) {
      const acknowledged = confirm("Weet je zeker dat je de log wilt verwijderen?");
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/logs/${log.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getLogs();
      }
    },
    setTableFilters(v) {
      this.selectedLogsFilters = v;
    },
    checkUser(filteredUser) {
      if (!this.selectedLogsFilters[this.userFilterProperty]) {
        return true;
      }

      return this.selectedLogsFilters[this.userFilterProperty].some((user) => user === filteredUser.username);
    },
    checkSource(filteredSource) {
      if (!this.selectedLogsFilters[this.sourceFilterProperty]) {
        return true;
      }

      return this.selectedLogsFilters[this.sourceFilterProperty].some((source) => source === filteredSource.source);
    },
    checkResource(filteredResource) {
      if (!this.selectedLogsFilters[this.resourceFilterProperty]) {
        return true;
      }

      return this.selectedLogsFilters[this.resourceFilterProperty].some(
        (resource) => resource === filteredResource.resource,
      );
    },
    sortColumn(prop) {
      if (this.sortKey !== prop) {
        this.sortKey = prop;
        this.sortAscending = true;
      } else {
        this.sortAscending = !this.sortAscending;
      }
    },
  },
};
</script>

<style>
.search-filter-container {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.no-padding {
  padding-bottom: 0 !important;
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
