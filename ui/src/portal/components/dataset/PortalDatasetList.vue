<template>
  <div class="dataset-container">
    <ul class="dataset-list">
      <li v-for="dataset in datasets" :key="dataset.id">
        <PortalDatasetListItem :dataset="dataset" />
      </li>
    </ul>
  </div>
</template>

<script>
import PortalDatasetListItem from "@/portal/components/dataset/PortalDatasetListItem.vue";

export default {
  name: "PortalDatasetList",
  components: { PortalDatasetListItem },
  props: { datasets: Array },
};
</script>

<style scoped>
.dataset-container {
  display: flex;
  flex-direction: column;
}

.dataset-list > li:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-60);
  margin-bottom: 16px;
}
</style>
