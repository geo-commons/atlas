<template>
  <ExpandButton :title="relatedTable.title" :is-open="true" @show-content="onShowContentChange">
    <template #default>
      <div>
        <!--        <span v-if="error">{{ error }}</span>-->
        <!--        <span v-if="loading">Bezig met laden...</span>-->
        <!--        <span v-if="!loading && !error && displayProperties.length === 0">Geen weergave beschikbaar.</span>-->
        <div>
          <div class="table-wrapper">
            <table class="related-table">
              <thead>
                <tr>
                  <th></th>
                  <th v-for="(property, i) in tableHeaders" :key="i" class="related-header">
                    {{ property }}
                    <!--                    <StackSortableTableHeaderItem-->
                    <!--                      :header-text="headerText(property)"-->
                    <!--                      :property="displayProperties[i]"-->
                    <!--                      :sort-stack="sortStack"-->
                    <!--                      @sort="(column, ascending) => sortColumn(column, ascending)"-->
                    <!--                    />-->
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, i) in relatedTableData" :key="i">
                  <td>
                    <button @click="onSelectRelatedData(item)">bekijk</button>
                  </td>
                  <td v-for="(value, key, index) in item" :key="index" class="related-cell">
                    <RichValue :data-key="key" :data-value="value" />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </template>
  </ExpandButton>
</template>

<script setup lang="ts">
import { ICqlFilterEntry, IRelatedTable, SourceType } from "@/types/related-table";
import ExpandButton from "@/components/ExpandButton.vue";
import { onMounted, ref, watch } from "vue";
import nunjucks from "nunjucks";
import RichValue from "@/components/RichValue.vue";

const { layerFeature, tableFeature, fieldMapping, relatedTable } = defineProps<{
  layerFeature?: Record<string, string>;
  tableFeature?: Record<string, string>;
  fieldMapping: Record<string, string>;
  relatedTable: IRelatedTable;
}>();

const emit = defineEmits<{
  (e: "select-related-table-object", type: { relatedTableId: number; item: any }): void;
}>();

const fieldMappingValues = ref<Record<string, string>>({});
const relatedTableData = ref<Record<string, string>[]>([{}]);
const tableHeaders = ref<string[]>([]);

const onShowContentChange = (isOpen: boolean) => {
  // Emit event or handle content visibility change
};

const getRestData = async (table: IRelatedTable) => {
  const fullUrl = `${table.source.url}${table.list_endpoint}`;
  const renderedUrl = nunjucks.renderString(fullUrl, fieldMappingValues.value);

  try {
    const response = await fetch(renderedUrl);

    if (!response.ok) {
      console.error(`HTTP error! status: ${response.status}`);
      return [];
    }

    const data = await response.json();
    // todo: results moet hier misschien nog vervangen worden door het juiste key word dat gebruikt gaat worden als 'response key'

    return data.results;
  } catch (error) {
    console.error("Error fetching data:", error);
    return [];
  }
};

const getOwsData = async (table: IRelatedTable) => {
  const params = new URLSearchParams([
    ["service", "WFS"],
    ["version", "1.0.0"],
    ["request", "GetFeature"],
    ["typename", table.layer_name],
    ["outputFormat", "application/json"],
    ["maxFeatures", "5000"],
  ]);

  if (table.list_cql_filters.length > 0) {
    let replacedFilters: string[] = [];
    table.list_cql_filters.forEach((filterObject: ICqlFilterEntry) => {
      if (fieldMappingValues.value[filterObject.key]) {
        const replaceValue = nunjucks.renderString(filterObject.cql_filter, fieldMappingValues.value);
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
      const properties = data.features.map((feature: any) => feature.properties);

      return properties;
    } catch (e) {
      console.error(e);
    }
  }

  // loading = false;
  return [];
};

const getRelatedTableData = (table: IRelatedTable) => {
  if (table.source_type === SourceType.REST) {
    return getRestData(table);
  }

  if (table.source_type === SourceType.WMTS || table.source_type === SourceType.OWS) {
    return getOwsData(table);
  }

  return [];
};

const getFieldMappingValue = (fieldMapping: Record<string, string>, feature: any) => {
  const mapping: Record<string, string> = {};
  if (fieldMapping) {
    for (const [key, value] of Object.entries(fieldMapping)) {
      mapping[value] = feature.properties ? feature.properties[key] : feature[key];
    }
  }
  fieldMappingValues.value = mapping;
};

const handleTableUpdate = async () => {
  getFieldMappingValue(fieldMapping, layerFeature || tableFeature);

  relatedTableData.value = await getRelatedTableData(relatedTable);

  // todo: wat als er geen data is?
  if (relatedTableData.value.length > 0) {
    // retrieve one item to determine table headers,
    // todo: in the end also check if display_properties is set
    const firstItem = relatedTableData.value[0];
    tableHeaders.value = Object.keys(firstItem);
  }
};

onMounted(async () => {
  await handleTableUpdate();
});

watch(
  () => relatedTable,
  async () => {
    await handleTableUpdate();
  },
  { deep: true },
);

const onSelectRelatedData = (item: any) => {
  // Emit event or handle related data selection
  emit("select-related-table-object", { relatedTableId: relatedTable.id, item });
};
</script>

<style scoped>
.table-wrapper {
  word-wrap: break-word;
  overflow: auto;
  flex: 1 1 auto;
}

.related-table {
  font-size: var(--font-size-small);
  overflow-x: auto;
  border-collapse: collapse;
  width: 100%;
}

.related-cell {
  padding: 4px;
  text-align: left;
  height: 30px;
  border-bottom: 1px solid var(--color-grey-60);
}

.related-table tbody tr:hover {
  background-color: var(--color-grey-40);
}

.related-header {
  font-weight: var(--font-weight-normal);
  color: var(--color-text-grey);
  padding: 8px 4px;
  border-bottom: 1px solid var(--color-grey-60);
  text-align: left;
}
</style>
