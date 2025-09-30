<template>
  <span
    v-if="visibility"
    class="tw-inline-block tw-px-2 tw-py-0.5 tw-rounded-xl tw-text-xs tw-font-medium tw-ml-1 tw-tracking-wide tw-align-baseline tw-whitespace-nowrap tw-flex-shrink-0 tw-my-1"
    :class="getVisibilityClass(visibility)"
  >
    {{ visibility }}
  </span>
</template>

<script setup lang="ts">
interface VisibilityIndicatorProps {
  visibility?: string | null;
}

const { visibility = null } = defineProps<VisibilityIndicatorProps>();

const getVisibilityClass = (visibility: string): string => {
  switch (visibility.toLowerCase()) {
    case "publiek":
      return "visibility-public tw-bg-blue-100 tw-text-blue-800";
    case "intern":
      return "visibility-internal tw-bg-purple-100 tw-text-purple-800";
    default:
      return "visibility-default";
  }
};
</script>
