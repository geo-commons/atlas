<template>
  <span
    v-if="visibility"
    v-tippy="{ content: getTooltipText(visibility), placement: 'top' }"
    class="tw-inline-block tw-px-2 tw-py-0.5 tw-rounded-xl tw-text-xs tw-font-medium tw-ml-1 tw-tracking-wide tw-align-baseline tw-whitespace-nowrap tw-flex-shrink-0 tw-my-1 tw-lowercase tw-cursor-help"
    :class="getVisibilityClass(visibility)"
  >
    {{ visibility }}
  </span>
</template>

<script setup lang="ts">
type VisibilityValue = "intern" | "Intern" | "publiek" | "Publiek";

interface VisibilityIndicatorProps {
  visibility?: VisibilityValue | null;
}

const { visibility = null } = defineProps<VisibilityIndicatorProps>();

const getVisibilityClass = (visibility: VisibilityValue): string => {
  if (visibility.toLowerCase() === "publiek") {
    return "visibility-public tw-bg-blue-100 tw-text-blue-800";
  }
  return "visibility-internal tw-bg-purple-100 tw-text-purple-800";
};

const getTooltipText = (visibility: VisibilityValue): string => {
  if (visibility.toLowerCase() === "publiek") {
    return "Deze informatie is zichtbaar voor alle niet-ingelogde gebruikers wanneer deze informatie is gepubliceerd.";
  }
  return "Deze informatie is alleen zichtbaar voor interne gebruikers en wordt niet getoond aan niet-ingelogde bezoekers.";
};
</script>
