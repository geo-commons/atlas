<template>
  <div class="feature-info-linked-data">
    <button class="back-button" @click="back">
      <ArrowLeftIcon class="icon __smedium" />
      <span class="back-button-text">Terug naar overzicht</span>
    </button>

    <h3>{{ selectedRelatedTableAttributes?.relatedTable.title || "Loading..." }}</h3>
    <!--    <h3>Gezocht op: [{{ property }}] met waarde: [{{ value }}]</h3>-->

    <!--    <div v-if="loading" class="loading">Loading linked data...</div>-->

    <!--    <div v-else-if="error" class="error">-->
    <!--      {{ error }}-->
    <!--    </div>-->

    <!--    <div v-else-if="linkedDataItems.length === 0" class="no-results">No linked data found</div>-->

    <div class="">
      <div v-for="(result, i) in relatedTableData" :key="i" class="">
        <div v-for="(value, key) in result" :key="key" class="">
          <span class="label">{{ key }}:</span>
          <span class="value">{{ value }}</span>
        </div>
      </div>
    </div>

    <div v-if="feature !== null && relatedTables.length > 0">
      <div v-for="(table, key) in relatedTables" :key="key">
        <RelatedTableList
          :table-feature="feature"
          :related-table="table"
          @select-related-table-object="onSelectRelatedTableObject"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import ArrowLeftIcon from "@/assets/icons/arrow-left-icon.svg";
import { IRelatedTable, SourceType } from "@/types/related-table";
import nunjucks from "nunjucks";
import RelatedTableList from "@/components/related-tables/RelatedTableList.vue";

const { selectedRelatedTableAttributes } = defineProps<{
  selectedRelatedTableAttributes: { relatedTable: IRelatedTable; item: any };
}>();

const emit = defineEmits<{
  (e: "back"): void;
  (e: "select-related-table-object", type: { relatedTable: IRelatedTable; item: any }): void;
}>();

const relatedTableData = ref<Record<string, string>[]>([{}]);
const relatedTable = ref<IRelatedTable | null>(null);
const relatedTables = ref<IRelatedTable[]>([]);
const feature = ref<object | null>(null);

const back = () => {
  emit("back");
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

const getRelatedTableData = (table: IRelatedTable, item: any) => {
  if (table.source_type === SourceType.REST) {
    return getRestData(table, item);
  }

  if (table.source_type === SourceType.WMTS) {
    return [];
  }

  return [];
};

const getRelatedTables = async (table: IRelatedTable) => {
  relatedTables.value = [];
  table.related_tables?.forEach(async (relatedTable) => {
    const response = await fetch(`/atlas/api/v1/tables-v2/${relatedTable.slug || relatedTable.to_table.slug}/`);
    const result = await response.json();

    if (!response.ok) {
      console.error("gaat iets fout bij het ophalen van gerelateerde tabel");
      return;
    }

    relatedTables.value.push(result as IRelatedTable);
  });
};

const handleSelectedRelatedTableAttributes = async () => {
  await getRelatedTables(selectedRelatedTableAttributes.relatedTable);

  relatedTable.value = selectedRelatedTableAttributes.relatedTable;

  feature.value = selectedRelatedTableAttributes.item;

  relatedTableData.value = await getRelatedTableData(
    selectedRelatedTableAttributes.relatedTable,
    selectedRelatedTableAttributes.item,
  );
};

onMounted(async () => {
  await handleSelectedRelatedTableAttributes();
});

watch(
  () => selectedRelatedTableAttributes,
  async () => {
    await handleSelectedRelatedTableAttributes();
  },
  { deep: true },
);
</script>

<style scoped>
.back-button {
  display: flex;
  align-items: center;
  font-size: var(--font-size-small);
  gap: 4px;
  margin: 0 0 24px 6px;
}
</style>
