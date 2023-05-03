<template>
  <div>
    <div class="buttons-wrapper">
      <div
        class="buttons"
        :class="{
          isOpen: panel === 'layers' || panel === 'activeLayers',
          showSecondButton: !isEmbed && visibleLayers.length > 0,
        }"
      >
        <button
          v-if="!isEmbed"
          v-tippy
          class="iconbutton"
          :class="{ isActive: panel === 'layers' }"
          content="Alle lagen"
          aria-label="Toon alle lagen"
          :aria-expanded="String(panel === 'layers')"
          aria-controls="layers"
          @click="() => togglePanel('layers')"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24"
            viewBox="0 0 24 24"
            width="24"
          >
            <path d="M0 0h24v24H0V0z" fill="none" />
            <path
              fill="currentColor"
              d="M11.99 18.54l-7.37-5.73L3 14.07l9 7 9-7-1.63-1.27zM12 16l7.36-5.73L21 9l-9-7-9 7 1.63 1.27L12 16zm0-11.47L17.74 9 12 13.47 6.26 9 12 4.53z"
            />
          </svg>
        </button>

        <button
          v-if="visibleLayers.length > 0"
          v-tippy
          class="iconbutton"
          :tabindex="visibleLayers.length > 0 ? 0 : -1"
          :class="{ isActive: panel === 'activeLayers' }"
          content="Zichtbare lagen"
          aria-label="Toon zichtbare lagen"
          :aria-expanded="String(panel === 'activeLayers')"
          aria-controls="visibleLayers"
          @click="() => togglePanel('activeLayers')"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24"
            viewBox="0 0 24 24"
            width="24"
          >
            <path d="M0 0h24v24H0V0z" fill="none" />
            <path
              fill="currentColor"
              d="M12 6c3.79 0 7.17 2.13 8.82 5.5C19.17 14.87 15.79 17 12 17s-7.17-2.13-8.82-5.5C4.83 8.13 8.21 6 12 6m0-2C7 4 2.73 7.11 1 11.5 2.73 15.89 7 19 12 19s9.27-3.11 11-7.5C21.27 7.11 17 4 12 4zm0 5c1.38 0 2.5 1.12 2.5 2.5S13.38 14 12 14s-2.5-1.12-2.5-2.5S10.62 9 12 9m0-2c-2.48 0-4.5 2.02-4.5 4.5S9.52 16 12 16s4.5-2.02 4.5-4.5S14.48 7 12 7z"
            />
          </svg>
        </button>
      </div>

      <transition name="fade">
        <div
          v-if="!isEmbed && visibleLayers.length > 0"
          class="counter visible-layer-counter"
        >
          {{ visibleLayers.length }}
        </div>
      </transition>
    </div>

    <transition name="fade">
      <ul v-if="panel === 'layers'" id="layers" class="layers">
        <div class="layers-search">
          <label for="layers-search">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="18px"
              viewBox="0 0 24 24"
              width="18px"
              fill="currentColor"
            >
              <path d="M0 0h24v24H0V0z" fill="none" />
              <path
                d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
              />
            </svg>
          </label>
          <input
            id="layers-search"
            v-model="searchQuery"
            type="search"
            name="query"
            placeholder="Zoek laag"
          />
        </div>
        <li>
          <ExpandButton
            v-for="category in categories"
            :key="category.id"
            :title="category.title"
            :is-open="searchQuery != ''"
            class="category-wrapper"
          >
            <template #button>
              <div
                v-if="
                  category.layers.filter((layer) => layer.is_visible).length > 0
                "
                class="counter layer-counter"
              >
                {{ category.layers.filter((layer) => layer.is_visible).length }}
              </div>
            </template>
            <template #default>
              <ul :id="category.id" class="sublayers">
                <li
                  v-for="layer in category.layers"
                  :key="layer.id"
                  class="sublayer"
                >
                  <!-- <div class="sublayer-check"> -->
                  <input
                    :id="layer.id"
                    type="checkbox"
                    :name="layer.id"
                    :checked="layer.is_visible"
                    :disabled="
                      layer.is_disabled ||
                      (layer.login_required && (!user || !user.token))
                    "
                    @change="() => onSelectLayer(layer)"
                  />
                  <label :for="layer.id">
                    {{ layer.title }}
                    <LayerAuthentication
                      v-if="layer.login_required && (!user || !user.token)"
                    />
                  </label>
                  <!-- </div> -->
                  <LayerFit
                    v-if="!layer.is_disabled && layer.extent"
                    :layer="layer"
                    @click="() => onFit(layer)"
                  />
                  <LayerInfo :layer="layer" />
                </li>
              </ul>
            </template>
          </ExpandButton>
        </li>
      </ul>
    </transition>

    <transition name="fade">
      <ul
        v-if="visibleLayers.length > 0 && panel === 'activeLayers'"
        id="visibleLayers"
        class="visible-layers"
      >
        <VisibleLayer
          v-for="(layer, i) in visibleLayers"
          :key="layer.id"
          :position="position"
          :layer="layer"
          :layer-is-closable="!isEmbed"
          :layer-opacity-is-changable="!isEmbed"
          :is-open="i === 0"
          @set-layer-opacity="setLayerOpacity"
          @toggle-layer="onSelectLayer"
        />
      </ul>
    </transition>
  </div>
</template>

<script>
import { intersects } from "ol/extent";
import ExpandButton from "./ExpandButton";
import VisibleLayer from "./VisibleLayer";
import LayerAuthentication from "./LayerAuthentication";
import LayerFit from "./LayerFit";
import LayerInfo from "./LayerInfo";

export default {
  name: "LayersPanel",
  components: {
    ExpandButton,
    VisibleLayer,
    LayerAuthentication,
    LayerFit,
    LayerInfo,
  },
  props: {
    layers: Array,
    position: Object,
    user: Object,
    isEmbed: Boolean,
    initiallyShowLayerList: Boolean,
  },
  data() {
    const visibleLayers = this.layers.filter(
      (layer) => layer.category && layer.is_visible
    );

    return {
      panel:
        visibleLayers.length > 0
          ? "activeLayers"
          : this.initiallyShowLayerList
          ? "layers"
          : "",
      searchQuery: "",
    };
  },
  computed: {
    categories() {
      let categories = [];

      this.layers.forEach((layer) => {
        if (!layer.category) {
          return;
        }

        if (this.searchQuery) {
          const searchFor = this.searchQuery.toLowerCase();
          const searchIn = layer.title.toLowerCase();

          if (searchIn.search(searchFor) === -1) {
            return;
          }
        }

        const existingCategory = categories.find(
          (c) => c.id === layer.category.id
        );

        layer.is_disabled = false;
        if (layer.zoom_min && this.position.zoom < layer.zoom_min) {
          layer.is_disabled = true;
        }

        if (layer.zoom_max && this.position.zoom > layer.zoom_max) {
          layer.is_disabled = true;
        }

        if (
          layer.extent &&
          this.position.extent &&
          !intersects(layer.extent, this.position.extent)
        ) {
          layer.is_disabled = true;
        }

        if (existingCategory) {
          existingCategory.layers.push(layer);
          return;
        }

        const newCategory = {
          ...layer.category,
          layers: [layer],
        };

        categories.push(newCategory);
      });

      return categories;
    },
    visibleLayers() {
      return this.layers.filter((layer) => layer.category && layer.is_visible);
    },
  },
  methods: {
    togglePanel(selectedPanel) {
      if (this.panel === "layers" && selectedPanel === "layers") {
        this.panel = "activeLayers";
        return;
      }

      this.panel = selectedPanel !== this.panel ? selectedPanel : "";
    },
    onSelectLayer(selectedLayer) {
      this.$emit("toggle-layer", [selectedLayer.id, !selectedLayer.is_visible]);
    },
    setLayerOpacity(values) {
      this.$emit("set-layer-opacity", values);
    },
    onFit(selectedLayer) {
      this.$emit("on-fit", selectedLayer.extent);
    },
  },
};
</script>

<style scoped>
.buttons-wrapper {
  position: relative;
}

.buttons {
  display: flex;
  background: white;
  width: var(--width-button-large);
  overflow: hidden;
  border-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);
  transition: width 0.1s ease, border-radius 0.1s;
}

.buttons.isOpen {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.buttons.showSecondButton {
  width: calc(var(--width-button-large) * 2 + 1px);
}

.iconbutton {
  position: relative;
  width: var(--width-button-large);
  height: var(--width-button-large);
}

.iconbutton:not(:last-child) {
  box-sizing: content-box;
  border-right: 1px solid var(--color-grey-50);
}

.counter {
  flex-shrink: 0;
  height: 18px;
  min-width: 18px;
  border-radius: 9px;
  border: 2px solid var(--color-primary);
  padding: 0 3px;
  background: white;
  color: var(--color-primary);
  font-size: 11px;
  font-weight: var(--font-weight-bold);
  line-height: 14px;
  text-align: center;
  white-space: nowrap;
  user-select: none;
}

.visible-layer-counter {
  position: absolute;
  top: 2px;
  left: calc(100% - 8px);
}

.layer-counter {
  margin: 7px 8px 0 4px;
}

.layers,
.visible-layers {
  position: absolute;
  bottom: var(--width-button-large);
  left: 0;
  max-height: calc(
    (100 * var(--vh)) -
      ((var(--width-button-large) * 2) + (var(--padding-screen) * 3))
  );
  width: calc(var(--width-detail) - (var(--padding-screen) * 2));
  max-width: calc(
    100vw - (var(--padding-screen) * 3) - var(--width-button-normal)
  );
  overflow-y: auto;
  background: white;
  border-radius: var(--radius-small);
  border-bottom-left-radius: 0;
  box-shadow: var(--shadow-normal);
}

.layers-search {
  width: 100%;
  display: flex;
  height: var(--width-button-large);
  border-bottom: 1px solid var(--color-grey-50);
}

.layers-search label {
  flex-shrink: 0;
  width: 32px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-icon-grey);
}

.layers-search input {
  flex-grow: 1;
  height: 100%;
}

.category-wrapper:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-50);
}

.sublayers {
  padding: 0 4px 4px 30px;
}

.sublayer {
  position: relative;
  display: flex;
}

.sublayer > input {
  position: absolute;
  top: 5px;
  left: 0;
  width: 14px;
  height: 14px;
  margin: 0;
}

.sublayer > label {
  display: flex;
  position: relative;
  width: 100%;
  cursor: pointer;
  padding: 2px 0 2px 20px;
  user-select: none;
  word-break: break-word;
}

.sublayer > input:disabled + label {
  text-decoration: line-through;
}
</style>
