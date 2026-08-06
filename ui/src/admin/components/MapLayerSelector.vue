<template>
  <div class="tw-flex tw-flex-col">
    <div class="tw-py-4 tw-flex tw-flex-row tw-items-center tw-justify-between tw-gap-2">
      <label class="tw-font-bold">Beschikbare kaartlagen</label>
      <div class="tw-flex tw-gap-1">
        <Button
          v-tippy="{ placement: 'bottom' }"
          text
          severity="secondary"
          type="button"
          :aria-label="
            isToggleCategoriesOpen ? 'Alle beschikbare kaartlagen inklappen' : 'Alle beschikbare kaartlagen uitklappen'
          "
          :content="isToggleCategoriesOpen ? 'Alles inklappen' : 'Alles uitklappen'"
          :disabled="layers.length === 0"
          @click="toggleCategories"
        >
          <i
            class="pi pi-chevron-down tw-transition-transform tw-duration-200"
            :class="{ 'tw-rotate-180': isToggleCategoriesOpen }"
          />
        </Button>
      </div>
    </div>

    <IconField class="tw-mb-4">
      <InputIcon class="pi pi-search" />
      <InputText v-model="searchQuery" placeholder="Zoek kaartlaag" fluid />
      <InputIcon v-if="searchQuery" class="cursor-pointer pi pi-times" @click="searchQuery = ''" />
    </IconField>

    <div class="tw-flex tw-flex-col tw-gap-4">
      <MapCategory
        v-for="category in displayedCategoryTree"
        :key="category.id"
        :category="category"
        :is-open="!closedCategoryIds.has(category.id)"
        @toggle-open="handleCategoryToggle"
      >
        <MapLayerItem
          v-for="layer in category.layers"
          :key="layer.id"
          :layer="layer"
          :is-layer-visible="false"
          :select-layer="selectLayer"
        />
        <MapCategory
          v-for="subCategory in category.subcategories"
          :key="subCategory.id"
          :category="subCategory"
          :is-open="!closedCategoryIds.has(subCategory.id)"
          @toggle-open="handleCategoryToggle"
        >
          <MapLayerItem
            v-for="layer in subCategory.layers"
            :key="layer.id"
            :layer="layer"
            :is-layer-visible="false"
            :select-layer="selectLayer"
          />
        </MapCategory>
      </MapCategory>

      <Message v-if="searchQuery.trim() && displayedCategoryTree.length === 0" severity="info">
        Geen kaartlagen gevonden.
      </Message>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";

import MapCategory from "./MapCategory.vue";
import MapLayerItem from "./MapLayerItem.vue";
import { buildCategoryTree, matchesLayerSearch } from "@/utils/map-layer-tree";

import type { IAdminLayer, IMapCategoryConfig } from "@/types/map-layer-tree";
import type { ICategory } from "@/types/category";

const { layers, categories, mapCategories, selectLayer } = defineProps<{
  layers: IAdminLayer[];
  categories: ICategory[];
  mapCategories: IMapCategoryConfig[];
  selectLayer: (layer: IAdminLayer) => void;
}>();

const searchQuery = ref<string>("");
const closedCategoryIds = ref<Set<string>>(new Set());

watch(searchQuery, () => {
  closedCategoryIds.value = new Set();
});

const visibleLayers = computed(() => {
  if (!searchQuery.value) {
    return layers;
  }

  const searchTerm = searchQuery.value.trim().toLowerCase();
  return layers.filter((layer) => matchesLayerSearch(layer, searchTerm));
});

const displayedCategoryTree = computed(() => {
  return buildCategoryTree(visibleLayers.value, categories, mapCategories);
});

const displayedCategoryIds = computed(() => {
  return displayedCategoryTree.value.flatMap((category) => [
    category.id,
    ...category.subcategories.map((subcategory) => subcategory.id),
  ]);
});

const isToggleCategoriesOpen = computed(() => {
  return displayedCategoryIds.value.some((categoryId) => !closedCategoryIds.value.has(categoryId));
});

const toggleCategories = (): void => {
  if (isToggleCategoriesOpen.value) {
    closedCategoryIds.value = new Set(displayedCategoryIds.value);
    return;
  }

  closedCategoryIds.value = new Set();
};

const handleCategoryToggle = (categoryId: string, categoryIsOpen: boolean): void => {
  const nextClosedCategoryIds = new Set(closedCategoryIds.value);

  if (categoryIsOpen) {
    nextClosedCategoryIds.delete(categoryId);
  } else {
    nextClosedCategoryIds.add(categoryId);
  }

  closedCategoryIds.value = nextClosedCategoryIds;
};
</script>
