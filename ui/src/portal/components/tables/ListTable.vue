<template>
  <div v-if="!loading && tableData.length > 0">
    <DataTable :value="tableData" size="small" scrollable responsive-layout="scroll" class="tw-w-full">
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
      >
        <template #body="{ data }">
          <RichValue :data-key="col" :data-value="fetchDot(col, data)" />
        </template>
      </Column>

      <template #empty>
        <span class="tw-text-gray-400">Geen items</span>
      </template>
    </DataTable>
    <div class="tw-flex tw-items-start tw-mt-2">
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
</template>

<script setup lang="ts">
import { IRelatedTable, ICqlFilterEntry, SourceType } from "@/types/related-table";
import nunjucks from "nunjucks";
import fetchDot from "fetch-dot";
import { ref, watch, computed } from "vue";
import { pickTemplateValues } from "@/components/related-tables/utils";
import { formatFriendlyFieldLabel } from "@/utils/string-helpers";

const { relatedTable, fieldMapping } = defineProps<{
  relatedTable: IRelatedTable;
  fieldMapping: Record<string, string>;
}>();

const emit = defineEmits<{
  (e: "select-related-table-object", type: { relatedTableId: number; item: any; relatedTableTitle: string }): void;
}>();

const tableData = ref<Record<string, string>[]>([]);
const loading = ref<boolean>(true);
const pageState = ref({
  page: 0,
  first: 10,
  rows: 10,
});
const totalItems = ref<number>(0);
const errorMessage = ref<string | null>(null);

const tableHeaders = computed(() => {
  if (relatedTable.list_display_properties && relatedTable.list_display_properties.length > 0) {
    return relatedTable.list_display_properties;
  }

  const firstItem = tableData.value[0];
  return firstItem ? Object.keys(firstItem) : [];
});

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

const onSelectRelatedData = (item: any) => {
  // Emit event or handle related data selection
  emit("select-related-table-object", { relatedTableId: relatedTable.id, item, relatedTableTitle: relatedTable.title });
};

const getRestData = async (table: IRelatedTable) => {
  const fullUrl = `${table.source.url}${table.list_endpoint}`;
  const renderedUrl = nunjucks.renderString(fullUrl, fieldMapping);
  const url = new URL(renderedUrl);

  // If pagination is enabled, add pagination parameters to the request URL
  if (table.page_param && table.items_per_page_param && table.total_items_page_property) {
    url.searchParams.set(table.page_param, (pageState.value.page + table.start_page_index).toString());
    url.searchParams.set(table.items_per_page_param, pageState.value.rows.toString());
  }

  try {
    const response = await fetch(url.toString(), {
      method: table.method,
      body: table.method === "POST" ? nunjucks.renderString(table.request_body, fieldMapping) : null,
    });

    if (!response.ok) {
      if (response.status === 404) {
        tableData.value = [];
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

    const templateUsedValues = pickTemplateValues(fullUrl, fieldMapping);

    tableData.value = arrayResult.map((item) => ({
      ...templateUsedValues,
      ...item,
    }));

    // If pagination is enabled set total items
    if (table.total_items_page_property) {
      totalItems.value = fetchDot(table.total_items_page_property, data);
    }
  } catch (error) {
    errorMessage.value = (error as Error).message;
    tableData.value = [];
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
      if (fieldMapping[filterObject.key]) {
        const replaceValue = nunjucks.renderString(filterObject.cql_filter, fieldMapping);
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

      tableData.value = properties;
    } catch (e) {
      errorMessage.value = (e as Error).message;
      tableData.value = [];
    }
  }

  loading.value = false;
};

const getTableData = (table: IRelatedTable) => {
  if (table.source_type === SourceType.REST) {
    getRestData(table);
  }

  if (table.source_type === SourceType.WMTS || table.source_type === SourceType.OWS) {
    getOwsData(table);
  }
};

const fetchTableData = () => {
  loading.value = true;
  errorMessage.value = null;

  getTableData(relatedTable);
};

const updatePageState = (event: any) => {
  pageState.value = {
    ...pageState.value,
    page: event.page,
    first: event.first,
    rows: event.rows,
  };

  // Re-fetch data with new pagination parameters
  fetchTableData();
};

watch(
  () => [relatedTable, fieldMapping],
  () => {
    if (relatedTable) {
      fetchTableData();
    }
  },
  { immediate: true, deep: true },
);
</script>
