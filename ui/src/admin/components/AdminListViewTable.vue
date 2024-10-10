<script setup lang="ts">
import EditIcon from "@/assets/icons/edit-icon.svg";
import TrashIcon from "@/assets/icons/trash-icon.svg";
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
};

const props = withDefaults(defineProps<AdminListViewProps>(), {});

// Emits
const emit = defineEmits<{
  (e: "update-list-sort", key: string): void;
  (e: "toggle-element-in-checked-row", value: boolean, id: number, title: string): void;
  (e: "remove-all-elements-from-selected-items"): void;
  (e: "toggle-is-all-selected", value: boolean): void;
  (e: "delete-row", row: any): void;
  (e: "toggle-clear-selected"): void;
}>();

// Initiation
const router = useRouter();

// Table logic
const checkedRows: Ref<Array<object>> = ref([]);
const checkedAllRows: Ref<boolean> = ref(false);

const checkAllRows = (value: boolean) => {
  for (const row of props.items) {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-expect-error
    checkedRows.value[row.id] = value;

    emit("toggle-element-in-checked-row", value, row.id, row.title ? row.title : row.label ? row.label : "");
  }
};

watch(
  () => props.items,
  (value) => {
    if (checkedAllRows.value) {
      checkAllRows(true);
    }
  },
);

watch(
  () => checkedAllRows.value,
  (newValue, oldValue) => {
    if (newValue) {
      emit("toggle-is-all-selected", true);
    }

    if (!newValue && oldValue) {
      checkedRows.value = [];
      emit("remove-all-elements-from-selected-items");
      emit("toggle-is-all-selected", false);
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
</script>

<template>
  <div class="card !tw-text-md tw-overflow-x-scroll">
    <table class="admin-table tw-rounded-md">
      <thead>
        <tr class="table-border">
          <th class="tw-min-w-[32px] tw-max-w-[32px] tw-overflow-x-hidden">
            <Checkbox
              v-model="checkedAllRows"
              :binary="true"
              @update:modelValue="(value: boolean) => checkAllRows(value)"
            />
          </th>
          <th v-for="header in props.tableHeaders" :key="header.key" class="first:tw-pl-4">
            <AdminListViewTableHeader
              :header="header"
              :sort="props.sort"
              @update-list-sort="(key: string) => $emit('update-list-sort', key)"
            />
          </th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody v-if="items.length">
        <tr v-for="row in items" :key="row.id" class="table-border">
          <td class="">
            <Checkbox
              v-model="checkedRows[row.id]"
              :binary="true"
              @update:modelValue="
                (value: boolean) =>
                  emit(
                    'toggle-element-in-checked-row',
                    value,
                    row.id,
                    row.title ? row.title : row.label ? row.label : '',
                  )
              "
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
          <td class="btn-col">
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
          <td class="btn-col">
            <button
              v-tippy="{ placement: 'bottom' }"
              class="iconbutton __normal __round __admin_hover tw-my-1"
              aria-label="Verwijder"
              content="Verwijder"
              type="button"
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
