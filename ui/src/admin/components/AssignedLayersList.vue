<template>
  <div>
    <h2 class="tw-mb-4 tw-mt-8">Toegewezen op kaartlagen</h2>
    <div class="tw-flex tw-gap-4 tw-bg-white tw-p-4 tw-rounded-lg tw-flex-wrap tw-w-full">
      <template v-if="layers && layers.length > 0">
        <router-link
          v-for="layer in layers"
          :key="layer.id"
          :to="`/layers/update/${layer.id}`"
          target="_blank"
          rel="noopener"
          class="tw-flex tw-p-4 tw-rounded-lg tw-gap-2 tw-text-gray-900 tw-no-underline tw-border-solid tw-border-gray-200 tw-border-[1px] hover:tw-bg-gray-100 hover:tw-text-blue-700 tw-transition-colors"
        >
          <div>
            <i class="pi pi-external-link tw-opacity-50"></i>
          </div>
          <span class="tw-font-bold">{{ layer.name }}</span>
        </router-link>
      </template>
      <template v-else>
        <div class="tw-text-gray-500 tw-text-sm tw-py-4 tw-w-full tw-text-center">
          Geen kaartlagen toegewezen aan deze metadataset.
          <div class="tw-mt-4">
            <router-link
              to="/layers"
              class="tw-inline-block tw-p-4 tw-rounded-lg tw-gap-2 tw-text-gray-900 tw-no-underline tw-border-solid tw-border-gray-200 tw-border-[1px] hover:tw-bg-gray-100 hover:tw-text-blue-700 tw-font-bold tw-transition-colors"
              target="_blank"
              rel="noopener"
            >
              <i class="pi pi-external-link tw-opacity-50 tw-mr-2"></i>
              Bekijk kaartlagen
            </router-link>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Layer {
  id: number;
  name: string;
}

interface Props {
  layers: Layer[];
}

defineProps<Props>();
</script>
