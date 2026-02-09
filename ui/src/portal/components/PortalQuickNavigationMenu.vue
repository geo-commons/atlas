<template>
  <div>
    <h2 class="tw-text-2xl tw-mb-6">Direct naar</h2>
    <ul class="tw-space-y-2">
      <li>
        <a
          href="/atlas/"
          target="_blank"
          rel="noopener noreferrer"
          class="tw-w-full tw-flex tw-items-center tw-gap-3 tw-px-4 tw-py-3 tw-rounded-xl hover:tw-bg-gray-50 tw-transition-colors tw-group tw-text-left tw-no-underline"
        >
          <i
            class="pi pi-map-marker tw-text-lg tw-text-gray-500 group-hover:tw-text-[var(--color-primary-organization)] tw-transition-colors"
            aria-hidden="true"
          ></i>
          <span class="tw-text-gray-700 group-hover:tw-text-gray-900 tw-font-medium">Hoofdkaart</span>
        </a>
      </li>
      <li v-if="availableLinks.maps">
        <a
          href="/maps"
          class="tw-w-full tw-flex tw-items-center tw-gap-3 tw-px-4 tw-py-3 tw-rounded-xl hover:tw-bg-gray-50 tw-transition-colors tw-group tw-text-left tw-no-underline"
        >
          <i
            class="pi pi-map tw-text-lg tw-text-gray-500 group-hover:tw-text-[var(--color-primary-organization)] tw-transition-colors"
            aria-hidden="true"
          ></i>
          <span class="tw-text-gray-700 group-hover:tw-text-gray-900 tw-font-medium">Alle kaarten</span>
        </a>
      </li>
      <li v-if="availableLinks.metadatasets">
        <a
          href="/metadatasets"
          class="tw-w-full tw-flex tw-items-center tw-gap-3 tw-px-4 tw-py-3 tw-rounded-xl hover:tw-bg-gray-50 tw-transition-colors tw-group tw-text-left tw-no-underline"
        >
          <i
            class="pi pi-database tw-text-lg tw-text-gray-500 group-hover:tw-text-[var(--color-primary-organization)] tw-transition-colors"
            aria-hidden="true"
          ></i>
          <span class="tw-text-gray-700 group-hover:tw-text-gray-900 tw-font-medium">Alle metadatasets</span>
        </a>
      </li>
      <li v-if="availableLinks.tables">
        <a
          href="/tables"
          class="tw-w-full tw-flex tw-items-center tw-gap-3 tw-px-4 tw-py-3 tw-rounded-xl hover:tw-bg-gray-50 tw-transition-colors tw-group tw-text-left tw-no-underline"
        >
          <i
            class="pi pi-table tw-text-lg tw-text-gray-500 group-hover:tw-text-[var(--color-primary-organization)] tw-transition-colors"
            aria-hidden="true"
          ></i>
          <span class="tw-text-gray-700 group-hover:tw-text-gray-900 tw-font-medium">Alle tabellen</span>
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "PortalQuickNavigationMenu",
  props: {
    availableLinks: {
      type: Object,
      default: () => {
        return {
          maps: false,
          tables: false,
          metadatasets: false,
        };
      },
    },
  },
};
</script>
