<template>
  <div
    class="tw-mt-4 tw-bg-white tw-rounded-lg tw-border tw-border-gray-200 tw-p-4 tw-border-solid tw-flex tw-flex-col tw-gap-4 tw-items-start"
  >
    <div v-for="table in relatedTables" :key="table.id" class="tw-w-full">
      <div class="tw-flex">
        <Panel :header="table.title" toggleable class="tw-flex-1">
          <div class="tw-space-y-4">
            <div>Naar de tabel: {{ table.title }}</div>

            <div>
              <label class="tw-block tw-text-sm tw-font-medium tw-text-gray-700 tw-mb-2"> Field Mapping (JSON) </label>
              <CodeMirror
                :id="`field-mapping-${table.id}`"
                :model-value="formatFieldMapping(table.field_mapping)"
                :extensions="[extensions]"
                :basic="false"
                class="!tw-text-sm tw-border tw-border-gray-300 tw-rounded"
                @update:model-value="(value) => updateFieldMapping(table.id, value)"
              />
            </div>
          </div>
        </Panel>
        <button
          v-tippy="{ placement: 'bottom' }"
          class="iconbutton __normal __round __admin_hover"
          :aria-label="'Verwijderen'"
          content="Verwijderen"
          type="button"
          @click="deleteRelatedTable(table.id)"
        >
          <TrashIcon class="icon" />
        </button>
      </div>
    </div>
    <Button
      class="!tw-text-sm !tw-font-medium tw-mt-3"
      @click="
        () => {
          showAddNewTableDrawer = true;
        }
      "
    >
      <AddIcon class="tw-w-4 tw-h-4" />
      Nieuwe relatie
    </Button>
    <Drawer v-model:visible="showAddNewTableDrawer" position="right" header="Nieuwe relatie naar tabel toevoegen">
      <div class="tw-space-y-4">
        <div>
          <label class="tw-block tw-text-sm tw-font-medium tw-text-gray-700 tw-mb-2"> Selecteer een tabel </label>
          <Dropdown
            v-model="selectedTable"
            :options="options"
            option-label="title"
            placeholder="Kies een tabel"
            class="tw-w-full"
            :disabled="!options || options.length === 0"
          />
        </div>
        <div class="tw-flex tw-gap-2">
          <Button class="!tw-text-sm !tw-font-medium" :disabled="!selectedTable" @click="addRelatedTable">
            Toevoegen
          </Button>
          <Button class="!tw-text-sm !tw-font-medium" severity="secondary" @click="cancelAddTable"> Annuleren</Button>
        </div>
      </div>
    </Drawer>
  </div>
</template>

<script setup lang="ts">
import CodeMirror from "vue-codemirror6";
import { json, jsonParseLinter } from "@codemirror/lang-json";
import { clouds } from "thememirror";
import { linter } from "@codemirror/lint";
import { Text } from "@codemirror/state";
import AddIcon from "@/assets/icons/add-icon.svg";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import { IRelatedTable } from "@/types/related-table";
import { ref, toRefs } from "vue";

interface RelatedTablesFieldProps {
  relatedTables: IRelatedTable[] | null;
  options: IRelatedTable[];
  parentId: number;
}

interface RelatedTablesFieldEmits {
  (e: "related-tables-changed", value: IRelatedTable[]): void;
}

const props = defineProps<RelatedTablesFieldProps>();
const { relatedTables, options } = toRefs(props);

console.log(relatedTables);

const emit = defineEmits<RelatedTablesFieldEmits>();

const extensions = [json(), linter(jsonParseLinter()), clouds];
const showAddNewTableDrawer = ref<boolean>(false);
const selectedTable = ref<IRelatedTable | null>(null);

function formatFieldMapping(fieldMapping: Record<string, string>): string {
  if (!fieldMapping) return "{}";

  return JSON.stringify(fieldMapping, null, 2);
}

// todo: check for valid json
function updateFieldMapping(tableId: number, value: string | Text | undefined) {
  if (!relatedTables.value || typeof value !== "string") return;

  const relatedTable = relatedTables.value.find((table) => tableId === table.id);

  if (relatedTable) {
    if (!value || value.trim() === "") {
      relatedTable.field_mapping = {};
      return;
    }

    try {
      relatedTable.field_mapping = JSON.parse(value);
    } catch {
      // Ignore JSON parse errors.
    }
    emit("related-tables-changed", relatedTables.value);
  }
}

function addRelatedTable() {
  if (!selectedTable.value || !relatedTables.value) return;

  // Create a copy of the selected table with empty field mapping for the new relation
  const newRelatedTable: IRelatedTable = {
    ...selectedTable.value,
    field_mapping: {},
    related_tables: null, // Reset related tables for the copy to avoid nested relations
  };

  const updatedRelatedTables = [...relatedTables.value, newRelatedTable];
  emit("related-tables-changed", updatedRelatedTables);

  // Reset selection and close drawer
  selectedTable.value = null;
  showAddNewTableDrawer.value = false;
}

function cancelAddTable() {
  selectedTable.value = null;
  showAddNewTableDrawer.value = false;
}

function deleteRelatedTable(tableId: number) {
  if (!relatedTables.value) return;

  const updatedRelatedTables = relatedTables.value.filter((table) => table.id !== tableId);
  emit("related-tables-changed", updatedRelatedTables);
}
</script>

<style scoped></style>
