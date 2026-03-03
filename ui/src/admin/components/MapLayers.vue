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
      <ConfirmPopup group="templating">
        <template #message="slotProps">
          <div class="tw-px-4">
            <i :class="slotProps.message.icon" class=""></i>
            <p>{{ slotProps.message.message }}</p>
          </div>
        </template>
      </ConfirmPopup>
      <div>
        <div class="selected-layer-header-wrapper">
          <label class="setting-label">
            <MapIcon />
            Basis lagen</label
          >
          <div v-if="hasMultipleBaseLayersVisible" class="base-layer-warning">
            Let op: er zijn twee basis lagen die standaard zichtbaar zijn
          </div>
        </div>
        <ul class="settings">
          <li v-for="selectedLayer in selectedBaseLayers" :key="selectedLayer.layer" class="setting">
            <button
              type="button"
              class="button __chevron __no-hover layer-button"
              @click="toggleLayerSettings(selectedLayer)"
            >
              <span>
                {{ selectedLayer.title }}
              </span>
              <ViewIcon
                v-if="isLayerVisible(selectedLayer)"
                v-tippy
                content="Standaard zichtbaar"
                class="icon __smedium reset-transform"
              />
              <ChevronRightIcon class="icon setting-chevron" />
            </button>
            <button
              v-tippy="{ placement: 'bottom' }"
              class="iconbutton __normal __transparent-bg __no-hover"
              type="button"
              aria-label="Verwijder laag"
              content="Verwijder"
              @click="confirmDeselect($event, selectedLayer)"
            >
              <RemoveLayerIcon class="icon" />
            </button>
          </li>
        </ul>
        <div class="selected-layer-header-wrapper">
          <label class="setting-label">
            <LayerIcon class="icon" />
            Kaartlagen</label
          >
        </div>
        <DnDProvider>
          <ul class="tw-pl-2">
            <li v-for="(mapCategory, categoryIndex) in data.categories" :key="mapCategory.category">
              <MapLayersTreeCategoryRow
                :category="mapCategory"
                :index="categoryIndex"
                :categories="data.categories"
                :is-target="isCategoryTarget(categoryIndex)"
                @reorder="handleCategoryDropReorder"
                @drag-start="handleCategoryDragStart"
                @drag-hover="handleCategoryDragHover"
                @drag-end="handleCategoryDragEnd"
              >
                <button
                  type="button"
                  class="category-toggle setting tw-mr-4"
                  :aria-expanded="!isSelectedCategoryCollapsed(mapCategory.category)"
                  @click="toggleSelectedCategoryCollapse(mapCategory.category)"
                >
                  <span class="category-title">{{ mapCategory.title }}</span>
                  <ChevronRightIcon
                    class="icon category-chevron"
                    :class="{ collapsed: isSelectedCategoryCollapsed(mapCategory.category) }"
                  />
                </button>
              </MapLayersTreeCategoryRow>
              <ul v-show="!isSelectedCategoryCollapsed(mapCategory.category)" class="settings">
                <li
                  v-for="(selectedLayer, layerIndex) in getLayersByCategory(mapCategory.category)"
                  :key="selectedLayer.id"
                  class="setting"
                >
                  <MapLayersTreeLayerRow
                    :layer="selectedLayer"
                    :index="layerIndex"
                    :layers="getLayersByCategory(mapCategory.category)"
                    :group="layerGroupForCategory(mapCategory.category)"
                    :is-target="isLayerTarget(mapCategory.category, layerIndex)"
                    @reorder="handleLayerDropReorder"
                    @drag-start="handleLayerDragStart"
                    @drag-hover="handleLayerDragHover"
                    @drag-end="handleLayerDragEnd"
                  >
                    <button
                      type="button"
                      class="button __chevron __no-hover layer-button"
                      @click="toggleLayerSettings(selectedLayer)"
                    >
                      {{ selectedLayer.title }}
                      <ViewIcon
                        v-if="isLayerVisible(selectedLayer)"
                        v-tippy
                        content="Standaard zichtbaar"
                        class="icon __smedium reset-transform"
                      />
                      <ChevronRightIcon class="icon setting-chevron" />
                    </button>
                    <button
                      v-tippy="{ placement: 'bottom' }"
                      class="iconbutton __normal __transparent-bg __no-hover tw-ml-auto"
                      type="button"
                      aria-label="Verwijder laag"
                      content="Verwijder"
                      @click="confirmDeselect($event, selectedLayer)"
                    >
                      <RemoveLayerIcon class="icon" />
                    </button>
                  </MapLayersTreeLayerRow>
                </li>
              </ul>
            </li>
          </ul>
        </DnDProvider>

        <div class="settings">
          <div class="search-wrapper">
            <SearchIcon class="icon" />
            <input id="layers-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek laag" />
          </div>

          <ul class="tw-pl-2">
            <li v-for="category in displayedAvailableCategories" :key="category.id">
              <button
                type="button"
                class="category-toggle setting"
                :aria-expanded="!isAvailableCategoryCollapsed(category.id)"
                @click="toggleAvailableCategoryCollapse(category.id)"
              >
                <span class="category-title">{{ category.title }}</span>
                <ChevronRightIcon
                  class="icon category-chevron"
                  :class="{ collapsed: isAvailableCategoryCollapsed(category.id) }"
                />
              </button>
              <ul v-show="!isAvailableCategoryCollapsed(category.id)">
                <li v-for="layer in getUnselectedLayersByCategory(category.id)" :key="layer.id" class="setting">
                  {{ layer.title }}
                  <button
                    v-tippy="{ placement: 'bottom' }"
                    class="iconbutton __normal __transparent-bg __no-hover"
                    type="button"
                    aria-label="Voeg laag toe"
                    content="Voeg toe"
                    @click="selectLayer(layer)"
                  >
                    <AddLayerIcon class="icon" />
                  </button>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </template>
  </AdminSidePanel>
</template>

<script>
import ArrowLeftIcon from "../../assets/icons/arrow-left-icon.svg";
import LayerIcon from "../../assets/icons/layer-icon.svg";
import AddLayerIcon from "../../assets/icons/add-layer-icon.svg";
import RemoveLayerIcon from "../../assets/icons/remove-layer-icon.svg";
import SearchIcon from "../../assets/icons/search-icon.svg";
import ChevronRightIcon from "@/assets/icons/chevron-right-icon.svg";
import AdminSidePanel from "@/admin/components/AdminSidePanel.vue";
import MapIcon from "@/assets/icons/map-icon.svg";
import ViewIcon from "@/assets/icons/view-icon.svg";
import { getAllObjects } from "@/utils/api-helpers";
import { useConfirm } from "primevue";
import { DnDProvider } from "@vue-dnd-kit/core";
import MapLayersTreeCategoryRow from "@/admin/components/MapLayersTreeCategoryRow.vue";
import MapLayersTreeLayerRow from "@/admin/components/MapLayersTreeLayerRow.vue";

export default {
  name: "MapLayers",
  components: {
    ViewIcon,
    MapIcon,
    AdminSidePanel,
    ChevronRightIcon,
    ArrowLeftIcon,
    LayerIcon,
    AddLayerIcon,
    RemoveLayerIcon,
    SearchIcon,
    DnDProvider,
    MapLayersTreeCategoryRow,
    MapLayersTreeLayerRow,
  },
  props: {
    initialData: Object,
  },
  emits: ["update-layers", "show-form", "show-layer", "update-categories"],
  data() {
    return {
      allLayers: [],
      allCategories: [],
      selectedMapLayerConfigs: [],
      searchQuery: "",
      loading: false,
      confirm: null,
      data: {},
      collapsedSelectedCategories: {},
      collapsedAvailableCategories: {},
      categoryDrag: {
        activeIndex: null,
        targetIndex: null,
        dropCommitted: false,
      },
      layerDrag: {
        categoryId: null,
        activeIndex: null,
        targetIndex: null,
        dropCommitted: false,
      },
    };
  },
  computed: {
    layerById() {
      return new Map(this.allLayers.map((layer) => [layer.id, layer]));
    },
    unselectedLayers() {
      return this.allLayers.filter(
        (layer) =>
          this.selectedMapLayerConfigs.filter((selectedLayer) => selectedLayer.layer === layer.id).length === 0,
      );
    },
    visibleUnselectedLayers() {
      if (!this.searchQuery) {
        return this.unselectedLayers;
      }

      const searchTerm = this.searchQuery.trim().toLowerCase();

      return this.unselectedLayers.filter((layer) => {
        // Laag velden
        const matchesLayerTitle = layer.title.toLowerCase().includes(searchTerm);
        const matchesLayerDescription = layer.description?.toLowerCase().includes(searchTerm) || false;
        const matchesLayerSearchTerms =
          layer.search_terms?.some((term) => term.trim().toLowerCase().includes(searchTerm)) || false;

        // Metadataset velden
        const matchesMetadatasetTitle = layer.metadataset?.title.toLowerCase().includes(searchTerm);
        const matchesMetadatasetAbstract = layer.metadataset?.abstract?.toLowerCase().includes(searchTerm) || false;
        const metadatasetKeywords = layer.metadataset?.keyword ? layer.metadataset.keyword.split(/\r?\n/) : [];
        const matchesMetadatasetKeywords =
          metadatasetKeywords.some((term) => term.trim().toLowerCase().includes(searchTerm)) || false;

        return (
          matchesLayerTitle ||
          matchesLayerDescription ||
          matchesLayerSearchTerms ||
          matchesMetadatasetTitle ||
          matchesMetadatasetAbstract ||
          matchesMetadatasetKeywords
        );
      });
    },
    selectedBaseLayers() {
      return this.selectedMapLayerConfigs
        .map((config) => this.layerById.get(config.layer))
        .filter(
          (layerData, index) => layerData && this.isBaseLayerConfig(this.selectedMapLayerConfigs[index], layerData),
        );
    },
    selectedRegularLayers() {
      return this.selectedMapLayerConfigs
        .map((config) => {
          return {
            ...this.layerById.get(config.layer),
            mapLayerOrdering: config.ordering,
          };
        })
        .filter(
          (layerData, index) => layerData && this.isRegularLayerConfig(this.selectedMapLayerConfigs[index], layerData),
        );
    },
    displayedAvailableCategories() {
      if (!this.searchQuery) {
        return this.allCategories;
      }

      const visibleCategoryIds = new Set(
        this.visibleUnselectedLayers
          .map((layer) => layer.category?.id)
          .filter((categoryId) => categoryId !== undefined),
      );

      return this.allCategories.filter((category) => visibleCategoryIds.has(category.id));
    },
    hasMultipleBaseLayersVisible() {
      return (
        this.selectedMapLayerConfigs.filter((l) => {
          // Check if the layer has custom settings.
          if (l.settings.customSettings && l.settings.is_base && l.settings.is_visible) {
            return l;
          }

          // When the layer has no custom settings get corresponding default layer settings.
          const layerData = this.allLayers.find((layer) => layer.id === l.layer);
          if (!l.settings.customSettings && layerData.is_base && layerData.is_visible) {
            return l;
          }
        }).length > 1
      );
    },
  },
  watch: {
    initialData: {
      handler(newInitialData) {
        if (newInitialData) {
          this.data = {
            ...newInitialData,
            categories: newInitialData.categories || [],
          };
        }
      },
      immediate: true,
      deep: true,
    },
  },
  async created() {
    this.loading = true;
    Promise.all([this.getLayers(), this.getCategories()]).then(() => {
      this.loading = false;
    });

    this.selectedMapLayerConfigs = this.initialData.layers;
  },
  mounted() {
    this.confirm = useConfirm();
  },
  methods: {
    moveItem(items, fromIndex, toIndex) {
      const nextItems = [...items];
      const [movedItem] = nextItems.splice(fromIndex, 1);
      if (movedItem === undefined) {
        return items;
      }
      nextItems.splice(toIndex, 0, movedItem);
      return nextItems;
    },
    isBaseLayerConfig(config, layerData) {
      if (config.settings.customSettings) {
        return config.settings.is_base;
      }
      return layerData?.is_base;
    },
    isRegularLayerConfig(config, layerData) {
      return !this.isBaseLayerConfig(config, layerData);
    },
    async getLayers() {
      const url = getAllObjects("/atlas/api/v1/layers/");
      const result = await fetch(url, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layers");
      }

      const response = await result.json();
      this.allLayers = response.results;
    },
    async getCategories() {
      const url = getAllObjects("/atlas/api/v1/categories/");
      const result = await fetch(url, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch categories");
      }

      const response = await result.json();
      this.allCategories = response.results;
    },
    selectLayer(layer) {
      const layerCategory = layer.category;
      const mapCategories = this.data.categories || [];
      const mapCategory = mapCategories.find((candidate) => candidate.category === layerCategory.id);

      // When there is no corresponding mapCategory found, that means that for the mapCategory object for this category
      // does not exist yet.
      if (!mapCategory) {
        const newCategories = [
          ...mapCategories,
          {
            category: layerCategory.id,
            title: layerCategory.title,
            ordering: mapCategories.length - 1,
          },
        ];
        this.data.categories = this.normalizeCategoryOrdering(newCategories);
        this.$emit("update-categories", [...this.data.categories]);
      }

      this.selectedMapLayerConfigs.push({
        layer: layer.id,
        settings: { customSettings: false },
        map_category: mapCategory ? mapCategory.id : null,
      });

      this.selectedMapLayerConfigs = this.normalizeLayerOrdering(this.selectedMapLayerConfigs);
      this.$emit("update-layers", this.selectedMapLayerConfigs);
    },
    deselectLayer(layer) {
      this.selectedMapLayerConfigs = this.selectedMapLayerConfigs.filter(
        (selectedLayer) => selectedLayer.layer !== layer.id,
      );

      this.selectedMapLayerConfigs = this.normalizeLayerOrdering(this.selectedMapLayerConfigs);

      this.$emit("update-layers", this.selectedMapLayerConfigs);

      const layerCategory = layer.category.id;
      const mapCategory = this.data.categories.find((c) => c.category === layerCategory);
      if (mapCategory) {
        const hasRemainingLayerInCategory = this.selectedMapLayerConfigs.some((config) => {
          const configLayer = this.layerById.get(config.layer);
          if (!configLayer || configLayer.category?.id !== layerCategory) {
            return false;
          }

          return this.isRegularLayerConfig(config, configLayer);
        });

        if (!hasRemainingLayerInCategory) {
          const updatedCategories = this.data.categories.filter((c) => c.category !== layerCategory);
          this.data.categories = this.normalizeCategoryOrdering(updatedCategories);
          this.$emit("update-categories", this.data.categories);
        }
      }
    },
    getLayersByCategory(categoryId) {
      const orderingByLayerId = new Map(
        this.selectedMapLayerConfigs.map((config) => [config.layer, config.ordering ?? Number.MAX_SAFE_INTEGER]),
      );

      return this.selectedRegularLayers
        .filter((layer) => layer.category?.id === categoryId)
        .sort(
          (a, b) =>
            (orderingByLayerId.get(a.id) ?? Number.MAX_SAFE_INTEGER) -
            (orderingByLayerId.get(b.id) ?? Number.MAX_SAFE_INTEGER),
        );
    },
    getUnselectedLayersByCategory(categoryId) {
      return this.visibleUnselectedLayers.filter((layer) => layer.category?.id === categoryId);
    },
    isSelectedCategoryCollapsed(categoryId) {
      return Boolean(this.collapsedSelectedCategories[categoryId]);
    },
    isAvailableCategoryCollapsed(categoryId) {
      return Boolean(this.collapsedAvailableCategories[categoryId]);
    },
    toggleSelectedCategoryCollapse(categoryId) {
      this.collapsedSelectedCategories = {
        ...this.collapsedSelectedCategories,
        [categoryId]: !this.isSelectedCategoryCollapsed(categoryId),
      };
    },
    toggleAvailableCategoryCollapse(categoryId) {
      this.collapsedAvailableCategories = {
        ...this.collapsedAvailableCategories,
        [categoryId]: !this.isAvailableCategoryCollapsed(categoryId),
      };
    },
    back() {
      this.$emit("show-form");
    },
    toggleLayerSettings(selectedLayer) {
      this.$emit("show-layer", selectedLayer.id);
    },
    isLayerVisible(layer) {
      const layerConfig = this.selectedMapLayerConfigs.find((l) => l.layer === layer.id);

      if (layerConfig.settings.customSettings) {
        return layerConfig.settings.is_visible;
      }

      return layer.is_visible;
    },
    confirmDeselect(event, layer) {
      this.confirm.require({
        target: event.target,
        group: "templating",
        message: `Weet u zeker dat u de kaartlaag: "${layer.title}" wilt deselecteren?`,
        rejectProps: {
          icon: "pi pi-times",
          label: "Annuleer",
          outlined: true,
        },
        acceptProps: {
          icon: "pi pi-check",
          label: "Deselecteer",
        },
        accept: () => {
          this.deselectLayer(layer);
        },
        reject: () => {},
      });
    },
    normalizeCategoryOrdering(categories) {
      return categories.map((category, index) => ({
        ...category,
        ordering: index,
      }));
    },
    normalizeLayerOrdering(mapLayerConfigs) {
      const categories = this.data.categories || [];
      const orderingByLayerId = new Map();

      categories.forEach((mapCategory) => {
        const categoryLayers = mapLayerConfigs.filter((config) => {
          const layerData = this.layerById.get(config.layer);
          if (!layerData || layerData.category?.id !== mapCategory.category) {
            return false;
          }

          return this.isRegularLayerConfig(config, layerData);
        });

        categoryLayers.forEach((config, index) => {
          orderingByLayerId.set(config.layer, index);
        });
      });

      return mapLayerConfigs.map((config) => {
        if (!orderingByLayerId.has(config.layer)) {
          return config;
        }

        return {
          ...config,
          ordering: orderingByLayerId.get(config.layer),
        };
      });
    },
    layerGroupForCategory(categoryId) {
      return `map-layers-${categoryId}`;
    },
    isCategoryTarget(index) {
      return (
        this.categoryDrag.activeIndex !== null &&
        this.categoryDrag.activeIndex !== index &&
        this.categoryDrag.targetIndex === index
      );
    },
    isLayerTarget(categoryId, index) {
      return (
        this.layerDrag.categoryId === categoryId &&
        this.layerDrag.activeIndex !== null &&
        this.layerDrag.activeIndex !== index &&
        this.layerDrag.targetIndex === index
      );
    },
    reorderCategories({ fromIndex, toIndex }) {
      fromIndex = Number(fromIndex);
      toIndex = Number(toIndex);
      if (!Number.isInteger(fromIndex) || !Number.isInteger(toIndex)) {
        return;
      }

      if (fromIndex === toIndex || fromIndex < 0 || toIndex < 0 || !this.data.categories?.length) {
        return;
      }

      const nextCategories = this.moveItem(this.data.categories, fromIndex, toIndex);
      this.data.categories = this.normalizeCategoryOrdering(nextCategories);
      this.$emit("update-categories", this.data.categories);
    },
    handleCategoryDropReorder(payload) {
      this.categoryDrag.dropCommitted = true;
      this.reorderCategories(payload);
    },
    handleCategoryDragStart({ index }) {
      this.categoryDrag.activeIndex = index;
      this.categoryDrag.targetIndex = index;
      this.categoryDrag.dropCommitted = false;
    },
    handleCategoryDragHover({ index }) {
      if (this.categoryDrag.activeIndex === null) {
        return;
      }
      this.categoryDrag.targetIndex = index;
    },
    handleCategoryDragEnd() {
      if (!this.categoryDrag.dropCommitted) {
        this.reorderCategories({
          fromIndex: this.categoryDrag.activeIndex,
          toIndex: this.categoryDrag.targetIndex,
        });
      }

      this.categoryDrag.activeIndex = null;
      this.categoryDrag.targetIndex = null;
      this.categoryDrag.dropCommitted = false;
    },
    reorderLayersInCategory({ categoryId, fromIndex, toIndex }) {
      fromIndex = Number(fromIndex);
      toIndex = Number(toIndex);
      if (!Number.isInteger(fromIndex) || !Number.isInteger(toIndex)) {
        return;
      }

      if (fromIndex === toIndex || fromIndex < 0 || toIndex < 0) {
        return;
      }

      const categoryLayerConfigs = this.selectedMapLayerConfigs
        .filter((config) => {
          const configLayer = this.layerById.get(config.layer);
          return configLayer?.category?.id === categoryId && this.isRegularLayerConfig(config, configLayer);
        })
        .sort((a, b) => (a.ordering ?? Number.MAX_SAFE_INTEGER) - (b.ordering ?? Number.MAX_SAFE_INTEGER));

      if (fromIndex >= categoryLayerConfigs.length || toIndex >= categoryLayerConfigs.length) {
        return;
      }

      const reorderedCategoryLayerConfigs = this.moveItem(categoryLayerConfigs, fromIndex, toIndex);
      const orderingByLayerId = new Map(reorderedCategoryLayerConfigs.map((config, index) => [config.layer, index]));

      this.selectedMapLayerConfigs = this.selectedMapLayerConfigs.map((config) => {
        if (!orderingByLayerId.has(config.layer)) {
          return config;
        }

        return {
          ...config,
          ordering: orderingByLayerId.get(config.layer),
        };
      });
      this.$emit("update-layers", this.selectedMapLayerConfigs);
    },
    handleLayerDropReorder(payload) {
      this.layerDrag.dropCommitted = true;
      this.reorderLayersInCategory(payload);
    },
    handleLayerDragStart({ categoryId, index }) {
      this.layerDrag.categoryId = categoryId;
      this.layerDrag.activeIndex = index;
      this.layerDrag.targetIndex = index;
      this.layerDrag.dropCommitted = false;
    },
    handleLayerDragHover({ categoryId, index }) {
      if (this.layerDrag.activeIndex === null || this.layerDrag.categoryId !== categoryId) {
        return;
      }
      this.layerDrag.targetIndex = index;
    },
    handleLayerDragEnd() {
      if (!this.layerDrag.dropCommitted && this.layerDrag.categoryId !== null) {
        this.reorderLayersInCategory({
          categoryId: this.layerDrag.categoryId,
          fromIndex: this.layerDrag.activeIndex,
          toIndex: this.layerDrag.targetIndex,
        });
      }

      this.layerDrag.categoryId = null;
      this.layerDrag.activeIndex = null;
      this.layerDrag.targetIndex = null;
      this.layerDrag.dropCommitted = false;
    },
  },
};
</script>

<style scoped>
.settings + .settings {
  margin-top: 40px;
}

.setting .iconbutton {
  margin-left: auto;
}

li.setting:first-child {
  border-top: none;
}

.selected-layer-header-wrapper {
  width: 100%;
  height: 54px;
  border-bottom: 1px solid var(--color-grey-60);
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: center;
  justify-content: center;
}

.setting-label {
  display: flex;
  gap: 4px;
  align-items: center;
  justify-content: center;
}

.base-layer-warning {
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-small);
  color: var(--color-alert);
}

.search-wrapper {
  position: relative;
  border-top: 1px solid var(--color-grey-60);
  border-bottom: 1px solid var(--color-grey-60);
  margin-bottom: -1px;
}

.search-wrapper svg {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 16px;
  margin: auto 0;
  pointer-events: none;
}

.search-wrapper input {
  width: 100%;
  height: 48px;
  padding: 0 0 0 48px;
}

.setting-chevron {
  width: 32px;
  margin-left: auto;
}

.layer-button {
  background: transparent;
  padding: 0;
}

.category-toggle {
  display: flex;
  align-items: center;
  width: 100%;
  border: 0;
  background: transparent;
  padding: 0;
  text-align: left;
}

.category-title {
  font-size: var(--font-size-default);
  font-weight: var(--font-weight-bold);
}

.category-chevron {
  margin-left: auto;
  transform: rotate(90deg);
  transition: transform 0.2s ease;
}

.category-chevron.collapsed {
  transform: rotate(0deg);
}

/* The hover transform somehow breaks v-tippy.  */
.button.__chevron:hover svg.reset-transform {
  transform: translateX(0);
}
</style>
