<template>
  <div>
    <div v-if="!loading && relatedTableData.length > 0">
      <DataTable
        :value="relatedTableData"
        size="small"
        scrollable
        responsive-layout="scroll"
        class="tw-w-full !tw-text-black"
        removable-sort
      >
        <Column v-if="!relatedTable.disable_detail_view" header="" style="width: 3rem">
          <template #body="{ data }">
            <Button
              v-tippy
              content="Bekijk details"
              icon="pi pi-arrow-right"
              text
              rounded
              size="small"
              aria-label="Bekijk details"
              @click="onSelectRelatedData(data)"
            />
          </template>
        </Column>

        <Column
          v-for="col in tableHeaders"
          :key="col"
          :field="col"
          :header="formatFriendlyFieldLabel(col, relatedTable.friendly_fields)"
          sortable
        >
          <template #body="{ data }">
            <RichValue :data-key="col" :data-value="fetchDot(col, data)" position="left" />
          </template>
        </Column>

        <template #empty>
          <span class="tw-text-gray-400">Geen items</span>
        </template>
      </DataTable>
      <div class="tw-flex tw-items-start">
        <Paginator
          v-if="showPaginator"
          :template="{
            default: 'PrevPageLink CurrentPageReport NextPageLink RowsPerPageDropdown',
          }"
          class="tw-mb-4 tw-mt-2"
          :rows="pageState.rows"
          :total-records="totalItems"
          current-page-report-template="Pagina {currentPage} van {totalPages}"
          :first="pageState.page * pageState.rows - 1 + pageState.rows"
          :rows-per-page-options="[10, 20, 30, 50, 100]"
          :pt="{
            root: '!tw-p-0',
          }"
          @page="updatePageState"
        ></Paginator>
      </div>
    </div>
    <div v-else-if="loading" class="tw-flex tw-justify-center tw-items-center tw-mt-2 tw-mb-2">
      <ProgressSpinner stroke-width="2" style="width: 48px; height: 48px" />
    </div>
    <div v-else-if="errorMessage" class="tw-mt-2 tw-mb-2 tw-mb-0">
      <Message severity="error">{{ errorMessage }}</Message>
    </div>
    <div v-else class="tw-mt-2 tw-mb-0 tw-mb-2">
      <Message severity="secondary">Geen resultaten gevonden</Message>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ICqlFilterEntry, IRelatedTable, SourceType } from "@/types/related-table";
import { IPosition } from "@/types/map";
import { computed, onMounted, ref, watch } from "vue";
import nunjucks from "nunjucks";
import RichValue from "@/components/RichValue.vue";
import fetchDot from "fetch-dot";
import { formatFriendlyFieldLabel } from "@/utils/string-helpers";
import { pickTemplateValues } from "@/components/related-tables/utils";

const { layerFeature, tableFeature, fieldMapping, relatedTable, relatedTableTitle, position } = defineProps<{
  layerFeature?: Record<string, string>;
  tableFeature?: Record<string, string>;
  fieldMapping: Record<string, string>;
  relatedTable: IRelatedTable;
  relatedTableTitle: string;
  position: IPosition;
}>();

const emit = defineEmits<{
  (e: "select-related-table-object", type: { relatedTableId: number; item: any; relatedTableTitle: string }): void;
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
const errorMessage = ref<string | null>(null);

const showPaginator = computed(() => {
  // Don't show paginator if pagination is not enabled for REST source type
  if (
    relatedTable.source_type === SourceType.REST &&
    (!relatedTable.page_param || !relatedTable.items_per_page_param || !relatedTable.total_items_page_property)
  ) {
    return false;
  }

  return totalItems.value !== null;
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
    url.searchParams.set(table.page_param, (pageState.value.page + table.start_page_index).toString());
    url.searchParams.set(table.items_per_page_param, pageState.value.rows.toString());
  }

  try {
    const response = await fetch(url.toString(), {
      method: table.method,
      body: table.method === "POST" ? nunjucks.renderString(table.request_body, fieldMappingValues.value) : null,
    });

    if (!response.ok) {
      if (response.status === 404) {
        relatedTableData.value = [];
        totalItems.value = 0;
        errorMessage.value = null;
        loading.value = false;
        return;
      }

      let error = `Er is een onbekende fout opgetreden bij het ophalen van de gegevens. Probeer het later opnieuw. HTTP Status: ${response.status}`;

      try {
        const errorResponse = await response.json();

        if (table.list_error_property) {
          error = fetchDot(table.list_error_property, errorResponse) ?? error;
        }
      } catch {
        // Response body was not JSON, ignore and use default message
      }

      throw new Error(error);
    }

    const data = await response.json();
    const result = table.list_property ? fetchDot(table.list_property, data) : data;

    // Ensure the result is always an array for easier handling in the template
    const arrayResult = Array.isArray(result) ? result : result != null ? [result] : [];

    const templateUsedValues = pickTemplateValues(fullUrl, fieldMappingValues.value);

    relatedTableData.value = arrayResult.map((item) => ({
      ...templateUsedValues,
      ...item,
    }));

    // If pagination is enabled set total items
    if (table.total_items_page_property) {
      totalItems.value = fetchDot(table.total_items_page_property, data);
    }
  } catch (error) {
    errorMessage.value = (error as Error).message;
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
        const error = `Er is een fout opgetreden bij het ophalen van de gegevens. Probeer het later opnieuw. HTTP Status: ${result.status}`;
        throw new Error(error);
      }

      const data = await result.json();
      const properties = data.features.map((feature: any) => feature.properties);
      totalItems.value = data.numberMatched;

      relatedTableData.value = properties;
    } catch (e) {
      errorMessage.value = (e as Error).message;
    }
  }

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
      mapping[value] = feature.properties ? fetchDot(key, feature.properties) : fetchDot(key, feature);
    }
  }

  fieldMappingValues.value = {
    ...mapping,
    x: position.marker ? position.marker[0].toFixed(3) : "",
    y: position.marker ? position.marker[1].toFixed(3) : "",
  };
};

const handleTableUpdate = () => {
  loading.value = true;
  errorMessage.value = null;
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
  () => {
    handleTableUpdate();
  },
  { deep: true },
);

const onSelectRelatedData = (item: any) => {
  // Emit event or handle related data selection
  emit("select-related-table-object", { relatedTableId: relatedTable.id, item, relatedTableTitle: relatedTableTitle });
};
</script>
