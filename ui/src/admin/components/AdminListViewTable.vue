<script setup lang="ts">
import EditIcon from "@/assets/icons/edit-icon.svg";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import { useRouter } from "vue-router";
import AdminListViewTableHeader, { TableHeaderRef } from "@/admin/components/AdminListViewTableHeader.vue";

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
};

const props = withDefaults(defineProps<AdminListViewProps>(), {});

// Emits
const emit = defineEmits<{
  (e: "update-list-sort", key: string): void;
}>();

// Initiation
const router = useRouter();

// Table logic
const deleteObject = (object: any) => {
  console.log("delete object");
};

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
  <div class="card">
    <table class="admin-table tw-rounded-md">
      <thead>
        <tr class="table-border">
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
      <tbody>
        <tr v-for="layer in items" :key="layer.id" class="table-border">
          <td v-for="header in tableHeaders" :key="header.key" class="first:tw-pl-4">
            <p v-if="!header.enableLink">{{ getValue(layer, header.key, header.isArrayWithKey, header.mapValues) }}</p>
            <router-link
              v-else
              class="admin-title-link"
              type="button"
              :aria-label="`${layer[header.key]} configureren`"
              :to="`/${props.apiName}/update/${layer.id}`"
            >
              {{ getValue(layer, header.key, header.isArrayWithKey, header.mapValues) }}
            </router-link>
          </td>
          <td class="btn-col">
            <button
              v-tippy="{ placement: 'bottom' }"
              class="iconbutton __normal __round __admin_hover tw-my-1"
              :aria-label="`${layer[props.tableHeaders[0].header]} configureren`"
              content="Wijzig"
              type="button"
              @click="router.push(`/${props.apiName}/update/${layer.id}`)"
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
              @click="deleteObject(layer)"
            >
              <TrashIcon class="icon" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
