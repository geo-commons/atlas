<template>
  <a
    :href="objectUrl"
    class="card-link tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-overflow-hidden hover:tw-shadow-md hover:tw-border-[var(--color-primary-organization)] tw-transition-all tw-cursor-pointer tw-group tw-block tw-h-full"
  >
    <!-- Map cards with thumbnail -->
    <template v-if="objectType === 'map'">
      <div v-if="showThumbnail" class="tw-relative tw-h-48 tw-bg-gray-100">
        <img
          :src="getImageUrl"
          alt="Voorbeeldweergave themakaart"
          class="tw-w-full tw-h-full tw-object-cover group-hover:tw-scale-105 tw-transition-transform tw-duration-300"
        />
      </div>
      <div
        v-else
        class="tw-h-48 tw-bg-gradient-to-br tw-from-gray-100 tw-to-gray-200 tw-flex tw-items-center tw-justify-center"
      >
        <i class="pi pi-map tw-text-5xl tw-text-gray-400" aria-hidden="true"></i>
      </div>
      <div class="tw-p-6">
        <h3
          class="tw-text-lg tw-leading-snug tw-line-clamp-2 tw-font-medium tw-mb-3 group-hover:tw-text-[var(--color-primary-organization)] tw-transition-colors"
        >
          {{ title }}
        </h3>
        <p v-if="summary" class="tw-text-gray-600 tw-text-sm tw-leading-relaxed tw-line-clamp-2">{{ summary }}</p>
      </div>
    </template>
    <!-- Metadataset and Table cards with icon -->
    <template v-else>
      <div class="tw-p-7 tw-h-full tw-flex tw-flex-col">
        <div class="tw-flex tw-items-start tw-justify-between tw-gap-3 tw-mb-3">
          <div
            class="tw-w-12 tw-h-12 tw-bg-gray-50 tw-rounded-xl group-hover:tw-bg-[var(--color-primary-organization)]/10 tw-transition-colors tw-flex tw-items-center tw-justify-center tw-shrink-0"
          >
            <i
              v-if="objectType === 'metadataset'"
              class="pi pi-database tw-text-gray-700 group-hover:tw-text-[var(--color-primary-organization)] tw-transition-colors tw-text-2xl tw-leading-[1] tw-block"
              aria-hidden="true"
            ></i>
            <i
              v-else-if="objectType === 'table'"
              class="pi pi-chart-bar tw-text-gray-700 group-hover:tw-text-[var(--color-primary-organization)] tw-transition-colors tw-text-2xl tw-leading-[1] tw-block"
              aria-hidden="true"
            ></i>
          </div>
        </div>
        <p v-if="category" class="tw-text-gray-500 tw-text-xs tw-mt-3 tw-uppercase">
          {{ category }}
        </p>
        <h3
          class="tw-text-xl tw-leading-snug tw-mb-2 tw-font-medium tw-line-clamp-2 group-hover:tw-text-[var(--color-primary-organization)] tw-transition-colors"
        >
          {{ title }}
        </h3>
        <p v-if="summary" class="tw-text-gray-600 tw-leading-relaxed tw-line-clamp-3 tw-mt-0">{{ summary }}</p>
        <p v-if="formattedLastUpdated" class="tw-text-gray-500 tw-text-sm tw-mt-auto">
          Laatst bijgewerkt: <span class="tw-font-bold">{{ formattedLastUpdated }}</span>
        </p>
      </div>
    </template>
  </a>
</template>

<script>
import defaultMapsThumbnail from "@/assets/images/default_map_thumbnail.png";
import defaultTableThumbnail from "@/assets/images/default_table_thumbnail.png";
import defaultMetadatasetThumbnail from "@/assets/images/default_dataset_thumbnail.png";

import { formatDateValue } from "@/utils/date-formatter";

export default {
  name: "PortalCard",
  props: {
    thumbnail: String,
    title: String,
    summary: String,
    objectUrl: String,
    objectType: String,
    showThumbnail: {
      default: false,
      type: Boolean,
    },
    lastUpdated: {
      default: null,
      type: [String, Object],
    },
    category: {
      default: null,
      type: String,
    },
  },
  computed: {
    formattedLastUpdated() {
      if (!this.lastUpdated) return null;
      return formatDateValue(this.lastUpdated);
    },
    getImageUrl() {
      if (!this.thumbnail) {
        switch (this.objectType) {
          case "map":
            return defaultMapsThumbnail;
          case "table":
            return defaultTableThumbnail;
          case "metadataset":
            return defaultMetadatasetThumbnail;
        }
      }
      return this.thumbnail;
    },
  },
};
</script>

<style scoped>
.card-link {
  text-decoration: none;
  color: inherit;
  width: 100%;
}

.card-link:focus-visible {
  outline: 2px solid var(--color-primary-organization);
  outline-offset: 2px;
}
</style>
