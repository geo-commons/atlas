<template>
  <li class="layer-wrapper">
    <ExpandButton :title="layer.title" :is-open="isOpen" @show-content="onToggleOpen">
      <template #header>
        <div v-if="!sortLayers" class="tw-flex tw-items-center">
          <div v-if="layerOpacityIsChangable" class="opacity-wrapper">
            <input
              v-if="showSlider"
              id="opacity"
              class="opacity-slider"
              type="range"
              name="opacity"
              min="0"
              max="100"
              step="10"
              :aria-label="`Transparantie van laag ${layer.title} instellen`"
              :value="layer.opacity * 100"
              @change="(e) => changeLayerOpacity(layer.id, e.target.value / 100)"
            />
            <button
              v-tippy
              class="iconbutton __xs __round"
              :class="{ isActive: showSlider }"
              content="Transparantie"
              aria-label="Toon transparantie schuifregelaar"
              @click="toggleSlider"
            >
              <OpacityIcon />
            </button>
            <input
              :id="`${layer.id}-opacity`"
              class="opacity-input"
              type="number"
              :name="`${layer.id}-opacity`"
              :aria-label="`Transparantie van laag ${layer.title} instellen`"
              min="0"
              max="100"
              step="10"
              :value="layer.opacity * 100"
              @change="(e) => changeLayerOpacity(layer.id, e.target.value / 100)"
            />
          </div>
          <button
            v-tippy="{ placement: 'right' }"
            class="iconbutton __xs __round"
            :content="isSelectable ? 'Laag niet selecteerbaar maken' : 'Laag selecteerbaar maken'"
            :aria-label="isSelectable ? 'Laag niet selecteerbaar maken' : 'Laag selecteerbaar maken'"
            @click="toggleLayerSelectable"
          >
            <SelectableIcon v-if="isSelectable" class="icon __smedium" />
            <SelectableDisabledIcon v-if="!isSelectable" class="icon __smedium" />
          </button>
          <LayerInfo :layer="layer" :show-always="true" />
          <button
            v-if="layerIsClosable"
            v-tippy="{ placement: 'right' }"
            class="iconbutton __xs __round"
            content="Sluit"
            aria-label="Sluit laag"
            @click="toggleLayer"
          >
            <CloseCircleIcon />
          </button>
        </div>
        <div
          v-else
          class="tw-flex tw-items-center"
          :class="index === visibleLayers.length - 1 ? 'extra-padding-right' : ''"
        >
          <button
            v-show="index > 0"
            v-tippy="{ placement: 'right' }"
            class="iconbutton __xs __round"
            content="Verplaats kaartlaag naar boven"
            aria-label="Verplaats kaartlaag naar boven"
            @click="changeLayerOrder('up')"
          >
            <ArrowUpIcon class="icon __small" />
          </button>
          <button
            v-show="index < visibleLayers.length - 1"
            v-tippy="{ placement: 'right' }"
            class="iconbutton __xs __round"
            content="Verplaats kaartlaag naar beneden"
            aria-label="Verplaats kaartlaag naar beneden"
            @click="changeLayerOrder('down')"
          >
            <ArrowDownIcon class="icon __small" />
          </button>
        </div>
      </template>

      <template #default>
        <div class="content">
          <img
            v-if="layerHasLegend && !legendJson"
            :src="layer.legend_url ? layer.legend_url : legendImage"
            class="legend"
            :alt="`Legenda voor laag ${layer.title}`"
          />
          <div v-if="layerHasLegend && legendJson" class="tw-flex tw-flex-col tw-gap-2">
            <div v-for="legendField in legendJson" :key="legendField.name">
              <div v-if="legendField.filter" class="tw-flex tw-flex-row tw-items-start tw-gap-2">
                <Checkbox
                  v-model="checkboxFilters[getFilterParameter(legendField.filter)]"
                  :input-id="legendField.name"
                  :value="getFilterValue(legendField.filter)"
                  @update:model-value="updateLegendFilters(getFilterParameter(legendField.filter))"
                />
                <label :for="legendField.name" class="tw-flex tw-flex-row tw-items-start tw-gap-2">
                  <img :src="getLegendFieldImage(legendField.name)" />{{
                    legendField.title ? legendField.title : legendField.name
                  }}
                </label>
              </div>
              <div v-else>
                <div class="tw-flex tw-flex-row tw-items-start tw-gap-2">
                  <img :src="getLegendFieldImage(legendField.name)" />{{
                    legendField.title ? legendField.title : legendField.name
                  }}
                </div>
              </div>
            </div>
          </div>
          <span v-if="!layerHasLegend && !legendJson">Geen legenda beschikbaar</span>
          <span v-if="errorLoadingLegend">Kan de legenda niet laden</span>
        </div>
      </template>
    </ExpandButton>
  </li>
</template>

<script>
import ExpandButton from "./ExpandButton";
import LayerInfo from "./LayerInfo";
import ArrowUpIcon from "../assets/icons/arrow-up-icon.svg";
import ArrowDownIcon from "../assets/icons/arrow-down-icon.svg";
import CloseCircleIcon from "../assets/icons/close-circle-icon.svg";
import OpacityIcon from "../assets/icons/opacity-icon.svg";
import SelectableIcon from "../assets/icons/selectable-icon.svg";
import SelectableDisabledIcon from "../assets/icons/selectable-disabled-icon.svg";
import { useMapStore } from "@/stores/map_store";
import { fetchLegendImage } from "@/utils/legend-utils";
import { getFetchParameters, layerRequiresAuthentication } from "@/utils/auth";
import { ELayerTypes } from "@/types/layer";

export default {
  name: "VisibleLayer",
  components: {
    ExpandButton,
    LayerInfo,
    ArrowUpIcon,
    ArrowDownIcon,
    CloseCircleIcon,
    OpacityIcon,
    SelectableIcon,
    SelectableDisabledIcon,
  },
  props: {
    layer: Object,
    layerIsClosable: Boolean,
    layerOpacityIsChangable: Boolean,
    position: Object,
    isOpen: Boolean,
    user: Object,
    mapId: String,
    sortLayers: Boolean,
    index: Number,
  },
  data() {
    return {
      showSlider: false,
      store: null,
      errorLoadingLegend: false,
      legendImage: null,
      legendJson: null,
      isSelectable: null,
      initialIsSelectable: null,
      checkboxFilters: [],
    };
  },
  computed: {
    layerHasLegend() {
      return (
        this.layer.source_type === ELayerTypes.WMS ||
        this.layer.source_type === ELayerTypes.WMS_WFS ||
        this.layer.source_type === ELayerTypes.WMTS ||
        this.layer.legend_url
      );
    },
    visibleLayers() {
      return this.store ? this.store.visibleLayers : [];
    },
  },
  watch: {
    async position(position, oldPosition) {
      if (position.zoom !== oldPosition.zoom && this.layerHasLegend) {
        await this.setLegend();
      }
    },
  },
  async mounted() {
    this.isSelectable = this.layer.is_selectable;
    this.initialIsSelectable = this.layer.is_selectable;

    if (this.layerHasLegend) {
      await this.setLegend();
    }
  },
  created() {
    this.store = useMapStore(this.mapId);

    this.store.$subscribe((_, state) => {
      // Subscribes to the store and keeps the layer’s checkbox filters in sync.
      // Whenever filters for this layer change in the store, the corresponding
      // checkboxFilters are updated. If no layer filters exist, the filters are reset.
      if (state.layerFilters[this.layer.id]) {
        setTimeout(() => {
          this.checkboxFilters = state.layerFilters[this.layer.id]?.filters;
        }, 100);
      } else if (!Object.keys(state.layerFilters).length) {
        this.checkboxFilters = [];
      }
    });
  },
  methods: {
    fetchLegendImage,
    toggleSlider() {
      this.showSlider = !this.showSlider;
    },
    changeLayerOpacity(layerId, opacity) {
      this.store.setLayerOpacity({ selectedLayerId: layerId, opacity: opacity });
    },
    toggleLayer() {
      // Make sure to restore is_selectable to its initial value.
      if (this.initialIsSelectable && this.layer.is_selectable !== this.initialIsSelectable) {
        this.toggleLayerSelectable();
      }
      this.store.toggleLayer({ selectedLayerId: this.layer.id, is_visible: false });
    },
    toggleLayerSelectable() {
      this.isSelectable = !this.isSelectable;
      this.store.toggleLayerisSelectable({ selectedLayerId: this.layer.id, is_selectable: this.isSelectable });
    },
    async fetchLegendAsJson() {
      const params = new URLSearchParams({
        SERVICE: "WMS",
        VERSION: "1.1.1",
        REQUEST: "GetLegendGraphic",
        FORMAT: "application/json",
        LAYER: this.layer.name,
        STYLE: this.layer.server_style || "",
      });

      const url = new URL(this.layer.url);

      if (params) {
        url.search = params.toString();
      }

      const fetchParams = layerRequiresAuthentication(this.layer) ? getFetchParameters(this.layer, this.user) : {};

      try {
        const result = await fetch(url, fetchParams);
        if (result.ok) {
          const data = await result.json();
          return data?.Legend?.[0]?.rules || [];
        }
      } catch (e) {
        console.error(e);
      }

      return false;
    },
    getLegendFieldImage(rule) {
      const params = new URLSearchParams({
        SERVICE: "WMS",
        VERSION: "1.1.1",
        REQUEST: "GetLegendGraphic",
        FORMAT: "image/png",
        LAYER: this.layer.name,
        RULE: rule,
      });

      const url = `${this.layer.url}?${params.toString()}`;

      return url;
    },
    async setLegend() {
      if (this.layer.is_filterable_in_legend) {
        const result = await this.fetchLegendAsJson();

        if (result) {
          this.legendJson = result;
          this.checkboxFilters = this.store.getFiltersForLayer(this.layer.id);
          return;
        }
      }

      try {
        const legendImageResult = await this.fetchLegendImage(this.layer, this.position, this.user);

        if (legendImageResult) {
          this.legendImage = legendImageResult.url;
          this.errorLoadingLegend = legendImageResult.error;
        }
      } catch (e) {
        console.error(e);
      }
    },
    getFilterParameter(filterString) {
      // Regex to extract the parameter name before '='
      const match = filterString.match(/\[([a-zA-Z0-9_]+)\s*=/);

      return match ? match[1] : null;
    },
    getFilterValue(filterString) {
      // Regex to extract the filter value after '='
      const match = filterString.match(/\b\w+\s*=\s*'((?:''|[^'])*)'/);

      return match ? match[1] : null;
    },
    updateLegendFilters(filterParameter) {
      const oldLayerFilters = this.store.getFiltersForLayer(this.layer.id);

      const filters = {
        ...oldLayerFilters,
        [filterParameter]: this.checkboxFilters[filterParameter],
      };

      // Remove filter if no checkbox filter values are selected
      if (!this.checkboxFilters[filterParameter]?.length) {
        delete filters[filterParameter];
      }

      this.store.updateFiltersForLayer(this.layer.id, filters);
    },
    changeLayerOrder(direction) {
      this.store.changeLayerOrder({ selectedLayerId: this.layer.id, direction: direction });
    },
    onToggleOpen(isOpen) {
      this.$emit("toggle-is-open", { layerId: this.layer.id, isOpen });
    },
  },
};
</script>

<style scoped>
.layer-wrapper:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-50);
}

.opacity-wrapper {
  display: flex;
  align-items: center;
}

.opacity-input {
  width: 22px;
  flex-shrink: 0;
  padding: 0;
  font-size: 12px;
  font-weight: var(--font-weight-bold);
}

.opacity-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.opacity-input[type="number"] {
  -moz-appearance: textfield;
}

.opacity-slider {
  flex-shrink: 0;
  width: 80px;
  margin: 0;
}

.content {
  padding: 4px 8px 4px;
  overflow-x: auto;
}

input[type="number"] {
  border: none;
}

.extra-padding-right {
  padding-right: 24px;
}
</style>
