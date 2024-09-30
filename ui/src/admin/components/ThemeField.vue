<template>
  <div class="theme-field" :style="{ maxWidth: `${questionsWidth}px` }">
    <multi-select
      :v-bind="field"
      :loading="!availableThemes.length"
      :model-value="props.modelValue"
      :options="availableThemes"
      option-label="title"
      placeholder="Kies thema's"
      data-key="id"
      filter
      fluid
      class="!max-w-full"
      filter-placeholder="Zoek thema"
      @update:modelValue="(value) => emit('update:modelValue', value)"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => [],
  },
  field: {
    type: Object,
    default: () => ({}),
  },
});
const emit = defineEmits(["update:modelValue"]);

const availableThemes = ref([]);
const questionsWidth = ref(0);

const getThemes = async () => {
  try {
    const result = await fetch("/atlas/api/v1/themes/", {
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
    });

    if (!result.ok) {
      throw new Error("Could not fetch themes");
    }

    const response = await result.json();
    availableThemes.value = response.map((theme) => ({
      id: theme.id,
      title: theme.title,
    }));
  } catch (error) {
    console.error(error);
  }
};

const setQuestionsWidth = () => {
  questionsWidth.value = document.getElementsByClassName("section-questions")[0].offsetWidth;
};

onMounted(() => {
  getThemes();
  setQuestionsWidth();
  window.addEventListener("resize", setQuestionsWidth);
});

onUnmounted(() => {
  window.removeEventListener("resize", setQuestionsWidth);
});
</script>
