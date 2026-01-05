<template>
  <div class="tw-p-2">
    <div class="tw-ml-2">
      <ButtonGroup>
        <Button variant="outlined" size="small" label="Terug" icon="pi pi-arrow-left" @click="back" />
        <Button
          variant="outlined"
          size="small"
          label="Naar begin"
          icon="pi pi-home"
          @click="closeRelatedTableDetails"
        />
      </ButtonGroup>
    </div>

    <div class="tw-px-2">
      <p class="tw-font-bold tw-mb-2">{{ relatedTable?.title }}</p>
      <table-list>
        <table>
          <tbody>
            <tr v-for="(value, index) in tableItems" :key="index">
              <td>
                {{ formatRawString(getResolvedKey(value) || "") }}
              </td>
              <td>
                <RichValue :data-key="getResolvedKey(value)" :data-value="fetchDot(value, relatedTableData)" />
              </td>
            </tr>
          </tbody>
        </table>
      </table-list>
    </div>

    <div v-if="feature !== null && relatedTables.length > 0" class="">
      <div v-for="(table, key) in relatedTables" :key="key" class="tw-pt-4">
        <RelatedTableList
          :table-feature="feature"
          :related-table="table.to_table"
          :field-mapping="table.field_mapping"
          @select-related-table-object="onSelectRelatedTableObject"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import ArrowLeftIcon from "@/assets/icons/arrow-left-icon.svg";
import { ICqlFilterEntry, IRelatedTable, SourceType } from "@/types/related-table";
import nunjucks from "nunjucks";
import TableList from "@/components/TableList.vue";
import { formatRawString, getResolvedKey } from "@/utils/string-helpers";
import RichValue from "@/components/RichValue.vue";
import RelatedTableList from "@/components/related-tables/RelatedTableList.vue";
import fetchDot from "fetch-dot";

const { selectedRelatedTableAttributes } = defineProps<{
  selectedRelatedTableAttributes: { relatedTableId: number; item: any };
}>();

const emit = defineEmits<{
  (e: "back"): void;
  (e: "close-related-table-details"): void;
  (e: "select-related-table-object", type: { relatedTable: IRelatedTable; item: any }): void;
}>();

const relatedTableData = ref<Record<string, string>>({});
const relatedTable = ref<IRelatedTable>();
const relatedTables = ref<IRelatedTable[]>([]);
const feature = ref<Record<string, string> | null>(null);

const tableItems = computed(() => {
  if (relatedTable.value?.detail_display_properties && relatedTable.value?.detail_display_properties.length > 0) {
    return relatedTable.value.detail_display_properties;
  }

  const firstItem = relatedTableData.value;
  return firstItem ? Object.keys(firstItem) : [];
});

const back = () => {
  emit("back");
};

const closeRelatedTableDetails = () => {
  emit("close-related-table-details");
};

const onSelectRelatedTableObject = (attr: any) => {
  emit("select-related-table-object", attr);
};

const getRestData = async (table: IRelatedTable, item: any) => {
  const fullUrl = `${table.source.url}${table.detail_endpoint}`;
  const renderedUrl = nunjucks.renderString(fullUrl, item);

  try {
    const response = await fetch(renderedUrl);

    if (!response.ok) {
      // TODO: introduce proper error handling
      console.error(`HTTP error! status: ${response.status}`);
      return [];
    }

    const data = await response.json();
    return table.detail_property ? fetchDot(table.detail_property, data) : data;
  } catch (error) {
    // TODO: introduce proper error handling
    console.error("Error fetching data:", error);
    return [];
  }
};

const getOwsData = async (table: IRelatedTable, item: any) => {
  const params = new URLSearchParams([
    ["service", "WFS"],
    ["version", "1.0.0"],
    ["request", "GetFeature"],
    ["typename", table.layer_name],
    ["outputFormat", "application/json"],
    ["maxFeatures", "5000"],
  ]);

  if (table.detail_cql_filters.length > 0) {
    let replacedFilters: string[] = [];
    table.detail_cql_filters.forEach((filterObject: ICqlFilterEntry) => {
      const filterValue = item[filterObject.key];
      if (filterValue) {
        const replaceValue = nunjucks.renderString(filterObject.cql_filter, item);
        replacedFilters.push(replaceValue);
      }
    });
    const joinedFilters = replacedFilters.join(" AND ");

    params.set("cql_filter", joinedFilters);

    try {
      const url = new URL(table.source.url);
      url.search = params.toString();

      const result = await fetch(url.toString());
      if (!result.ok) {
        console.error(`HTTP error! status: ${result.status}`);
        return;
      }

      const data = await result.json();
      const properties = data.features[0]?.properties || {};

      return properties;
    } catch (e) {
      console.error(e);
    }
  }

  // loading = false;
  return [];
};

const getRelatedTableData = (table: IRelatedTable, item: any) => {
  if (table.source_type === SourceType.REST) {
    return getRestData(table, item);
  }

  if (table.source_type === SourceType.WMTS || table.source_type === SourceType.OWS) {
    return getOwsData(table, item);
  }

  return [];
};

const getRelatedTable = async (tableId: number) => {
  const response = await fetch(`/atlas/api/v1/tables-v2/${tableId}/`);
  const result = await response.json();

  if (!response.ok) {
    console.error("gaat iets fout bij het ophalen van gerelateerde tabel");
    return;
  }
  relatedTable.value = result;
  relatedTables.value = relatedTable.value?.related_tables || [];
};

const handleSelectedRelatedTableAttributes = async () => {
  feature.value = selectedRelatedTableAttributes.item;

  await getRelatedTable(selectedRelatedTableAttributes.relatedTableId);

  if (!relatedTable.value) {
    // TODO: introduce proper error handling
    console.error("Related table not found");
    return;
  }

  relatedTableData.value = await getRelatedTableData(relatedTable.value, selectedRelatedTableAttributes.item);
};

onMounted(async () => {
  await handleSelectedRelatedTableAttributes();
});

onUnmounted(() => {
  console.log("Component unmounted");
});

watch(
  () => selectedRelatedTableAttributes,
  async () => {
    await handleSelectedRelatedTableAttributes();
  },
  { deep: true },
);
</script>

<!--TODO: styling nalopen of verplaatsen, misschien tailwind? -->
<style scoped>
.back-button {
  display: flex;
  align-items: center;
  font-size: var(--font-size-small);
  gap: 4px;
}

.table-wrapper td:first-child {
  width: 40%;
  color: var(--color-text-grey);
}

.table-wrapper td:last-child {
  padding-left: 20px;
}

.table-wrapper th,
.table-wrapper td {
  padding: 4px;
  vertical-align: top;
}
</style>
