<template>
  <div class="tw-min-h-screen tw-bg-gray-50">
    <header class="tw-bg-white tw-border-b tw-border-gray-200 tw-border-solid tw-border-0">
      <div class="tw-max-w-7xl tw-mx-auto tw-px-6 tw-py-10">
        <div class="tw-flex tw-items-start tw-gap-4">
          <div
            class="tw-w-16 tw-h-16 tw-bg-gray-50 tw-rounded-2xl tw-flex tw-items-center tw-justify-center tw-flex-shrink-0"
          >
            <i class="pi pi-table tw-text-2xl tw-text-gray-700" aria-hidden="true"></i>
          </div>
          <div class="tw-flex-1">
            <h1 class="tw-text-4xl tw-my-3">{{ table ? table.title : error ? "Error" : loading ? "Laden..." : "" }}</h1>
          </div>
        </div>
      </div>
    </header>

    <div v-if="loading" class="tw-flex tw-justify-center tw-items-center tw-min-h-[60vh]">
      <Spinner class="spinner" :style-type="'portal'" />
    </div>

    <div v-else-if="error" class="tw-max-w-7xl tw-mx-auto tw-px-6 tw-py-10">
      <Message severity="error">{{ error }}</Message>
    </div>

    <main
      v-else
      id="main-content"
      class="tw-max-w-7xl tw-mx-auto tw-px-6 tw-pt-8 tw-grid lg:tw-grid-cols-4 tw-gap-6 tw-items-start"
    >
      <section
        v-if="isSearchEnabled"
        class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-6 lg:tw-col-span-1"
      >
        <Form v-slot="{ errors, meta }" :initial-values="initialValues" @submit="onSubmit">
          <div class="tw-grid lg:tw-grid-cols-1 tw-gap-6 tw-items-end">
            <div v-for="searchField in searchFields" :key="searchField">
              <label
                :class="['tw-block tw-text-sm tw-font-medium tw-mb-2', errors[searchField] ? 'tw-text-red-600' : '']"
              >
                {{ friendlySearchFields[searchField] ? friendlySearchFields[searchField] : searchField }}
                <span v-if="errors[searchField]" class="tw-text-red-600"> - {{ errors[searchField] }}</span>
              </label>

              <Field v-slot="{ field }" :name="searchField" rules="required">
                <InputText
                  v-bind="field"
                  :model-value="field.value"
                  class="tw-w-full"
                  type="text"
                  @update:model-value="field.onChange"
                />
              </Field>
            </div>

            <Button label="Zoeken" icon="pi pi-search" type="submit" :disabled="!meta.valid" />
          </div>
        </Form>
      </section>

      <section
        :class="`tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-6 tw-overflow-hidden ${isSearchEnabled ? 'lg:tw-col-span-3' : 'lg:tw-col-span-4'}`"
      >
        <ListTable
          v-if="relatedTable"
          :related-table="relatedTable"
          :field-mapping="fieldMapping"
          @select-related-table-object="onSelectRelatedTableObject"
        />
        <Message v-else-if="isSearchEnabled" severity="info">
          Voer een zoekopdracht uit om de gegevens te bekijken.
        </Message>
        <Message v-else severity="secondary">Geen resultaten gevonden.</Message>
      </section>
    </main>
  </div>

  <DetailTableDrawer
    v-model:visible="visible"
    :selected-related-table-attributes="selectedRelatedTableAttributes"
    :selected-related-table-id="selectedRelatedTableId"
    :selected-related-table-title="selectedRelatedTableTitle"
    @select-related-table-object="onSelectRelatedTableObject"
    @back="back"
    @close-related-table-details="closeRelatedTableDetails"
  />
</template>

<script setup lang="ts">
import { IRelatedTable } from "@/types/related-table";
import { onMounted, ref, computed } from "vue";
import { useRoute } from "vue-router";
import { Form, Field } from "vee-validate";
import ListTable from "@/portal/components/tables/ListTable.vue";
import DetailTableDrawer from "../components/tables/DetailTableDrawer.vue";

const route = useRoute();

const loading = ref<boolean>(true);
const error = ref<string | null>(null);

const table = ref<IRelatedTable | null>(null);

const relatedTable = ref<IRelatedTable | null>(null);
const fieldMapping = ref<Record<string, string>>({});

const selectedRelatedTableAttributes = ref<Record<string, string> | null>(null);
const selectedRelatedTableId = ref<number | null>(null);
const selectedRelatedTableTitle = ref<string | null>(null);
const history = ref<{ relatedTableId: number; item: any; relatedTableTitle: string }[]>([]);
const visible = ref<boolean>(false);

const onSelectRelatedTableObject = (data: { relatedTableId: number; item: any; relatedTableTitle: string }) => {
  selectedRelatedTableAttributes.value = data.item;
  selectedRelatedTableId.value = data.relatedTableId;
  selectedRelatedTableTitle.value = data.relatedTableTitle;
  visible.value = true;
  history.value.push(data);
};

const back = () => {
  if (history.value.length > 0) {
    history.value.pop();

    if (history.value.length) {
      const lastHistoryItem = history.value[history.value.length - 1];
      selectedRelatedTableAttributes.value = lastHistoryItem.item;
      selectedRelatedTableId.value = lastHistoryItem.relatedTableId;
      selectedRelatedTableTitle.value = lastHistoryItem.relatedTableTitle;
      return;
    }
  }

  // if no history item was found, reset the history and selected related table attributes
  selectedRelatedTableAttributes.value = null;
  history.value = [];
  visible.value = false;
};

const closeRelatedTableDetails = () => {
  selectedRelatedTableAttributes.value = null;
  selectedRelatedTableId.value = null;
  selectedRelatedTableTitle.value = null;
  history.value = [];
  visible.value = false;
};

// Build initial values so vee-validate knows all fields
const initialValues = computed(() => Object.fromEntries(searchFields.value.map((f) => [f, ""])));

const onSubmit = (values: Record<string, string>) => {
  search(values);
};

const search = (values: Record<string, string>) => {
  relatedTable.value = table.value;
  fieldMapping.value = values;
};

const getTable = async () => {
  try {
    const res = await fetch(`/atlas/api/v1/tables/${route.params.slug}/`, {
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
    });

    if (!res.ok) {
      error.value = "Kon de tabel niet laden. Controleer de URL of probeer het later opnieuw.";
      table.value = null;
      return;
    }

    table.value = (await res.json()) as IRelatedTable;
  } catch {
    error.value = "Er is een probleem opgetreden bij het laden van de tabel.";
    table.value = null;
  } finally {
    loading.value = false;
  }
};

const asTemplateSource = (v: unknown): string => {
  if (v == null) return "";
  if (typeof v === "string") return v;

  // If post_body is already an object, turn it into a JSON string
  // so {{...}} inside values can be found.
  try {
    return JSON.stringify(v);
  } catch {
    return String(v);
  }
};

const extractTemplateParams = (v: unknown): string[] => {
  const s = asTemplateSource(v);

  const blocks = s.match(/{{[\s\S]*?}}/g) ?? [];
  const parameters = new Set<string>();

  for (const block of blocks) {
    const expr = block.slice(2, -2).trim();
    // capture first "root" identifier in the expression
    // examples:
    // postcode.replaceAll(...)   -> postcode
    // postcode | replace(' ', '') -> postcode
    // (postcode ?? '')           -> postcode
    const m = expr.match(/[A-Za-z_$][\w$]*/);
    if (m) parameters.add(m[0]);
  }

  return [...parameters];
};

const searchFields = computed<string[]>(() => {
  const params = new Set<string>();

  for (const p of extractTemplateParams(table.value?.list_endpoint)) params.add(p);
  for (const p of extractTemplateParams(table.value?.request_body)) params.add(p);
  for (const p of extractTemplateParams(table.value?.list_cql_filters)) params.add(p);

  return [...params];
});

const friendlySearchFields = computed<Record<string, string>>(() => {
  if (table.value?.friendly_search_fields) {
    return {
      ...table.value.friendly_search_fields,
    };
  }

  return {};
});

const isSearchEnabled = computed(() => {
  if (table.value && searchFields.value.length) {
    return true;
  }

  return false;
});

onMounted(async () => {
  await getTable();

  if (!isSearchEnabled.value) {
    search({});
  }
});
</script>
