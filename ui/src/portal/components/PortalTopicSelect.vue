<template>
  <div class="tw-flex tw-gap-2">
    <Dropdown
      v-model="selectedTopic"
      :options="topicCategories"
      option-label="label"
      option-value="value"
      placeholder="Selecteer een onderwerp"
      class="tw-max-w-full"
      :loading="loading"
      :disabled="loading"
      show-clear
      @change="onTopicChange"
    />
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
</script>
