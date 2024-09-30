<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper">
        <h1>Gebruikers</h1>
      </div>
    </div>

    <div class="admin-content-wrapper">
      <div class="search-filter-container">
        <div v-show="!loading" class="admin-search-wrapper">
          <SearchIcon class="icon" />
          <input id="users-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek gebruiker" />
        </div>

        <FilterSelect
          v-if="groups.length > 0"
          :filter-options="groups"
          :field-filters="selectedUserFilters"
          :filter-property="groupFilterProperty"
          :filter-property-display-name="'Groep'"
          :filter-on-id="true"
          :option-label="'name'"
          :label="'name'"
          @onFilterChange="(v) => setTableFilters(v)"
        />
      </div>

      <PaginationComponent
        :items="visibleUsers"
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
                    :header-text="'Gebruikersnaam'"
                    :property="'username'"
                    :sort-key="sortKey"
                    :sort-ascending="sortAscending"
                    @sort="(column) => sortColumn(column)"
                  />
                </th>
                <th>
                  <SortableTableHeaderItem
                    :header-text="'E-mailadres'"
                    :property="'email'"
                    :sort-key="sortKey"
                    :sort-ascending="sortAscending"
                    @sort="(column) => sortColumn(column)"
                  />
                </th>
                <th>
                  <SortableTableHeaderItem
                    :header-text="'Volledige naam'"
                    :property="'name'"
                    :sort-key="sortKey"
                    :sort-ascending="sortAscending"
                    @sort="(column) => sortColumn(column)"
                  />
                </th>
                <th>Groepen</th>
                <th>
                  <SortableTableHeaderItem
                    :header-text="'Datum toegetreden'"
                    :property="'date_joined'"
                    :sort-key="sortKey"
                    :sort-ascending="sortAscending"
                    @sort="(column) => sortColumn(column)"
                  />
                </th>
                <th>
                  <SortableTableHeaderItem
                    :header-text="'Laatste aanmelding'"
                    :property="'last_login'"
                    :sort-key="sortKey"
                    :sort-ascending="sortAscending"
                    @sort="(column) => sortColumn(column)"
                  />
                </th>
                <th>Actief</th>
                <th>Beheerder</th>
                <th class="btn-col"></th>
                <th class="btn-col"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in paginatedData" :key="user.id" class="table-border">
                <td class="first-column-padding">
                  <router-link
                    class="admin-title-link"
                    type="button"
                    :aria-label="`${user.username} configureren`"
                    :to="`/users/update/${user.id}`"
                  >
                    {{ user.username }}
                  </router-link>
                </td>
                <td>{{ user.email }}</td>
                <td>{{ user.name }}</td>
                <td>
                  <p class="user-group-wrapper">{{ getUserGroup(user) }}</p>
                </td>
                <td>{{ formatDateValue(user.date_joined) }}</td>
                <td>{{ formatDateValue(user.last_login) }}</td>
                <td>
                  <StatusIndicatorComponent :status="user.is_active" />
                </td>
                <td>
                  <StatusIndicatorComponent :status="user.is_staff && user.is_superuser" />
                </td>
                <td class="btn-col">
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    :aria-label="`${user.username} configureren`"
                    content="Wijzig"
                    type="button"
                    @click="$router.push(`/users/update/${user.id}`)"
                  >
                    <EditIcon class="icon" />
                  </button>
                </td>
                <td class="btn-col">
                  <button
                    v-if="user.id !== currentUser.id"
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __round __admin_hover"
                    aria-label="Verwijder gebruiker"
                    content="Verwijder"
                    type="button"
                    @click="deleteUser(user)"
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
import SearchIcon from "@/assets/icons/search-icon.svg";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import EditIcon from "@/assets/icons/edit-icon.svg";
import SortableTableHeaderItem from "@/components/SortableTableHeaderItem.vue";
import PaginationComponent from "@/components/Pagination.vue";
import { sortAlphabetically } from "@/utils/table-sort-helpers";
import StatusIndicatorComponent from "@/admin/components/StatusIndicator.vue";
import Cookies from "js-cookie";
import FilterSelect from "@/components/FilterSelect.vue";
import { formatDateValue } from "@/utils/date-formatter";
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";

export default {
  name: "UserList",
  components: {
    FilterSelect,
    StatusIndicatorComponent,
    TrashIcon,
    SearchIcon,
    EditIcon,
    PaginationComponent,
    SortableTableHeaderItem,
  },
  data() {
    return {
      users: [],
      searchQuery: "",
      currentPageNumber: 1,
      nrOfRecords: 20,
      sortKey: "",
      sortAscending: true,
      loading: false,
      groups: [],
      groupFilterProperty: "group",
      selectedUserFilters: {},
    };
  },
  computed: {
    ...mapState(useGlobalStore, {
      currentUser: "user",
    }),
    sortedUsers() {
      if (this.sortKey && this.users) {
        return this.users.slice(0).sort((a, b) => {
          const textA = a[this.sortKey]?.toLowerCase();
          const textB = b[this.sortKey]?.toLowerCase();
          return sortAlphabetically(textA, textB, this.sortAscending);
        });
      }

      return this.users;
    },
    filteredUsers() {
      if (Object.keys(this.selectedUserFilters).length > 0) {
        return this.sortedUsers.filter(this.checkGroup);
      }

      return this.sortedUsers;
    },
    visibleUsers() {
      if (!this.searchQuery) {
        return this.filteredUsers;
      }

      return this.filteredUsers.filter(
        (user) => user.username.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1,
      );
    },
    paginatedData() {
      const start = (this.currentPageNumber - 1) * this.nrOfRecords;
      const end = start + this.nrOfRecords;
      return this.visibleUsers.slice(start, end);
    },
  },
  created() {
    this.getUsers();
    this.getGroups();
  },
  methods: {
    formatDateValue,
    async getUsers() {
      this.loading = true;

      const result = await fetch("/atlas/api/v1/users/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch users");
      }

      this.users = await result.json();
      this.loading = false;

      return result;
    },
    async deleteUser(user) {
      const acknowledged = confirm("Weet je zeker dat je de gebruiker wilt verwijderen?");
      if (!acknowledged) {
        return;
      }

      const result = await fetch(`/atlas/api/v1/users/${user.id}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (result.ok) {
        this.getUsers();
      }
    },
    async getGroups() {
      const result = await fetch("/atlas/api/v1/groups/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch groups");
      }

      this.groups = await result.json();
      return result;
    },
    getUserGroup(user) {
      const groupNames = [];

      user.atlas_groups.forEach((groupId) => {
        groupNames.push(this.getGroupNameById(groupId));
      });

      return groupNames.join(",\r\n");
    },
    getGroupNameById(groupId) {
      return this.groups.find((group) => group.id === groupId)?.name;
    },
    setTableFilters(v) {
      this.selectedUserFilters = v;
    },
    checkGroup(user) {
      if (!this.selectedUserFilters[this.groupFilterProperty]) {
        return true;
      }
      return this.selectedUserFilters[this.groupFilterProperty].some((group) => user.atlas_groups?.includes(group.id));
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

<style scoped>
.search-filter-container {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

p.user-group-wrapper {
  white-space: pre;
  margin: 0;
}
</style>
