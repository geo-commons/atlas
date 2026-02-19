<template>
  <router-link
    :to="{ name: 'metadataset-details', params: { slug: metadataset.slug } }"
    class="tw-flex tw-flex-col tw-w-full tw-group tw-no-underline tw-text-black tw-p-0 hover:tw-cursor-pointer focus:tw-outline-2 focus:tw-outline-primary focus:tw-outline-offset-2"
    type="link"
    aria-label="Bekijk metadataset"
  >
    <h2
      class="tw-mb-0 tw-text-lg tw-text-primary-organization lg:tw-text-xl group-hover:tw-underline group-focus:tw-underline lg:tw-m-0"
    >
      {{ metadataset.title }}
    </h2>
    <div v-if="metadataset.last_updated" class="tw-text-[var(--color-text-organization)] tw-text-sm">
      Laatst bijgewerkt: {{ formatDateValue(metadataset.last_updated) }}
    </div>
    <p v-if="metadataset.abstract">{{ metadataset.abstract }}</p>

    <div v-if="metadataset.topic_category" class="tw-mb-6">
      <span class="tw-bg-gray-100 tw-px-3 tw-py-2 tw-text-sm">
        {{ getTopicCategoryLabel(metadataset.topic_category) }}
      </span>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { IMetadataset } from "@/types/metadataset";
import { TopicCategoryId, topicCategoryLabels } from "@/types/TopicCategory";
import { formatDateValue } from "@/utils/date-formatter";

interface PortalMetadatasetListItemProps {
  metadataset: IMetadataset;
}

defineProps<PortalMetadatasetListItemProps>();

const getTopicCategoryLabel = (topicId: string): string => {
  return topicCategoryLabels[topicId as TopicCategoryId] || topicId;
};
</script>
