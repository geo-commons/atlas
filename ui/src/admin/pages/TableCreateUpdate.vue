<template>
  <div class="container __admin">
    <h1 class="font-weight-normal">Tabel wijzigen</h1>
    <Spinner v-if="loading" style-type="'admin'" />
    <AdminFormSections
      v-else
      ref="formSections"
      :sections="sections"
      :initial-values="initialValues"
      :compact-layout="false"
      :form-object="'tables'"
      :object-specific-save="saveTable"
      @update-source="(source) => (selectedSource.value = source)"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import AdminFormSections from "@/admin/components/AdminFormSections.vue";
import Spinner from "@/components/Spinner.vue";
import { getAllObjects } from "@/utils/api-helpers";
import { useToast } from "primevue";

const route = useRoute();
const router = useRouter();
const toast = useToast();

const formSections = ref();
const sources = ref([]);
const sections = ref({});
const initialValues = ref({});
const loading = ref(false);
const selectedSource = ref({});

const sourceTypes = [
  { id: "OWS", label: "OWS" },
  { id: "WMTS", label: "WMTS" },
  { id: "REST", label: "REST" },
];

async function getTable() {
  const result = await fetch(`/atlas/api/v1/tables-v2/${route.params.id}/`, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch table");
    return;
  }

  const data = await result.json();

  initialValues.value = data;
  initialValues.value.source_id = data.source?.id;
  initialValues.value.list_cql_filters = JSON.stringify(data.list_cql_filters, null, 2);
  initialValues.value.detail_cql_filters = JSON.stringify(data.detail_cql_filters, null, 2);

  const source = data.source;

  // Set selectedSource
  selectedSource.value = {
    id: source.id,
    label: source.title,
    url: source.url,
    type: source.source_type,
  };
}

async function getSources() {
  const url = getAllObjects("/atlas/api/v1/sources/");
  const result = await fetch(url, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch sources");
    return;
  }

  const response = await result.json();
  sources.value = response.results.map((source) => ({
    id: source.id,
    label: source.title,
  }));
}

async function saveTable(currentValues, continueEditing = false) {
  const url = `/atlas/api/v1/tables-v2/${route.params.id}/`;

  try {
    currentValues.list_cql_filters = validateAndParseJsonString(currentValues.list_cql_filters);
    currentValues.detail_cql_filters = validateAndParseJsonString(currentValues.detail_cql_filters);

    const result = await formSections.value.sendSaveRequest(url, "PATCH", currentValues);

    if (result.ok) {
      if (!continueEditing) {
        router.push(`/tables`);
      }

      toast.add({
        severity: "success",
        summary: "Tabel opgeslagen",
        detail: "De tabel is succesvol opgeslagen.",
        life: 3000,
      });
    }
  } catch (e) {
    console.error("An unexpected error occurred:", e);
  }
}

const validateAndParseJsonString = (text) => {
  if (!text || text.trim() === "") {
    return {};
  }

  return JSON.parse(text);
};

onMounted(async () => {
  loading.value = true;
  await Promise.all([getTable(), getSources()]);
  sections.value = getSections();
  loading.value = false;
});

function getSections() {
  return {
    general: {
      label: "Algemene gegevens",
      questions: [
        {
          label: "Titel",
          id: "title",
          name: "Title",
          type: "text",
          required: true,
        },
        {
          label: "Kort kenmerk",
          id: "slug",
          name: "Slug",
          type: "text",
          required: true,
        },
      ],
    },
    source: {
      label: "Bron",
      questions: [
        {
          label: "Bron",
          id: "source_id",
          name: "Source",
          type: "dropdown",
          required: true,
          placeholder: "bron",
          options: sources.value,
        },
        {
          label: "Type bron (OWS, WMTS, REST)",
          id: "source_type",
          name: "SourceType",
          type: "dropdown",
          required: true,
          placeholder: "Type bron",
          options: sourceTypes,
        },
      ],
    },
    table: {
      label: "Tabel Instellingen",
      questions: [
        {
          label: "Beschikbare velden",
          id: "fields",
          name: "Fields",
          type: "array",
          required: false,
        },
        {
          label: "Toon deze velden in de lijstweergave",
          id: "list_display_properties",
          name: "listDisplayProperties",
          type: "array",
          required: false,
          suggestionsFrom: "fields",
        },
        {
          label: "Toon deze velden in de detailweergave",
          id: "detail_display_properties",
          name: "listDisplayProperties",
          type: "array",
          required: false,
          suggestionsFrom: "fields",
        },
      ],
    },
    rest: {
      label: "Rest Specifieke Instellingen",
      questions: [
        {
          label: "Lijst endpoint",
          id: "list_endpoint",
          name: "listEndpoint",
          type: "text",
          required: false,
        },
        {
          label: "Detail endpoint",
          id: "detail_endpoint",
          name: "detailEndpoint",
          type: "text",
          required: false,
        },
        {
          label: "Veldnaam van lijst",
          id: "list_property",
          name: "ListProperty",
          type: "text",
          required: false,
        },
        {
          label: "Veldnaam van detailweergave",
          id: "detail_property",
          name: "DetailProperty",
          type: "text",
          required: false,
        },
        {
          label: "URL parameter voor pagina",
          id: "page_param",
          name: "PageParam",
          type: "text",
          required: false,
        },
        {
          label: "URL parameter voor items per pagina",
          id: "items_per_page_param",
          name: "ItemsPerPageParam",
          type: "text",
          required: false,
        },
        {
          label: "Veldnaam van totaal aantal items",
          id: "total_items_page_property",
          name: "TotalItemsPageProperty",
          type: "text",
          required: false,
        },
        {
          label: "Veldnaam van foutmelding in lijstweergave",
          id: "list_error_property",
          name: "ListErrorProperty",
          type: "text",
          required: false,
        },
        {
          label: "Veldnaam van foutmelding detailweergave",
          id: "detail_error_property",
          name: "DetailErrorProperty",
          type: "text",
          required: false,
        },
      ],
    },
    ows: {
      label: "OWS Specifieke Instellingen",
      questions: [
        {
          label: "Lijst CQL filters",
          id: "list_cql_filters",
          name: "listCqlFilters",
          type: "json",
          required: false,
        },
        {
          label: "Detail CQL filters",
          id: "detail_cql_filters",
          name: "detailCqlFilters",
          type: "json",
          required: false,
        },
      ],
    },
  };
}
</script>
