<template>
  <div class="tw-flex tw-flex-col">
    <ul>
      <li
        v-for="metadataset in metadatasets"
        :key="metadataset.id"
        class="tw-pb-4 tw-mb-4 last:tw-pb-0 last:tw-mb-0"
        style="border-bottom: 1px solid var(--color-grey-60);"
      >
        <PortalMetadatasetListItem :metadataset="metadataset" />
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import PortalMetadatasetListItem from "@/portal/components/dataset/PortalMetadatasetListItem.vue";
import { IMetadataset } from "@/types/metadataset";

interface PortalMetadatasetListProps {
  metadatasets: IMetadataset[];
}

defineProps<PortalMetadatasetListProps>();
</script>
