<script setup lang="ts">
import EditIcon from "@/assets/icons/edit-icon.svg";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import ViewIcon from "@/assets/icons/view-icon.svg";
import { useRouter } from "vue-router";
import AdminListViewTableHeader, { TableHeaderRef } from "@/admin/components/AdminListViewTableHeader.vue";
import { Ref, ref, watch } from "vue";
import { PaginationRef } from "@/admin/components/AdminListViewPaginator.vue";
import AdminListViewTableValue from "@/admin/components/AdminListViewTableValue.vue";

// Properties
export type TableHeader = {
  header: string;
  key: string;
  overrideKeyForFilter?: string;
  enableLink: boolean;
  isArrayWithKey?: string;
  mapValues?: { [key: string]: any };
};

type AdminListViewProps = {
  items: Array<any>;
  apiName: string;
  tableHeaders: Array<TableHeader>;
  sort: TableHeaderRef;
  pagination: PaginationRef;
  enableActions: boolean;
  enableDelete: boolean;
  enableEdit: boolean;
  viewBaseUrl?: string;
  blockDelete: Array<number>;
};

const props = withDefaults(defineProps<AdminListViewProps>(), { enableDelete: true });

// Emits
const emit = defineEmits<{
  (e: "update-selected-items", selectedItems: Array<{ id: number; title: string }>): void;
  (e: "update-list-sort", key: string): void;
  (e: "delete-row", row: any): void;
}>();

// Initiation
const router = useRouter();

// Table logic
const selectedRows: Ref<Array<{ id: number; title: string }>> = ref([]);
const selectedRowsCheckedValue: Ref<Record<number, boolean>> = ref({});

const selectAllRows: Ref<boolean> = ref(false);

const onSelectAllRows = (value: boolean) => {
  if (!value) {
    selectedRows.value = [];
    selectedRowsCheckedValue.value = {};
  } else {
    props.items.forEach((item) => {
      selectedRows.value.push({ id: item.id, title: item.title });
      selectedRowsCheckedValue.value[item.id] = true;
    });
  }

  emit("update-selected-items", selectedRows.value);
};

const onSelectRow = (row: any) => {
  if (selectedRows.value.some((selectedRow) => selectedRow.id === row.id)) {
    selectAllRows.value = false;
    selectedRows.value = selectedRows.value.filter((selectedRow) => selectedRow.id !== row.id);

    delete selectedRowsCheckedValue.value[row.id];
  } else {
    selectedRows.value.push({ id: row.id, title: row.title ? row.title : row.label ? row.label : "" });
    selectedRowsCheckedValue.value[row.id] = true;
  }

  emit("update-selected-items", selectedRows.value);
};

watch(
  () => props.items,
  () => {
    if (selectAllRows.value) {
      selectedRows.value = [];
      selectedRowsCheckedValue.value = {};
      onSelectAllRows(true);
    }
  },
);

const getValue = (obj: object, keyString: string, isArrayWithKey?: string, mapValues?: { [key: string]: any }): any => {
  const value = keyString.split(".").reduce((acc: any, key: string) => acc && acc[key], obj);

  if (Array.isArray(value) && isArrayWithKey) {
    return value.map((item: any) => item[isArrayWithKey]).join(", ");
  }

  if (mapValues && mapValues[value]) {
    return mapValues[value];
  }

  return value;
};

const blockDelete = (obj: any): any => {
  if (!props.blockDelete.length) {
    return false;
  }

  return props.blockDelete.includes(obj.id);
};

const resetSelection = () => {
  selectAllRows.value = false;
  selectedRows.value = [];
  selectedRowsCheckedValue.value = {};
  emit("update-selected-items", selectedRows.value);
};

defineExpose({ resetSelection });
</script>

<template>
  <div class="card !tw-text-md tw-overflow-x-scroll">
    <table class="admin-table tw-rounded-md">
      <thead>
        <tr class="table-border">
          <th v-if="items.length && props.enableActions" class="tw-w-8 tw-p-2">
            <Checkbox v-model="selectAllRows" :binary="true" @update:model-value="onSelectAllRows" />
          </th>
          <th v-for="header in props.tableHeaders" :key="header.key" class="first:tw-pl-4">
            <AdminListViewTableHeader
              :header="header"
              :sort="props.sort"
              @update-list-sort="(key: string) => $emit('update-list-sort', key)"
            />
          </th>
          <th v-if="props.enableEdit"></th>
          <th v-if="props.viewBaseUrl"></th>
          <th v-if="props.enableDelete"></th>
        </tr>
      </thead>
      <tbody v-if="items.length">
        <tr v-for="row in items" :key="row.id" class="table-border">
          <td v-if="props.enableActions" class="tw-w-8 tw-p-2">
            <Checkbox
              :model-value="selectedRowsCheckedValue[row.id]"
              :binary="true"
              @update:model-value="onSelectRow(row)"
            />
          </td>

          <td v-for="header in tableHeaders" :key="header.key" class="first:tw-pl-4">
            <p v-if="!header.enableLink">
              <AdminListViewTableValue :value="getValue(row, header.key, header.isArrayWithKey, header.mapValues)" />
            </p>
            <router-link
              v-else
              class="admin-title-link"
              type="button"
              :aria-label="`${row[header.key]} configureren`"
              :to="`/${props.apiName}/update/${row.id}`"
            >
              <AdminListViewTableValue :value="getValue(row, header.key, header.isArrayWithKey, header.mapValues)" />
            </router-link>
          </td>
          <td v-if="props.enableEdit" class="btn-col">
            <button
              v-tippy="{ placement: 'bottom' }"
              class="iconbutton __normal __round __admin_hover tw-my-1"
              :aria-label="`${row[props.tableHeaders[0].header]} configureren`"
              content="Wijzig"
              type="button"
              @click="router.push(`/${props.apiName}/update/${row.id}`)"
            >
              <EditIcon class="icon" />
            </button>
          </td>
          <td v-if="props.viewBaseUrl" class="btn-col">
            <a
              v-tippy="{ placement: 'bottom' }"
              class="iconbutton __normal __round __admin_hover tw-my-1 tw-bg-white"
              :aria-label="`${row[props.tableHeaders[0].header]} bekijken`"
              content="Bekijk"
              type="button"
              target="_blank"
              :href="`${props.viewBaseUrl}/${row.slug ? row.slug : row.id}`"
            >
              <ViewIcon class="icon" />
            </a>
          </td>
          <td v-if="enableDelete" class="btn-col">
            <button
              v-tippy="{ placement: 'bottom' }"
              :disabled="blockDelete(row)"
              class="iconbutton __normal __round __admin_hover tw-my-1"
              aria-label="Verwijder"
              type="button"
              content="Verwijder"
              @click="emit('delete-row', row)"
            >
              <TrashIcon class="icon" />
            </button>
          </td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr class="table-border">
          <td class="tw-pl-4 tw-py-4">Geen resultaten gevonden</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
