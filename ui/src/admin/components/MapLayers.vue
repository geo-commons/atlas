<template>
  <AdminSidePanel :loading="loading">
    <template #header>
      <button
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton __normal __outline"
        type="button"
        aria-label="Ga terug"
        content="Terug"
        @click="back()"
      >
        <ArrowLeftIcon class="icon" />
      </button>
      <h1 class="layers-header">
        <LayerIcon class="icon" />
        Lagen
      </h1>
    </template>
    <template #default>
      <div class="tw-px-4">
        <div class="tw-py-4 tw-flex tw-flex-col tw-gap-4">
          <label class="tw-font-bold">Geselecteerde basislagen</label>
          <Message v-if="hasMultipleBaseLayersVisible" severity="error"
            >Let op: er zijn twee basis lagen die standaard zichtbaar zijn.</Message
          >
        </div>
        <div class="tw-flex tw-flex-col tw-gap-2">
          <MapLayerItem
            v-for="selectedLayer in selectedBaseLayers"
            :key="selectedLayer.id"
            :layer="selectedLayer"
            :open-layer-settings="toggleLayerSettings"
            :is-layer-visible="isLayerVisible(selectedLayer)"
          />
        </div>

        <div class="tw-py-4 tw-flex tw-flex-row tw-items-center tw-justify-between tw-gap-2">
          <label class="tw-font-bold">Geselecteerde kaartlagen</label>
          <div class="tw-flex tw-gap-1">
            <Button
              v-tippy="{ placement: 'bottom' }"
              text
              severity="secondary"
              type="button"
              :aria-label="
                isToggleCategoriesOpen
                  ? 'Alle geselecteerde kaartlagen inklappen'
                  : 'Alle geselecteerde kaartlagen verbergen'
              "
              :content="isToggleCategoriesOpen ? 'Alles inklappen' : 'Alles uitklappen'"
              :disabled="selectedCategoryTree.length === 0"
              @click="toggleCategories"
            >
              <i
                class="pi pi-chevron-down tw-transition-transform tw-duration-200"
                :class="{ 'tw-rotate-180': isToggleCategoriesOpen }"
              />
            </Button>
          </div>
        </div>

        <IconField v-if="!isChangingOrder" class="tw-mb-4">
          <InputIcon class="pi pi-search" />
          <InputText v-model="selectedLayerSearchQuery" placeholder="Zoek kaartlaag" fluid />
          <InputIcon
            v-if="selectedLayerSearchQuery"
            class="cursor-pointer pi pi-times"
            @click="selectedLayerSearchQuery = ''"
          />
        </IconField>

        <div class="tw-flex tw-flex-col tw-gap-4">
          <DragDropProvider v-if="isChangingOrder" @drag-over="handleDragOver" @drag-end="handleDragEnd">
            <SortMapCategory
              v-for="(category, categoryIndex) in selectedCategoryTree"
              :key="category.id"
              :category="{ category: category.id }"
              :index="categoryIndex"
              group="category"
              :show-drag-handle="selectedCategoryTree.length > 1"
            >
              <MapCategory
                :category="category"
                :is-open="isSelectedCategoryOpen(category.id)"
                @toggle-open="handleCategoryToggle"
              >
                <SortMapLayer
                  v-for="(selectedLayer, layerIndex) in category.layers"
                  :key="selectedLayer.id"
                  :layer="selectedLayer"
                  :index="layerIndex"
                  :group="layerGroupForNode(category.id)"
                  :category-id="category.id"
                  :show-drag-handle="category.layers.length > 1"
                >
                  <div class="tw-flex-1">
                    <MapLayerItem
                      :layer="selectedLayer"
                      :open-layer-settings="toggleLayerSettings"
                      :is-layer-visible="isLayerVisible(selectedLayer)"
                      :deselect-layer="deselectLayer"
                      :is-changing-order="isChangingOrder"
                    />
                  </div>
                </SortMapLayer>

                <SortMapCategory
                  v-for="(subCategory, subcategoryIndex) in category.subcategories"
                  :key="subCategory.id"
                  :category="{ category: subCategory.id }"
                  :index="subcategoryIndex"
                  :group="subcategoryGroupForCategory(category.id)"
                  :parent-category-id="category.id"
                  :show-drag-handle="category.subcategories.length > 1"
                >
                  <MapCategory
                    :category="subCategory"
                    :is-open="isSelectedCategoryOpen(subCategory.id)"
                    @toggle-open="handleCategoryToggle"
                  >
                    <SortMapLayer
                      v-for="(selectedLayer, layerIndex) in subCategory.layers"
                      :key="selectedLayer.id"
                      :layer="selectedLayer"
                      :index="layerIndex"
                      :group="layerGroupForNode(subCategory.id)"
                      :category-id="subCategory.id"
                      :parent-category-id="category.id"
                      :show-drag-handle="subCategory.layers.length > 1"
                    >
                      <div class="tw-flex-1">
                        <MapLayerItem
                          :layer="selectedLayer"
                          :open-layer-settings="toggleLayerSettings"
                          :is-layer-visible="isLayerVisible(selectedLayer)"
                          :deselect-layer="deselectLayer"
                          :is-changing-order="isChangingOrder"
                        />
                      </div>
                    </SortMapLayer>
                  </MapCategory>
                </SortMapCategory>
              </MapCategory>
            </SortMapCategory>
          </DragDropProvider>

          <template v-else>
            <MapCategory
              v-for="category in displayedSelectedCategoryTree"
              :key="category.id"
              :category="category"
              :is-open="isSelectedCategoryOpen(category.id)"
              @toggle-open="handleCategoryToggle"
            >
              <MapLayerItem
                v-for="selectedLayer in category.layers"
                :key="selectedLayer.id"
                :layer="selectedLayer"
                :open-layer-settings="toggleLayerSettings"
                :is-layer-visible="isLayerVisible(selectedLayer)"
                :deselect-layer="deselectLayer"
              />
              <MapCategory
                v-for="subCategory in category.subcategories"
                :key="subCategory.id"
                :category="subCategory"
                :is-open="isSelectedCategoryOpen(subCategory.id)"
                @toggle-open="handleCategoryToggle"
              >
                <MapLayerItem
                  v-for="selectedLayer in subCategory.layers"
                  :key="selectedLayer.id"
                  :layer="selectedLayer"
                  :open-layer-settings="toggleLayerSettings"
                  :is-layer-visible="isLayerVisible(selectedLayer)"
                  :deselect-layer="deselectLayer"
                />
              </MapCategory>
            </MapCategory>
          </template>

          <Message v-if="selectedLayerSearchQuery.trim() && displayedSelectedCategoryTree.length === 0" severity="info">
            Geen kaartlagen gevonden.
          </Message>
        </div>

        <MapLayerSelector
          v-if="!isChangingOrder"
          :layers="unselectedLayers"
          :categories="allCategories"
          :map-categories="[]"
          :select-layer="selectLayer"
        />
      </div>
    </template>
    <template #footer>
      <div class="tw-flex tw-flex-col tw-gap-2">
        <Button :outlined="!isChangingOrder" :loading="isSavingOrder" fluid @click="toggleChangingOrder">{{
          isChangingOrder ? "Volgorde opslaan" : "Volgorde aanpassen"
        }}</Button>
      </div>
    </template>
  </AdminSidePanel>
</template>

<script setup lang="ts">
import Cookies from "js-cookie";
import ArrowLeftIcon from "../../assets/icons/arrow-left-icon.svg";
import LayerIcon from "../../assets/icons/layer-icon.svg";
import AdminSidePanel from "@/admin/components/AdminSidePanel.vue";
import { arrayMove } from "@dnd-kit/helpers";
import { DragDropProvider, type DragEndEvent, type DragOverEvent } from "@dnd-kit/vue";
import { isSortable } from "@dnd-kit/vue/sortable";
import { getAllObjects } from "@/utils/api-helpers";
import MapLayerItem from "./MapLayerItem.vue";
import MapCategory from "./MapCategory.vue";
import MapLayerSelector from "./MapLayerSelector.vue";
import { computed, onMounted, ref, watch } from "vue";

import type {
  CategoryId,
  IAdminLayer,
  ICategoryTreeNode,
  IMapCategoryConfig,
  IMapLayerConfig,
  IMapLayersData,
  LayerId,
} from "@/types/map-layer-tree";
import type { ICategory } from "@/types/category";
import {
  addLayerToCategoryTree,
  buildCategoryTree,
  getTreeLayerId,
  isBaseLayerConfig,
  matchesLayerSearch,
  removeBaseLayersFromCategoryTree,
  removeLayerFromCategoryTree,
} from "@/utils/map-layer-tree";
import SortMapLayer from "./SortMapLayer.vue";
import SortMapCategory from "./SortMapCategory.vue";
import { useToast } from "primevue";

type MapId = number | string;

interface IMapLayersState extends IMapLayersData {
  id?: MapId;
}

interface ISortableItemData {
  type: "category" | "subcategory" | "category-layer" | "subcategory-layer";
  categoryId?: CategoryId;
  parentCategoryId?: CategoryId;
}

const props = defineProps<{
  initialData: IMapLayersState;
}>();

const emit = defineEmits<{
  (e: "update-layer-config", config: { layers: IMapLayerConfig[]; categories: IMapCategoryConfig[] }): void;
  (e: "show-form"): void;
  (e: "show-layer", layerId: LayerId): void;
}>();

const allLayers = ref<IAdminLayer[]>([]);
const allCategories = ref<ICategory[]>([]);
const selectedMapLayerConfigs = ref<IMapLayerConfig[]>([]);
const loading = ref<boolean>(false);
const isChangingOrder = ref<boolean>(false);
const isSavingOrder = ref<boolean>(false);
const selectedCategoryTree = ref<ICategoryTreeNode[]>([]);
const selectedLayerSearchQuery = ref<string>("");
const closedCategoryIds = ref<Set<CategoryId>>(new Set());
const data = ref<IMapLayersState>({
  layers: [],
  categories: [],
});

const toast = useToast();

watch(selectedLayerSearchQuery, () => {
  closedCategoryIds.value = new Set();
});

const toggleCategories = (): void => {
  if (isToggleCategoriesOpen.value) {
    closedCategoryIds.value = new Set(displayedCategoryIds.value);
    return;
  }

  closedCategoryIds.value = new Set();
};

const layerById = computed(() => {
  return new Map<LayerId, IAdminLayer>(allLayers.value.map((layer) => [layer.id, layer]));
});

const unselectedLayers = computed(() => {
  return allLayers.value.filter((layer) => !selectedLayerIds.value.has(layer.id));
});

const selectedLayerIds = computed(() => {
  return new Set<LayerId>([
    ...selectedMapLayerConfigs.value.filter(isBaseLayerConfig).map((selectedLayer) => selectedLayer.layer),
    ...selectedCategoryTree.value.flatMap((category) => [
      ...category.layers.map(getTreeLayerId),
      ...category.subcategories.flatMap((subcategory) => subcategory.layers.map(getTreeLayerId)),
    ]),
  ]);
});

const selectedBaseLayers = computed(() => {
  return selectedMapLayerConfigs.value
    .map((config) => layerById.value.get(config.layer))
    .filter(
      (layerData, index): layerData is IAdminLayer =>
        Boolean(layerData) && isBaseLayerConfig(selectedMapLayerConfigs.value[index]),
    );
});

const hasMultipleBaseLayersVisible = computed(() => {
  return (
    selectedMapLayerConfigs.value.filter((layerConfig) => {
      if (layerConfig.settings.is_base && layerConfig.settings.is_visible) {
        return layerConfig;
      }

      return false;
    }).length > 1
  );
});

onMounted(async () => {
  loading.value = true;

  try {
    await Promise.all([getLayers(), getCategories()]);
    rebuildSelectedCategoryTree();
    removeSelectedBaseLayersFromTree(true);
  } finally {
    loading.value = false;
  }
});

const getSelectedRegularLayers = (): IAdminLayer[] => {
  return selectedMapLayerConfigs.value
    .map((config) => layerById.value.get(config.layer))
    .filter(
      (layerData, index): layerData is IAdminLayer =>
        Boolean(layerData) && !isBaseLayerConfig(selectedMapLayerConfigs.value[index]),
    );
};

const getOrderingByLayerId = (): Map<LayerId, number> => {
  return new Map(
    selectedMapLayerConfigs.value
      .filter((config) => config.ordering !== undefined)
      .map((config) => [config.layer, config.ordering as number]),
  );
};

const visibleSelectedLayers = computed(() => {
  const searchTerm = selectedLayerSearchQuery.value.trim().toLowerCase();
  const selectedLayers = getSelectedRegularLayers();

  if (!searchTerm) {
    return selectedLayers;
  }

  return selectedLayers.filter((layer) => matchesLayerSearch(layer, searchTerm));
});

const displayedSelectedCategoryTree = computed(() => {
  if (!selectedLayerSearchQuery.value.trim()) {
    return selectedCategoryTree.value;
  }

  return buildCategoryTree(
    visibleSelectedLayers.value,
    allCategories.value,
    data.value.categories || [],
    getOrderingByLayerId(),
  );
});

const getCategoryIdsFromTree = (categoryTree: ICategoryTreeNode[]): CategoryId[] => {
  return categoryTree.flatMap((category) => [
    category.id,
    ...category.subcategories.map((subcategory) => subcategory.id),
  ]);
};

const displayedCategoryIds = computed(() => {
  return getCategoryIdsFromTree(
    isChangingOrder.value ? selectedCategoryTree.value : displayedSelectedCategoryTree.value,
  );
});

const isSelectedCategoryOpen = (categoryId: CategoryId): boolean => {
  return !closedCategoryIds.value.has(categoryId);
};

const isToggleCategoriesOpen = computed(() => {
  return displayedCategoryIds.value.some((categoryId) => isSelectedCategoryOpen(categoryId));
});

const handleCategoryToggle = (categoryId: CategoryId, isOpen: boolean): void => {
  const nextClosedCategoryIds = new Set(closedCategoryIds.value);

  if (isOpen) {
    nextClosedCategoryIds.delete(categoryId);
  } else {
    nextClosedCategoryIds.add(categoryId);
  }

  closedCategoryIds.value = nextClosedCategoryIds;
};

const rebuildSelectedCategoryTree = (): void => {
  selectedCategoryTree.value = buildCategoryTree(
    getSelectedRegularLayers(),
    allCategories.value,
    data.value.categories || [],
    getOrderingByLayerId(),
  );
};

const getExistingMapCategoryConfig = (categoryId: CategoryId): IMapCategoryConfig | undefined => {
  return (data.value.categories || []).find((category) => category.category === categoryId);
};

const getCategoryConfigsFromTree = (categoryTree: ICategoryTreeNode[]): IMapCategoryConfig[] => {
  return categoryTree.flatMap((category) => {
    const existingCategory = getExistingMapCategoryConfig(category.id);
    const categoryConfig: IMapCategoryConfig = {
      ...existingCategory,
      category: category.id,
      title: category.title,
      ordering: category.ordering,
    };

    return [
      categoryConfig,
      ...category.subcategories.map((subcategory) => {
        const existingSubcategory = getExistingMapCategoryConfig(subcategory.id);
        return {
          ...existingSubcategory,
          category: subcategory.id,
          title: subcategory.title,
          ordering: subcategory.ordering,
        };
      }),
    ];
  });
};

const getLayerOrderingFromTree = (categoryTree: ICategoryTreeNode[]): Map<LayerId, number> => {
  const orderingByLayerId = new Map<LayerId, number>();

  categoryTree.forEach((category) => {
    category.layers.forEach((layer) => orderingByLayerId.set(getTreeLayerId(layer), layer.ordering ?? 0));
    category.subcategories.forEach((subcategory) => {
      subcategory.layers.forEach((layer) => orderingByLayerId.set(getTreeLayerId(layer), layer.ordering ?? 0));
    });
  });

  return orderingByLayerId;
};

const getLayerConfigsFromTree = (categoryTree: ICategoryTreeNode[]): IMapLayerConfig[] => {
  const orderingByLayerId = getLayerOrderingFromTree(categoryTree);

  return selectedMapLayerConfigs.value.map((config) => ({
    ...config,
    ordering: orderingByLayerId.get(config.layer) ?? config.ordering ?? 0,
  }));
};

const emitLayerConfig = (categoryTree: ICategoryTreeNode[]): void => {
  const categories = getCategoryConfigsFromTree(categoryTree);
  const layers = getLayerConfigsFromTree(categoryTree);
  data.value.categories = categories;
  selectedMapLayerConfigs.value = layers;
  emit("update-layer-config", { layers, categories });
};

watch(
  () => props.initialData,
  (newInitialData) => {
    if (!newInitialData) {
      return;
    }

    data.value = {
      ...newInitialData,
      categories: newInitialData.categories || [],
    };
    selectedMapLayerConfigs.value = [...(newInitialData.layers || [])];
    rebuildSelectedCategoryTree();
  },
  {
    immediate: true,
    deep: true,
  },
);

const removeSelectedBaseLayersFromTree = (shouldEmit: boolean): void => {
  const normalizedTree = removeBaseLayersFromCategoryTree(selectedCategoryTree.value, selectedMapLayerConfigs.value);

  if (JSON.stringify(normalizedTree) === JSON.stringify(selectedCategoryTree.value)) {
    return;
  }

  selectedCategoryTree.value = normalizedTree;

  if (shouldEmit) {
    emitLayerConfig(normalizedTree);
  }
};

watch(selectedMapLayerConfigs, () => removeSelectedBaseLayersFromTree(true), { deep: true });

const getLayers = async (): Promise<void> => {
  const url = getAllObjects("/atlas/api/v1/layers/");
  const result = await fetch(url, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch layers");
  }

  const response = await result.json();
  allLayers.value = response.results;
};

const getCategories = async (): Promise<void> => {
  const url = getAllObjects("/atlas/api/v1/categories/");
  const result = await fetch(url, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });

  if (!result.ok) {
    console.error("Could not fetch categories");
  }

  const response = await result.json();
  allCategories.value = response.results;
};

const reorderItems = <T,>(items: T[], fromIndex: number, toIndex: number): T[] => {
  if (fromIndex === toIndex || fromIndex < 0 || toIndex < 0 || fromIndex >= items.length || toIndex >= items.length) {
    return items;
  }

  return arrayMove(items, fromIndex, toIndex);
};

const layerGroupForNode = (categoryId: CategoryId): string => {
  return `map-layers-${categoryId}`;
};

const subcategoryGroupForCategory = (categoryId: CategoryId): string => {
  return `map-subcategories-${categoryId}`;
};

const reorderCategories = (fromIndex: number, toIndex: number): void => {
  selectedCategoryTree.value = reorderItems(selectedCategoryTree.value, fromIndex, toIndex);
  emitLayerConfig(normalizeEditableTree(selectedCategoryTree.value));
};

const reorderSubcategories = (categoryId: CategoryId, fromIndex: number, toIndex: number): void => {
  selectedCategoryTree.value = selectedCategoryTree.value.map((category) => {
    if (category.id !== categoryId) {
      return category;
    }

    return {
      ...category,
      subcategories: reorderItems(category.subcategories, fromIndex, toIndex),
    };
  });
  emitLayerConfig(normalizeEditableTree(selectedCategoryTree.value));
};

const reorderCategoryLayers = (categoryId: CategoryId, fromIndex: number, toIndex: number): void => {
  selectedCategoryTree.value = selectedCategoryTree.value.map((category) => {
    if (category.id !== categoryId) {
      return category;
    }

    return {
      ...category,
      layers: reorderItems(category.layers, fromIndex, toIndex),
    };
  });
  emitLayerConfig(normalizeEditableTree(selectedCategoryTree.value));
};

const reorderSubcategoryLayers = (
  categoryId: CategoryId,
  subcategoryId: CategoryId,
  fromIndex: number,
  toIndex: number,
): void => {
  selectedCategoryTree.value = selectedCategoryTree.value.map((category) => {
    if (category.id !== categoryId) {
      return category;
    }

    return {
      ...category,
      subcategories: category.subcategories.map((subcategory) => {
        if (subcategory.id !== subcategoryId) {
          return subcategory;
        }

        return {
          ...subcategory,
          layers: reorderItems(subcategory.layers, fromIndex, toIndex),
        };
      }),
    };
  });
  emitLayerConfig(normalizeEditableTree(selectedCategoryTree.value));
};

const getSortableData = (data: unknown): ISortableItemData | null => {
  if (!data || typeof data !== "object" || !("type" in data)) {
    return null;
  }

  const sortableData = data as Partial<ISortableItemData>;
  if (
    sortableData.type !== "category" &&
    sortableData.type !== "subcategory" &&
    sortableData.type !== "category-layer" &&
    sortableData.type !== "subcategory-layer"
  ) {
    return null;
  }

  return sortableData as ISortableItemData;
};

const handleDragEnd = (event: DragEndEvent): void => {
  if (event.canceled || !isSortable(event.operation.source)) {
    return;
  }

  const { initialIndex, index } = event.operation.source;
  const { initialGroup, group } = event.operation.source;
  if (initialIndex === index || initialGroup !== group) {
    return;
  }

  const sortableData = getSortableData(event.operation.source.data);
  if (!sortableData) {
    return;
  }

  if (sortableData.type === "category") {
    reorderCategories(initialIndex, index);
    return;
  }

  if (sortableData.type === "subcategory" && sortableData.categoryId !== undefined) {
    reorderSubcategories(sortableData.categoryId, initialIndex, index);
    return;
  }

  if (sortableData.type === "category-layer" && sortableData.categoryId !== undefined) {
    reorderCategoryLayers(sortableData.categoryId, initialIndex, index);
    return;
  }

  if (
    sortableData.type === "subcategory-layer" &&
    sortableData.parentCategoryId !== undefined &&
    sortableData.categoryId !== undefined
  ) {
    reorderSubcategoryLayers(sortableData.parentCategoryId, sortableData.categoryId, initialIndex, index);
  }
};

const handleDragOver = (event: DragOverEvent): void => {
  const { source, target } = event.operation;

  if (!isSortable(source) || !isSortable(target)) {
    return;
  }

  if (source.initialGroup !== target.group) {
    event.preventDefault();
  }
};

const normalizeEditableTree = (categoryTree: ICategoryTreeNode[]): ICategoryTreeNode[] => {
  return categoryTree.map((category, categoryIndex) => ({
    ...category,
    ordering: categoryIndex,
    layers: category.layers.map((layer, layerIndex) => ({
      ...layer,
      ordering: layerIndex,
    })),
    subcategories: category.subcategories.map((subcategory, subcategoryIndex) => ({
      ...subcategory,
      ordering: subcategoryIndex,
      layers: subcategory.layers.map((layer, layerIndex) => ({
        ...layer,
        ordering: layerIndex,
      })),
    })),
  }));
};

const startChangingOrder = (): void => {
  isChangingOrder.value = true;
};

const saveChangingOrder = async (): Promise<void> => {
  removeSelectedBaseLayersFromTree(false);
  const normalizedTree = normalizeEditableTree(selectedCategoryTree.value);

  isSavingOrder.value = true;

  try {
    if (data.value.id !== undefined && data.value.id !== null) {
      const categories = getCategoryConfigsFromTree(normalizedTree);
      const layers = getLayerConfigsFromTree(normalizedTree);
      const response = await fetch(`/atlas/api/v1/maps/${data.value.id}/`, {
        method: "PATCH",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken") || "",
        },
        body: JSON.stringify({ layers, categories }),
      });

      if (response.ok) {
        toast.add({
          severity: "success",
          summary: "Kaartvolgorde succesvol opgeslagen",
          detail: "De kaartvolgorde is succesvol opgeslagen",
          life: 5000,
        });
      }

      if (!response.ok) {
        toast.add({
          severity: "error",
          summary: "Kaartvolgorde opslaan mislukt",
          detail: "Er is een fout opgetreden bij het opslaan van de kaartvolgorde",
          life: 5000,
        });
        return;
      }
    }

    selectedCategoryTree.value = normalizedTree;
    emitLayerConfig(normalizedTree);
    isChangingOrder.value = false;
  } finally {
    isSavingOrder.value = false;
  }
};

const selectLayer = (layer: IAdminLayer): void => {
  if (isChangingOrder.value) {
    return;
  }

  const layerCategory = layer.category;
  if (!layerCategory) {
    return;
  }

  if (!selectedMapLayerConfigs.value.some((selectedLayer) => selectedLayer.layer === layer.id)) {
    selectedMapLayerConfigs.value = [
      ...selectedMapLayerConfigs.value,
      {
        layer: layer.id,
        settings: { customSettings: false, is_base: false, is_visible: false },
        ordering: 0,
      },
    ];
  }

  selectedCategoryTree.value = addLayerToCategoryTree(selectedCategoryTree.value, allCategories.value, layer);
  emitLayerConfig(normalizeEditableTree(selectedCategoryTree.value));
};

const deselectLayer = (layer: IAdminLayer): void => {
  if (isChangingOrder.value) {
    return;
  }

  selectedMapLayerConfigs.value = selectedMapLayerConfigs.value.filter(
    (selectedLayer) => selectedLayer.layer !== layer.id,
  );
  selectedCategoryTree.value = removeLayerFromCategoryTree(selectedCategoryTree.value, getTreeLayerId(layer));
  emitLayerConfig(normalizeEditableTree(selectedCategoryTree.value));
};

const back = (): void => {
  emit("show-form");
};

const toggleLayerSettings = (layerId: LayerId): void => {
  if (isChangingOrder.value) {
    return;
  }

  emit("show-layer", layerId);
};

const isLayerVisible = (layer: IAdminLayer): boolean => {
  const layerConfig = selectedMapLayerConfigs.value.find((selectedLayer) => selectedLayer.layer === layer.id);

  return Boolean(layerConfig?.settings.is_visible);
};

const toggleChangingOrder = async (): Promise<void> => {
  if (isSavingOrder.value) {
    isChangingOrder.value = false;
    return;
  }

  if (!isChangingOrder.value) {
    startChangingOrder();
    return;
  }

  await saveChangingOrder();
};
</script>
