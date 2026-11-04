<script setup lang="ts">
import AdminListView from "@/admin/components/AdminListView.vue";
import { TableFilter } from "@/admin/components/AdminListViewFilter.vue";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";
import { apiFetch } from "@/utils/api-helpers";
import { computed, onMounted, ref } from "vue";

interface IFilterOption {
  id: string | number;
  label: string;
}

interface IAuditLogFilterData {
  actors: IFilterOption[];
  models: IFilterOption[];
  actions: IFilterOption[];
}

const actors = ref<IFilterOption[]>([]);
const models = ref<IFilterOption[]>([]);
const actions = ref<IFilterOption[]>([]);

const tableHeaders: TableHeader[] = [
  { header: "Datum", key: "date", enableLink: false },
  { header: "Model", key: "model", enableLink: false },
  { header: "Object", key: "object", enableLink: true, linkUrlKey: "admin_url" },
  { header: "Actie", key: "action", enableLink: false, tagActionIdKey: "action_id" },
  { header: "Uitgevoerd door", key: "actor", enableLink: false },
  { header: "Details", key: "summary", enableLink: false },
];

const tableFilters = computed<TableFilter[]>(() => [
  { options: models.value, name: "Model", key: "model", label: "label", dataKey: "id" },
  { options: actions.value, name: "Actie", key: "action", label: "label", dataKey: "id" },
  { options: actors.value, name: "Uitgevoerd door", key: "actor", label: "label", dataKey: "id" },
]);

const getUniqueFields = async (): Promise<void> => {
  const response = await apiFetch("/atlas/api/v1/audit-logs/unique-fields/");
  if (!response.ok) {
    console.error("Could not fetch audit log filter values");
    return;
  }

  const data: IAuditLogFilterData = await response.json();
  actors.value = data.actors;
  models.value = data.models;
  actions.value = data.actions;
};

onMounted(getUniqueFields);
</script>

<template>
  <AdminListView
    :loading="false"
    singular-name="Beheerlog"
    plural-name="Beheerlogs"
    api-name="audit-logs"
    :enable-create-object="false"
    :enable-delete="false"
    :enable-edit="false"
    :table-headers="tableHeaders"
    :table-filters="tableFilters"
  />
</template>
