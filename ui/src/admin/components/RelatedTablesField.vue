<template>
  <div class="tw-mt-4 tw-bg-white tw-rounded-lg tw-border tw-border-gray-200 tw-p-4 tw-border-solid">
    <div class="tw-flex tw-gap-2">
      <Panel v-for="table in relatedTables" :key="table.id" :header="table.title" toggleable class="tw-flex-1">
        <div class="tw-space-y-4">
          <div>
            <p><strong>Naar de tabel:</strong> {{ table.title }}</p>
          </div>

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
        @click="() => {}"
      >
        <TrashIcon class="icon" />
      </button>
    </div>
    <Button class="!tw-text-sm !tw-font-medium tw-mt-3" @click="() => {}">
      <AddIcon class="tw-w-4 tw-h-4" />
      Nieuwe relatie
    </Button>
  </div>
</template>

<script setup lang="ts">
import CodeMirror from "vue-codemirror6";
import { json, jsonParseLinter } from "@codemirror/lang-json";
import { clouds } from "thememirror";
import { linter } from "@codemirror/lint";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import AddIcon from "@/assets/icons/add-icon.svg";
import { IRelatedTable } from "@/types/related-table";

interface RelatedTablesFieldProps {
  relatedTables: IRelatedTable[] | null;
  options: IRelatedTable[];
  parentId: number;
}

interface RelatedTablesFieldEmits {
  (e: "related-tables-changed", value: IRelatedTable[]): void;
}

const { relatedTables, parentId, options } = defineProps<RelatedTablesFieldProps>();

const emit = defineEmits<RelatedTablesFieldEmits>();

const extensions = [json(), linter(jsonParseLinter()), clouds];

console.log("options", options);

function formatFieldMapping(fieldMapping: Record<string, string>): string {
  if (!fieldMapping) return "{}";

  return JSON.stringify(fieldMapping, null, 2);
}

// todo: check for valid json
function updateFieldMapping(tableId: number, value: string) {
  if (!relatedTables) return;

  const relatedTable = relatedTables.find((table) => tableId === table.id);

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
    emit("related-tables-changed", relatedTables);
  }
}
</script>

<style scoped></style>
