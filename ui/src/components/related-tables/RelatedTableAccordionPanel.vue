<template>
  <AccordionPanel :value="value">
    <AccordionHeader class="!tw-text-base">
      <span
        >{{ title }} <span v-if="count !== null">({{ count }})</span></span
      >
    </AccordionHeader>

    <AccordionContent class="tw-overflow-x-scroll">
      <slot :set-count="setCount" />
    </AccordionContent>
  </AccordionPanel>
</template>

<script setup lang="ts">
import { ref } from "vue";

defineProps<{
  value: string | number;
  title: string;
}>();

defineSlots<{
  default(props: { setCount: (count: number) => void }): unknown;
}>();

const count = ref<number | null>(null);

const setCount = (newCount: number) => {
  count.value = newCount;
};
</script>
