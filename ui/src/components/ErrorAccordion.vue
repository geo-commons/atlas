<script setup lang="ts">
interface ErrorAccordionProps {
  error: string | null;
}

// Props
const { error } = defineProps<ErrorAccordionProps>();
</script>

<template>
  <Accordion v-if="error" value="error" class="tw-mb-4">
    <AccordionPanel value="error" class="!tw-rounded-lg !tw-border !tw-border-red-500">
      <AccordionHeader
        :pt="{
          toggleicon: '!tw-text-red-500',
        }"
        class="!tw-px-4 !tw-py-4 !tw-text-red-500"
        >Er is iets fout gegaan bij het opslaan</AccordionHeader
      >
      <AccordionContent
        class="!tw-px-0"
        :pt="{
          content: '!tw-px-4 !tw-py-0 !tw-mt-0 !tw--mt-4',
        }"
      >
        <p class="m-0 tw-text-red-500">
          {{ error }}
        </p>
      </AccordionContent>
    </AccordionPanel>
  </Accordion>
</template>
