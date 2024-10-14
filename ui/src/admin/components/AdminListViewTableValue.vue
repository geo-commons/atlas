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
  const regex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?([+-]\d{2}:\d{2})$/;

  if (!regex.test(dateString)) {
    return false;
  }

  const date = new Date(dateString);

  if (isNaN(date.getTime())) {
    return false;
  }

  return date;
}
</script>

<template>
  <span v-if="props.value === true"> <CircleCheckIcon class="icon __green" /> </span>
  <span v-else-if="props.value === false"> <CircleCrossIcon class="icon __red" /> </span>
  <span v-else-if="isValidDate(props.value)">{{ formatDateValue(props.value) }}</span>
  <span v-else>{{ props.value }}</span>
</template>
