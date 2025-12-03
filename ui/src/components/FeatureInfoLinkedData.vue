<script setup lang="ts">
import { onMounted, ref } from "vue";
import ArrowLeftIcon from "@/assets/icons/arrow-left-icon.svg";

// interface LinkedDataRelation {
//   from_linked_data: number
//   to_linked_data: number
//   source_key: string
//   target_key: string
// }
//
// interface LinkedData {
//   id: number
//   title: string
//   name: string
//   kind: string
//   url: string
//   source_key: string
//   target_key: string
//   headers: string[]
//   display_properties: string[]
//   use_detail_view: boolean
//   detail_view_fields: string[]
//   related: LinkedDataRelation[]
// }

interface Props {
  id: number;
  property: string;
  value: string;
}

const { id, property, value } = defineProps<Props>();

const linkedDataItems = ref<any[]>([]);
const linkedData = ref<any>(null);
const loading = ref(false);
const error = ref<string | null>(null);
const emit = defineEmits<{
  back: [];
}>();

// const hasRelatedData = computed(() => {
//   return props.linkedData.related && props.linkedData.related.length > 0
// })

// const sourceValue = computed(() => {
//   return props.feature?.properties?.[props.linkedData.source_key] || null
// })

const fetchLinkedData = async () => {
  loading.value = true;
  error.value = null;

  try {
    // First fetch the linked data object
    const linkedDataResponse = await fetch(`/atlas/api/v1/linked-data/${id}/`);

    if (!linkedDataResponse.ok) {
      throw new Error(`Failed to fetch linked data: ${linkedDataResponse.status}`);
    }

    const linkedDataObject = await linkedDataResponse.json();
    linkedData.value = linkedDataObject;
    // Now fetch features using the linked data object
    const params = new URLSearchParams([
      ["service", "WFS"],
      ["version", "1.0.0"],
      ["request", "GetFeature"],
      ["typename", linkedDataObject.name],
      ["outputFormat", "application/json"],
      ["maxFeatures", "5000"],
    ]);

    if (property && value) {
      console.log("set filter");
      params.set("cql_filter", `${property} = '${value}'`);
    }

    const url = new URL(linkedDataObject.url);
    url.search = params.toString();

    const result = await fetch(url.toString());

    if (!result.ok) {
      if (result.status === 401) {
        throw new Error("U moet ingelogd zijn om deze data te bekijken.");
      } else if (result.status === 403) {
        throw new Error("U heeft geen rechten om deze data te bekijken.");
      } else {
        throw new Error("Er is een fout opgetreden tijdens het ophalen van de gegevens.");
      }
    }

    const data = await result.json();
    linkedDataItems.value = data.features || [];
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Failed to load linked data";
    linkedDataItems.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchLinkedData();
});

const back = () => {
  emit("back");
};
</script>

<template>
  <div class="feature-info-linked-data">
    <button class="back-button" @click="back">
      <ArrowLeftIcon class="icon __smedium" />
      <span class="back-button-text">Terug naar overzicht</span>
    </button>

    <h3>{{ linkedData?.title || "Loading..." }}</h3>
    <h3>Gezocht op: [{{ property }}] met waarde: [{{ value }}]</h3>

    <div v-if="loading" class="loading">Loading linked data...</div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else-if="linkedDataItems.length === 0" class="no-results">No linked data found</div>

    <div v-else class="linked-data-results">
      <div v-for="(feature, index) in linkedDataItems" :key="feature.id || index" class="linked-data-item">
        <div v-for="property in Object.keys(feature.properties || {})" :key="property" class="property">
          <span class="label">{{ property }}:</span>
          <span class="value">{{ feature.properties?.[property] }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.feature-info-linked-data {
  padding: 1rem;
}

.loading,
.error,
.no-results {
  padding: 0.5rem;
  text-align: center;
  font-style: italic;
}

.error {
  color: #dc3545;
}

.linked-data-item {
  border: 1px solid #ddd;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  border-radius: 4px;
}

.property {
  display: flex;
  margin-bottom: 0.25rem;
}

.label {
  font-weight: bold;
  margin-right: 0.5rem;
  min-width: 120px;
}

.value {
  flex: 1;
}
</style>
