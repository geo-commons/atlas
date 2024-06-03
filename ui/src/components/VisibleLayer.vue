<template>
  <li class="layer-wrapper">
    <ExpandButton :title="layer.title" :is-open="isOpen">
      <template #header>
        <div class="buttons">
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
              class="iconbutton __round"
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
            v-if="initialIsSelectable"
            v-tippy="{ placement: 'right' }"
            class="iconbutton __round"
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
            class="iconbutton __round"
            content="Sluit"
            aria-label="Sluit laag"
            @click="toggleLayer"
          >
            <CloseCircleIcon />
          </button>
        </div>
      </template>

      <template #default>
        <div class="content">
          <img v-if="layerHasLegend" :src="legendImage" class="legend" :alt="`Legenda voor laag ${layer.title}`" />
          <span v-if="!layerHasLegend">Geen legenda beschikbaar</span>
          <span v-if="errorLoadingLegend">Kan de legenda niet laden</span>
        </div>
      </template>
    </ExpandButton>
  </li>
</template>

<script>
import Projection from "ol/proj/Projection";
import TileWMS from "ol/source/TileWMS";
import View from "ol/View";
import ExpandButton from "./ExpandButton";
import LayerInfo from "./LayerInfo";
import { getFetchParameters, layerRequiresAuthentication } from "../utils/auth";
import CloseCircleIcon from "../assets/icons/close-circle-icon.svg";
import OpacityIcon from "../assets/icons/opacity-icon.svg";
import SelectableIcon from "../assets/icons/selectable-icon.svg";
import SelectableDisabledIcon from "../assets/icons/selectable-disabled-icon.svg";

export default {
  name: "VisibleLayer",
  components: {
    ExpandButton,
    LayerInfo,
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
  },
  data() {
    return {
      showSlider: false,
      errorLoadingLegend: false,
      legendImage: null,
      isSelectable: null,
      initialIsSelectable: null,
    };
  },
  computed: {
    layerHasLegend() {
      return this.layer.source_type === "WMS" || this.layer.source_type === "WMS_WFS";
    },
  },
  watch: {
    position(position, oldPosition) {
      if (position.zoom !== oldPosition.zoom) {
        this.fetchLegendImage();
      }
    },
  },
  mounted() {
    if (this.layerHasLegend) {
      this.fetchLegendImage();
    }
    this.isSelectable = this.layer.is_selectable;
    this.initialIsSelectable = this.layer.is_selectable;
  },
  methods: {
    toggleSlider() {
      this.showSlider = !this.showSlider;
    },
    changeLayerOpacity(layerId, opacity) {
      this.$emit("set-layer-opacity", [layerId, opacity]);
    },
    toggleLayer() {
      // Make sure to restore is_selectable to its initial value.
      if (this.initialIsSelectable && this.layer.is_selectable !== this.initialIsSelectable) {
        this.toggleLayerSelectable();
      }

      this.$emit("toggle-layer", this.layer);
    },
    toggleLayerSelectable() {
      this.isSelectable = !this.isSelectable;
      this.$emit("toggle-is-selectable", [this.layer.id, this.isSelectable]);
    },
    async fetchLegendImage() {
      const wmsSource = new TileWMS({
        url: this.layer.url,
        servertype: this.layer.server_type,
        params: {
          LAYERS: this.layer.name,
          TILED: true,
        },
      });

      const rdProjection = new Projection({
        code: "EPSG:28992",
        units: "m",
      });

      const view = new View({
        projection: rdProjection,
        enableRotation: false,
        center: this.position.center,
        zoom: this.position.zoom,
      });

      const params = {
        STYLE: this.layer.server_style ? this.layer.server_style : "",
        LEGEND_OPTIONS: "forceTitles:off;forceLabels:on;fontAntiAliasing:true",
      };

      const url = wmsSource.getLegendUrl(view.getResolution(), params);

      if (!layerRequiresAuthentication(this.layer)) {
        this.legendImage = url;
        return;
      }

      try {
        const result = await fetch(url, getFetchParameters(this.layer, this.user));

        if (result.ok) {
          const blob = await result.blob();
          this.legendImage = URL.createObjectURL(blob);
        } else {
          this.errorLoadingLegend = true;
        }
      } catch (e) {
        this.errorLoadingLegend = true;
      }
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

.iconbutton {
  width: 24px;
  height: 24px;
}

.content {
  padding: 4px 8px 4px;
  overflow-x: auto;
}

.buttons {
  display: flex;
  align-items: center;
}

input[type="number"] {
  border: none;
}
</style>
