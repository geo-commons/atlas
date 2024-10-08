<script setup lang="ts">
// Properties
import CircleCheckIcon from "@/assets/icons/circle-check-icon.svg";
import CircleCrossIcon from "@/assets/icons/circle-cross-icon.svg";
import { formatDateValue } from "../../utils/date-formatter";

type AdminListViewTableValueProps = {
  value: string | boolean;
};

const props = withDefaults(defineProps<AdminListViewTableValueProps>(), {});

// Date logic
function isValidDate(dateString: string) {
  const date = new Date(dateString);

  if (isNaN(date.getTime())) {
    return false;
  }

  return date;
}
</script>

<template>
  <span v-if="value === true"> <CircleCheckIcon class="icon __green" /> </span>
  <span v-else-if="value === false"> <CircleCrossIcon class="icon __red" /> </span>
  <span v-else-if="isValidDate(value)">{{ formatDateValue(value) }}</span>
  <span v-else>{{ value }}</span>
</template>
