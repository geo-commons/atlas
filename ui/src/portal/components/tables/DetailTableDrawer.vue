<template>
  <div class="card flex justify-center">
    <Drawer
      :visible="visible"
      position="right"
      class="!tw-w-full md:!tw-w-1/2"
      @update:visible="emit('update:visible', $event)"
    >
      <template #header>
        <div class="tw-flex tw-flex-col tw-gap-2">
          <!-- Button group above title -->
          <div>
            <ButtonGroup>
              <Button variant="outlined" size="small" label="Terug" icon="pi pi-arrow-left" @click="back" />
              <Button
                variant="outlined"
                size="small"
                label="Sluiten"
                icon="pi pi-times"
                @click="closeRelatedTableDetails"
              />
            </ButtonGroup>
          </div>
        </div>
      </template>
      <DetailTable
        v-if="selectedRelatedTable"
        :selected-related-table-attributes="selectedRelatedTableAttributes"
        :selected-related-table="selectedRelatedTable"
        @select-related-table-object="emit('select-related-table-object', $event)"
      />
      <div v-else-if="loading" class="tw-px-2 tw-mt-4 tw-flex tw-justify-center tw-items-center">
        <ProgressSpinner stroke-width="2" style="width: 48px; height: 48px" />
      </div>
      <div v-else-if="errorMessage" class="tw-mt-4 tw-mb-2 tw-px-2">
        <Message severity="error">{{ errorMessage }}</Message>
      </div>
      <div v-else class="tw-mt-4 tw-mb-2 tw-px-2">
        <Message severity="secondary">Geen gerelateerde tabel gevonden.</Message>
      </div>
    </Drawer>
  </div>
</template>

<script setup lang="ts">
import { IRelatedTable } from "@/types/related-table";
import DetailTable from "@/portal/components/tables/DetailTable.vue";
import { watch, ref, onMounted } from "vue";

const { selectedRelatedTableAttributes, selectedRelatedTableId, visible } = defineProps<{
  selectedRelatedTableAttributes: Record<string, string> | null;
  selectedRelatedTableId: number | null;
  visible: boolean;
}>();

const emit = defineEmits<{
  (e: "update:visible", value: boolean): void;
  (e: "select-related-table-object", type: { relatedTableId: number; item: any }): void;
  (e: "back"): void;
  (e: "close-related-table-details"): void;
}>();

const back = () => {
  emit("back");
};

const closeRelatedTableDetails = () => {
  emit("close-related-table-details");
};

const selectedRelatedTable = ref<IRelatedTable | null>(null);
const errorMessage = ref<string | null>(null);
const loading = ref<boolean>(true);

const fetchRelatedTable = async (id: number | null) => {
  loading.value = true;
  selectedRelatedTable.value = null;

  try {
    const response = await fetch(`/atlas/api/v1/tables/${id}/`);
    const result = await response.json();

    selectedRelatedTable.value = result;
  } catch {
    errorMessage.value =
      "Er is een fout opgetreden bij het ophalen van de gerelateerde tabel. Probeer het later opnieuw.";
  } finally {
    loading.value = false;
  }
};

watch(
  () => selectedRelatedTableId,
  async (id) => {
    if (id) {
      await fetchRelatedTable(id);
    }
  },
  { immediate: true },
);

onMounted(async () => {
  if (selectedRelatedTableId) {
    await fetchRelatedTable(selectedRelatedTableId);
  }
});
</script>
