<script setup lang="ts">
import AdminListView from "@/admin/components/AdminListView.vue";
import { onMounted, Ref, ref, unref } from "vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { TableFilter } from "@/admin/components/AdminListViewFilter.vue";
import { useGlobalStore } from "@/stores";
import { getAllObjects } from "@/utils/api-helpers";

const loading: Ref<boolean> = ref(true);
const users: Ref<Array<object>> = ref([]);
const groups: Ref<Array<object>> = ref([]);
const store = useGlobalStore();

const tableHeaders: Array<TableHeader> = [
  {
    header: "Gebruikersnaam",
    key: "username",
    enableLink: true,
  },
  {
    header: "E-mailadres",
    key: "email",
    enableLink: false,
  },
  {
    header: "Volledige naam",
    key: "name",
    enableLink: false,
  },
  {
    header: "Groepen",
    key: "atlas_groups",
    enableLink: false,
    isArrayWithKey: "name",
  },
  {
    header: "Datum toegetreden",
    key: "date_joined",
    enableLink: false,
  },
  {
    header: "Laatste aanmelding",
    key: "last_login",
    enableLink: false,
  },
  {
    header: "Actief",
    key: "is_active",
    enableLink: false,
  },
  {
    header: "Beheerder",
    key: "is_superuser",
    enableLink: false,
  },
];

const getUsers = async (params?: URLSearchParams): Promise<{ results: Array<object>; count: number }> => {
  const url = new URL("/atlas/api/v1/users/", window.location.origin);

  if (params) {
    url.search = params.toString();
  }

  const result = await fetch(url.toString(), {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch users");
  }

  const items = await result.json();

  return items;
};

const getGroups = async (): Promise<Array<object>> => {
  const url = getAllObjects("/atlas/api/v1/groups/");

  const result = await fetch(url, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch groups");
  }

  const response = await result.json();

  const groups = response.results.map((group: any) => {
    return { id: group.id, label: group.name };
  });

  return groups;
};

// onMounted
onMounted(() => {
  Promise.all([getUsers(), getGroups()]).then((result) => {
    users.value = result[0].results;
    groups.value = result[1];
    loading.value = false;
  });
});

const getTableFilters = (): Array<TableFilter> => {
  return [{ options: unref(groups), name: "Groepen", key: "atlas_groups", label: "label", dataKey: "id" }];
};
</script>

<template>
  <AdminListView
    :loading="loading"
    singular-name="Gebruiker"
    plural-name="Gebruikers"
    api-name="users"
    :enable-sort="false"
    :enable-create-object="false"
    :block-delete="[store?.user?.id]"
    :get-objects="getUsers"
    :table-headers="tableHeaders"
    :get-table-filters="getTableFilters"
  />
</template>
