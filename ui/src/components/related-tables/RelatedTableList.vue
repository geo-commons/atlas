<template>
  <ExpandButton :title="relatedTable.title" :is-open="true" class="feature" @show-content="onShowContentChange">
    <template #default>
      <div>
        <!--        <span v-if="error">{{ error }}</span>-->
        <!--        <span v-if="loading">Bezig met laden...</span>-->
        <!--        <span v-if="!loading && !error && displayProperties.length === 0">Geen weergave beschikbaar.</span>-->
        <div v-if="!loading && relatedTableData.length > 0">
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
                  <td v-for="(property, index) in tableHeaders" :key="index" class="related-cell">
                    <RichValue :data-key="property" :data-value="item[property]" />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <Paginator
            v-if="showPaginator"
            :template="{
              default: 'PrevPageLink PageLinks NextPageLink',
            }"
            :current-page-report-template="'({currentPage} van {totalPages})'"
            :rows="pageState.rows"
            :total-records="totalItems"
            :first="pageState.page * pageState.rows - 1 + pageState.rows"
            :rows-per-page-options="[10, 20, 30, 50, 100]"
            @page="updatePageState"
          ></Paginator>
        </div>
        <div v-else>
          <p class="tw-mt-2 tw-mb-0">Geen resultaten gevonden</p>
        </div>
      </div>
    </template>
  </ExpandButton>
</template>

<script setup lang="ts">
import { ICqlFilterEntry, IRelatedTable, SourceType } from "@/types/related-table";
import ExpandButton from "@/components/ExpandButton.vue";
import { computed, onMounted, ref, watch } from "vue";
import nunjucks from "nunjucks";
import RichValue from "@/components/RichValue.vue";
import fetchDot from "fetch-dot";

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
const relatedTableData = ref<Record<string, string>[]>([]);
// const tableHeaders = ref<string[]>([]);
const loading = ref<boolean>(false);
const pageState = ref({
  page: 0,
  first: 10,
  rows: 10,
});
const totalItems = ref<number>(0);

const onShowContentChange = (isOpen: boolean) => {
  // Emit event or handle content visibility change
};

const showPaginator = computed(() => {
  // Don't show paginator if pagination is not enabled
  if (!relatedTable.page_param || !relatedTable.items_per_page_param || !relatedTable.total_items_page_property) {
    return false;
  }

  return totalItems.value !== null && totalItems.value > pageState.value.rows;
});

const tableHeaders = computed(() => {
  if (relatedTable.list_display_properties && relatedTable.list_display_properties.length > 0) {
    return relatedTable.list_display_properties;
  }

  const firstItem = relatedTableData.value[0];
  return firstItem ? Object.keys(firstItem) : [];
});

const getRestData = async (table: IRelatedTable) => {
  const fullUrl = `${table.source.url}${table.list_endpoint}`;
  const renderedUrl = nunjucks.renderString(fullUrl, fieldMappingValues.value);
  const url = new URL(renderedUrl);

  // If pagination is enabled, add pagination parameters to the request URL
  if (table.page_param && table.items_per_page_param && table.total_items_page_property) {
    url.searchParams.set(table.page_param, (pageState.value.page + 1).toString());
    url.searchParams.set(table.items_per_page_param, pageState.value.rows.toString());
  }

  try {
    const response = await fetch(url.toString());

    if (!response.ok) {
      // TODO: introduce proper error handling
      console.error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    relatedTableData.value = table.list_property ? fetchDot(table.list_property, data) : data;

    // If pagination is enabled set total items
    if (table.total_items_page_property) {
      totalItems.value = fetchDot(table.total_items_page_property, data);
    }

    totalItems.value = data.total;
    loading.value = false;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
  loading.value = false;
};

const getOwsData = async (table: IRelatedTable) => {
  const params = new URLSearchParams([
    ["service", "WFS"],
    ["version", "1.0.0"],
    ["request", "GetFeature"],
    ["typename", table.layer_name],
    ["outputFormat", "application/json"],
    ["maxFeatures", pageState.value.rows.toString()],
    ["startIndex", (pageState.value.rows * pageState.value.page).toString()],
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
      totalItems.value = data.numberMatched;

      relatedTableData.value = properties;
      if (relatedTableData.value.length > 0) {
        // retrieve one item to determine table headers,
        // TODO: in the end also check if display_properties is set
        const firstItem = relatedTableData.value[0];
        tableHeaders.value = Object.keys(firstItem);
      }
    } catch (e) {
      console.error(e);
    }
  }

  // loading = false;
  loading.value = false;
};

const getRelatedTableData = (table: IRelatedTable) => {
  if (table.source_type === SourceType.REST) {
    getRestData(table);
  }

  if (table.source_type === SourceType.WMTS || table.source_type === SourceType.OWS) {
    getOwsData(table);
  }
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

const handleTableUpdate = () => {
  loading.value = true;
  getFieldMappingValue(fieldMapping, layerFeature || tableFeature);

  getRelatedTableData(relatedTable);
};

const updatePageState = (event: any) => {
  pageState.value = {
    ...pageState.value,
    page: event.page,
    first: event.first,
    rows: event.rows,
  };
  // Re-fetch data with new pagination parameters
  handleTableUpdate();
};

onMounted(() => {
  handleTableUpdate();
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
