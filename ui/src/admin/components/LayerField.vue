<template>
  <div class="layer-field">
    <Select
      class="!tw-mt-2"
      :model-value="props.modelValue"
      placeholder="Kies een laag"
      filter-placeholder="Zoek laag"
      :options="availableLayers"
      :loading="isLoading"
      filter
      fluid
      @update:modelValue="(value) => emit('update:modelValue', value)"
    ></Select>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { WMSCapabilities } from "ol/format";

const props = defineProps({
  currentSourceId: {
    type: Number,
  },
  sources: {
    type: Array,
    default: () => [],
  },
  modelValue: {
    type: String,
    default: () => "",
  },
});

const emit = defineEmits(["update:modelValue"]);

const availableLayers = ref([]);
const isLoading = ref(true);

const selectedSource = computed(() => {
  return props.sources.find((arr) => arr.id === props.currentSourceId);
});

watch(
  () => selectedSource.value,
  (newValue, oldValue) => {
    if (newValue !== oldValue || newValue?.id !== oldValue?.id) {
      getLayers();
    }
  },
);

const getLayers = async () => {
  availableLayers.value = [];
  isLoading.value = true;

  if (!selectedSource.value) {
    return;
  }

  // Don't run GetLayers for source with type REST, only for OWS
  if (selectedSource.value.type !== "OWS") {
    return;
  }

  try {
    const url = new URL(selectedSource.value.url);

    const params = new URLSearchParams({
      SERVICE: "WMS",
      REQUEST: "GetCapabilities",
      VERSION: "1.1.1",
    });

    url.search = params.toString();

    const response = await fetch(url);
    const body = await response.text();

    if (!body) {
      return;
    }

    const caps = await new WMSCapabilities().read(body);
    const layers = caps?.Capability?.Layer?.Layer.map((layer) => layer.Name);

    availableLayers.value = layers ? layers : [];

    isLoading.value = false;
  } catch (e) {
    console.error("failed to fetch source capabilities: ", e);

    isLoading.value = false;
  }
};

onMounted(async () => {
  await getLayers();
});
</script>
