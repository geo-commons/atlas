<script setup lang="ts">
import AdminListView from "@/admin/components/AdminListView.vue";
import { onMounted, Ref, ref, unref, computed } from "vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { TableFilter } from "@/admin/components/AdminListViewFilter.vue";

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
  getUniqueFields().then((result) => {
    users.value = result.usernames;
    resources.value = result.resources;
    sources.value = result.sources;
  });
});

const tableFilters = computed((): Array<TableFilter> => {
  return [
    { options: unref(users), name: "Gebruiker", key: "username", label: "" },
    { options: unref(resources), name: "Resource", key: "resource", label: "" },
    { options: unref(sources), name: "Bron", key: "source", label: "" },
  ];
});
</script>

<template>
  <AdminListView
    :loading="loading"
    singular-name="Log"
    plural-name="Logs"
    api-name="logs"
    :enable-delete="false"
    :enable-edit="false"
    :enable-create-object="false"
    :table-headers="tableHeaders"
    :table-filters="tableFilters"
    :view-base-url="'/atlas/admin/#/logs/update'"
  />
</template>
