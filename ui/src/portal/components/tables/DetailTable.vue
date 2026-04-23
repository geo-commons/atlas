<template>
  <h3 class="tw-mt-0 tw-mb-2">{{ selectedRelatedTableTitle }}</h3>
  <div v-if="feature">
    <div class="tw-flex tw-flex-col tw-gap-2">
      <div v-for="(value, index) in tableItems" :key="index" class="tw-grid tw-grid-cols-3">
        <div class="tw-col-span-1 tw-font-bold header">
          {{ formatFriendlyFieldLabel(value, selectedRelatedTable?.friendly_fields) }}
        </div>
        <div class="tw-col-span-2">
          <RichValue :data-key="getResolvedKey(value)" :data-value="fetchDot(value, feature)" />
        </div>
      </div>
      <div v-for="property in Object.keys(templateFields)" :key="property" class="tw-grid tw-grid-cols-3">
        <div class="tw-col-span-1 tw-font-bold header">
          {{ formatRawString(property) }}
        </div>
        <div class="tw-col-span-2">
          <MarkdownTemplate :source="templateFields[property]" :data="feature" />
        </div>
      </div>
    </div>
    <h3 v-if="selectedRelatedTable?.related_tables?.length" class="tw-mt-8 tw-mb-2">Gerelateerde data</h3>
    <Accordion :value="[0]" multiple>
      <AccordionPanel v-for="(table, key) in selectedRelatedTable?.related_tables ?? []" :key="key" :value="key">
        <AccordionHeader class="!tw-text-base">
          {{ table.related_table_title ? table.related_table_title : table.to_table.title }}
        </AccordionHeader>

        <AccordionContent>
          <div>
            <ListTable
              :related-table="table.to_table"
              :field-mapping="getFieldMapping(table.field_mapping, feature)"
              @select-related-table-object="
                onSelectRelatedData(
                  $event.item,
                  $event.relatedTableId,
                  table.related_table_title ? table.related_table_title : table.to_table.title,
                )
              "
            />
          </div>
        </AccordionContent>
      </AccordionPanel>
    </Accordion>
  </div>
  <div v-else-if="loading" class="tw-px-2 tw-mt-4 tw-flex tw-justify-center tw-items-center">
    <ProgressSpinner stroke-width="2" style="width: 48px; height: 48px" />
  </div>
  <div v-else-if="errorMessage" class="tw-mt-4 tw-mb-2 tw-px-2">
    <Message severity="error">{{ errorMessage }}</Message>
  </div>
  <div v-else class="tw-mt-4 tw-mb-2 tw-px-2">
    <Message severity="secondary">Geen resultaat gevonden.</Message>
  </div>
</template>

<script setup lang="ts">
import { IRelatedTable, ICqlFilterEntry, SourceType } from "@/types/related-table";
import { watch, ref, computed } from "vue";
import nunjucks from "nunjucks";
import fetchDot from "fetch-dot";
import ListTable from "./ListTable.vue";
import { formatFriendlyFieldLabel, formatRawString, getResolvedKey } from "@/utils/string-helpers";
import MarkdownTemplate from "@/components/MarkdownTemplate.vue";
import RichValue from "@/components/RichValue.vue";

const { selectedRelatedTableAttributes, selectedRelatedTable } = defineProps<{
  selectedRelatedTableAttributes: Record<string, string> | null;
  selectedRelatedTable: IRelatedTable | null;
  selectedRelatedTableTitle: string | null;
}>();

const emit = defineEmits<{
  (e: "select-related-table-object", type: { relatedTableId: number; item: any; relatedTableTitle: string }): void;
}>();

const loading = ref<boolean>(false);
const errorMessage = ref<string | null>(null);
const feature = ref<Record<string, string> | null>(null);

const tableItems = computed(() => {
  if (selectedRelatedTable?.detail_display_properties && selectedRelatedTable?.detail_display_properties.length > 0) {
    return selectedRelatedTable.detail_display_properties;
  }

  const firstItem = feature.value;
  return firstItem ? Object.keys(firstItem).filter((key) => key !== "x" && key !== "y") : [];
});

const templateFields = computed<Record<string, string>>(() => {
  if (selectedRelatedTable?.template_fields) {
    return {
      ...selectedRelatedTable.template_fields,
    };
  }

  return {};
});

const getFieldMapping = (fieldMapping: Record<string, string>, item: any): Record<string, string> => {
  const mapping: Record<string, string> = {};
  if (fieldMapping) {
    for (const [key, value] of Object.entries(fieldMapping)) {
      mapping[value] = item.properties ? fetchDot(key, item.properties) : fetchDot(key, item);
    }
  }

  return mapping;
};

const onSelectRelatedData = (item: any, relatedTableId: number, relatedTableTitle: string) => {
  // Emit event or handle related data selection
  feature.value = null;
  loading.value = true;
  errorMessage.value = null;
  emit("select-related-table-object", { relatedTableId: relatedTableId, item, relatedTableTitle });
};

const getRestData = async (table: IRelatedTable, item: any) => {
  const fullUrl = `${table.source.url}${table.detail_endpoint}`;
  const renderedUrl = nunjucks.renderString(fullUrl, item);

  try {
    const response = await fetch(renderedUrl);

    if (!response.ok) {
      let error = `Er is een onbekende fout opgetreden bij het ophalen van de gegevens. Probeer het later opnieuw. HTTP Status: ${response.status}`;

      try {
        const errorResponse = await response.json();

        if (table.detail_error_property) {
          error = fetchDot(table.detail_error_property, errorResponse) ?? error;
        }
      } catch {
        // Response body was not JSON, ignore and use default message
      }

      throw new Error(error);
    }

    const data = await response.json();
    return table.detail_property ? fetchDot(table.detail_property, data) : data;
  } catch (error) {
    errorMessage.value = (error as Error).message;
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
        const error = `Er is een fout opgetreden bij het ophalen van de gegevens. Probeer het later opnieuw. HTTP Status: ${result.status}`;
        throw new Error(error);
      }

      const data = await result.json();
      const properties = data.features[0]?.properties || {};

      return properties;
    } catch (e) {
      errorMessage.value = (e as Error).message;
    }
  }

  return [];
};

const getRelatedTableData = async (table: IRelatedTable, item: any) => {
  if (table.source_type === SourceType.REST) {
    return await getRestData(table, item);
  }

  if (table.source_type === SourceType.WMTS || table.source_type === SourceType.OWS) {
    return await getOwsData(table, item);
  }

  return [];
};

const fetchDetailData = async () => {
  loading.value = true;
  errorMessage.value = null;

  if (selectedRelatedTable) {
    feature.value = await getRelatedTableData(selectedRelatedTable, selectedRelatedTableAttributes);
  }

  loading.value = false;
};

watch(
  () => selectedRelatedTableAttributes,
  async () => {
    await fetchDetailData();
  },
  { deep: true, immediate: true },
);
</script>
