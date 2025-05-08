<script setup lang="ts">
import AdminListView from "@/admin/components/AdminListView.vue";
import { onMounted, Ref, ref, unref } from "vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { TableFilter } from "@/admin/components/AdminListViewFilter.vue";

const logs: Ref<Array<object>> = ref([]);
const loading: Ref<boolean> = ref(true);
const sources: Ref<Array<object>> = ref([]);
const resources: Ref<Array<object>> = ref([]);
const users: Ref<Array<object>> = ref([]);

const tableHeaders: Array<TableHeader> = [
  {
    header: "Datum",
    key: "time_created",
    enableLink: true,
  },
  {
    header: "Gebruikersnaam",
    key: "username",
    enableLink: true,
  },
];

const getLogs = async (params?: URLSearchParams): Promise<{ results: Array<object>; count: number }> => {
  const url = new URL("/atlas/api/v1/logs/", window.location.origin);

  if (params) {
    url.search = params.toString();
  }

  const result = await fetch(url.toString(), {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch logs");
  }

  const items = await result.json();

  return items;
};

const getUniqueFields = async () => {
  const result = await fetch("/atlas/api/v1/logs/unique-fields/", {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch unique fields for logs");
  }

  const items = await result.json();

  const usernames = items.usernames.filter((username: string | null) => username !== null);
  const resources = items.resources.filter((resource: string | null) => resource !== null);
  const sources = items.sources.filter((source: string | null) => source !== null);

  return { usernames, resources, sources };
};

// onMounted
onMounted(() => {
  Promise.all([getLogs(), getUniqueFields()]).then((result) => {
    logs.value = result[0].results;
    users.value = result[1].usernames;
    resources.value = result[1].resources;
    sources.value = result[1].sources;
    loading.value = false;
  });
});

const getTableFilters = (): Array<TableFilter> => {
  return [
    { options: unref(users), name: "Gebruiker", key: "username", label: "" },
    { options: unref(resources), name: "Resource", key: "resource", label: "" },
    { options: unref(sources), name: "Bron", key: "source", label: "" },
  ];
};
</script>

<template>
  <AdminListView
    :loading="loading"
    singular-name="Log"
    plural-name="Logs"
    api-name="logs"
    :enable-sort="false"
    :enable-delete="false"
    :enable-edit="false"
    :enable-create-object="false"
    :get-objects="getLogs"
    :table-headers="tableHeaders"
    :get-table-filters="getTableFilters"
    :view-base-url="'/atlas/admin/#/logs/update'"
  />
</template>
