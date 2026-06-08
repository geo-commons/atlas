<template>
  <div class="tw-flex tw-flex-col tw-gap-4">
    <IconField>
      <InputIcon class="pi pi-search" />
      <InputText v-model="searchQuery" placeholder="Zoek kaartlaag" fluid />
    </IconField>

    <div class="tw-flex tw-flex-col tw-gap-4">
      <MapCategory v-for="category in displayedCategoryTree" :key="category.id" :category="category">
        <MapLayerItem
          v-for="layer in category.layers"
          :key="layer.id"
          :layer="layer"
          :is-layer-visible="false"
          :select-layer="selectLayer"
        />
        <MapCategory v-for="subCategory in category.subcategories" :key="subCategory.id" :category="subCategory">
          <MapLayerItem
            v-for="layer in subCategory.layers"
            :key="layer.id"
            :layer="layer"
            :is-layer-visible="false"
            :select-layer="selectLayer"
          />
        </MapCategory>
      </MapCategory>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";

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
</script>
