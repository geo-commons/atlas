<script setup lang="ts">
import { onMounted } from "vue";
import ArrowLeftIcon from "@/assets/icons/arrow-left-icon.svg";

const { selectedRelatedTableAttributes } = defineProps<{
  selectedRelatedTableAttributes: object;
}>();

const emit = defineEmits<{
  back: [];
}>();

const back = () => {
  emit("back");
};

onMounted(() => {
  console.log(selectedRelatedTableAttributes);
});
</script>

<template>
  <div class="feature-info-linked-data">
    <button class="back-button" @click="back">
      <ArrowLeftIcon class="icon __smedium" />
      <span class="back-button-text">Terug naar overzicht</span>
    </button>

    <h3>{{ selectedRelatedTableAttributes?.slug || "Loading..." }}</h3>
    <!--    <h3>Gezocht op: [{{ property }}] met waarde: [{{ value }}]</h3>-->

    <!--    <div v-if="loading" class="loading">Loading linked data...</div>-->

    <!--    <div v-else-if="error" class="error">-->
    <!--      {{ error }}-->
    <!--    </div>-->

    <!--    <div v-else-if="linkedDataItems.length === 0" class="no-results">No linked data found</div>-->

    <div class="linked-data-results">
      <!--      <div v-for="(feature, index) in linkedDataItems" :key="feature.id || index" class="linked-data-item">-->
      <!--        <div v-for="property in Object.keys(feature.properties || {})" :key="property" class="property">-->
      <!--          <span class="label">{{ property }}:</span>-->
      <!--          <span class="value">{{ feature.properties?.[property] }}</span>-->
      <!--        </div>-->
      <!--      </div>-->
    </div>
  </div>
</template>

<style scoped>
.back-button {
  display: flex;
  align-items: center;
  font-size: var(--font-size-small);
  gap: 4px;
  margin: 0 0 24px 6px;
}
</style>
