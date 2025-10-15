<template>
  <div class="tw-min-w-[200px] tw-flex tw-gap-2">
    <Dropdown
      v-model="selectedTopic"
      :options="topicCategories"
      option-label="label"
      option-value="value"
      placeholder="Selecteer een onderwerp"
      class="tw-flex-1"
      :loading="loading"
      :disabled="loading"
      @change="onTopicChange"
    />
    <button
      v-if="hasSelectedTopic"
      class="tw-px-3 tw-py-2 tw-text-sm tw-bg-gray-100 hover:tw-bg-gray-200 focus:tw-bg-gray-200 focus:tw-outline-none focus:tw-ring-2 focus:tw-ring-blue-500 focus:tw-ring-offset-2 tw-text-gray-700 tw-rounded-md tw-border tw-border-gray-300 tw-transition-colors tw-duration-200 tw-whitespace-nowrap"
      title="Wis onderwerp filter"
      @click="clearTopic"
    >
      ✕
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

interface TopicOption {
  value: string;
  label: string;
}

interface PortalTopicSelectProps {
  selectedTopic?: string;
}

interface DropdownChangeEvent {
  value: string;
}

interface PortalTopicSelectEmits {
  (e: "on-topic-change", value: string): void;
}

const props = withDefaults(defineProps<PortalTopicSelectProps>(), {
  selectedTopic: "",
});

const emit = defineEmits<PortalTopicSelectEmits>();

const topicCategories = ref<TopicOption[]>([]);
const loading = ref(false);

const fetchTopicCategories = async () => {
  loading.value = true;
  try {
    const response = await fetch("/atlas/api/v1/metadatasets/topic-categories/", {
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
    });
    if (!response.ok) {
      console.error("Could not fetch topic categories");
      return;
    }
    const data = await response.json();
    topicCategories.value = data;
    loading.value = false;
  } catch (error) {
    console.error("Error fetching topic categories:", error);
  }
};

onMounted(() => {
  fetchTopicCategories();
});

const selectedTopic = computed({
  get: () => props.selectedTopic,
  set: (value: string) => {
    emit("on-topic-change", value);
  },
});

const onTopicChange = (event: DropdownChangeEvent) => {
  emit("on-topic-change", event.value);
};

const hasSelectedTopic = computed(() => {
  return props.selectedTopic !== "";
});

const clearTopic = () => {
  emit("on-topic-change", "");
};
</script>
