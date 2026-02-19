<template>
  <a
    :href="objectUrl"
    class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-overflow-hidden hover:tw-shadow-md hover:tw-border-[var(--color-primary-organization)] tw-transition-all tw-cursor-pointer tw-group tw-flex tw-items-stretch tw-h-full tw-no-underline tw-text-inherit tw-w-full focus-visible:tw-outline focus-visible:tw-outline-2 focus-visible:tw-outline-offset-2 focus-visible:tw-outline-[var(--color-primary-organization)]"
  >
    <div class="tw-flex tw-w-full">
      <div v-if="objectType === PortalCardObjectType.Map && showThumbnail" class="tw-p-4">
        <div
          class="tw-w-40 tw-h-28 sm:tw-w-48 sm:tw-h-32 tw-bg-gray-100 tw-flex tw-items-center tw-justify-center tw-shrink-0 tw-rounded tw-overflow-hidden"
        >
          <img
            :src="getImageUrl"
            alt="Voorbeeldweergave themakaart"
            class="tw-w-full tw-h-full tw-object-cover group-hover:tw-scale-105 tw-transition-transform tw-duration-300"
          />
        </div>
      </div>
      <div
        v-else
        class="tw-w-12 tw-h-12 tw-bg-gray-50 tw-rounded-xl group-hover:tw-bg-[var(--color-primary-organization)]/10 tw-transition-colors tw-flex tw-items-center tw-justify-center tw-shrink-0 tw-m-6"
      >
        <i
          v-if="objectType === PortalCardObjectType.Map"
          class="pi pi-map tw-text-2xl tw-text-gray-700 group-hover:tw-text-[var(--color-primary-organization)] tw-transition-colors"
          aria-hidden="true"
        ></i>
        <i
          v-else-if="objectType === PortalCardObjectType.Metadataset"
          class="pi pi-database tw-text-2xl tw-text-gray-700 group-hover:tw-text-[var(--color-primary-organization)] tw-transition-colors"
          aria-hidden="true"
        ></i>
        <i
          v-else-if="objectType === PortalCardObjectType.Table"
          class="pi pi-chart-bar tw-text-2xl tw-text-gray-700 group-hover:tw-text-[var(--color-primary-organization)] tw-transition-colors"
          aria-hidden="true"
        ></i>
      </div>
      <div class="tw-flex-1 tw-pr-6 tw-py-6">
        <h3
          class="tw-text-lg sm:tw-text-xl tw-leading-snug tw-my-2 tw-font-medium tw-line-clamp-2 group-hover:tw-text-[var(--color-primary-organization)] tw-transition-colors"
        >
          {{ title }}
        </h3>
        <p v-if="summary" class="tw-text-[var(--color-text-organization)] tw-leading-relaxed tw-line-clamp-2 tw-mt-0">
          {{ summary }}
        </p>
        <div class="tw-flex tw-gap-x-4 tw-flex-wrap">
          <p v-if="category" class="tw-text-[var(--color-text-organization)] tw-text-sm tw-my-1">
            Onderwerp: <span class="tw-font-bold">{{ category }}</span>
          </p>
          <p v-if="formattedLastUpdated" class="tw-text-[var(--color-text-organization)] tw-text-sm tw-my-1">
            Laatst bijgewerkt: <span class="tw-font-bold">{{ formattedLastUpdated }}</span>
          </p>
        </div>
      </div>
    </div>
  </a>
</template>

<script setup lang="ts">
import { usePortalCard, type PortalCardProps, PortalCardObjectType } from "@/portal/components/shared/portalCardShared";

defineOptions({ name: "PortalListCard" });

const props = withDefaults(defineProps<PortalCardProps>(), {
  thumbnail: null,
  summary: null,
  showThumbnail: false,
  lastUpdated: null,
  category: null,
});

const { formattedLastUpdated, getImageUrl } = usePortalCard(props);
</script>
