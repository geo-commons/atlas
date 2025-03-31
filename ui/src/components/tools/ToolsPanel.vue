<template>
  <div class="tools-panel">
    <div class="tools-panel__buttons">
      <SelectMenu
        v-if="features.selectarea"
        :show-select-menu="showSelectMenu"
        :set-tool="setTool"
        :toggle-select-area="toggleSelectArea"
        :tool="tool"
      />

      <MeasureMenu
        v-if="features.measure"
        :show-measure-menu="showMeasureMenu"
        :set-tool="setTool"
        :tool="tool"
        :toggle-measure="toggleMeasure"
      />

      <DrawMenu
        v-if="config && config.features.draw && features.draw && user"
        :show-draw-menu="showDrawMenu"
        :tool="tool"
        :color="color"
        :stroke-width="strokeWidth"
        :font-size="fontSize"
        :draw-features="drawFeatures"
        :removed-draw-features="removedDrawFeatures"
        :set-tool="setTool"
        :set-color="setColor"
        :set-stroke-width="setStrokeWidth"
        :set-font-size="setFontSize"
        :set-interaction="setInteraction"
        :clear-drawing="clearDrawing"
        :disable-draw-menu="disableDrawMenu"
        :after-draw="afterDraw"
        :toggle-draw="toggleDraw"
      />

      <EditLayerMenu
        v-if="config && config.features.edit_layer_features && features.edit_layer_features && user"
        :show-edit-feature-menu="showEditFeatureMenu"
        :toggle-edit-layer="toggleEditLayer"
        :tool="tool"
        :set-tool="setTool"
      />
    </div>
  </div>
</template>

<script>
import draw from "@/utils/draw";
import SelectMenu from "@/components/tools/SelectMenu.vue";
import MeasureMenu from "@/components/tools/MeasureMenu.vue";
import DrawMenu from "@/components/tools/DrawMenu.vue";
import EditLayerMenu from "@/components/tools/EditLayerMenu.vue";
import { DEFAULT_DRAWING_COLOR, DEFAULT_DRAWING_FONT_SIZE, DEFAULT_DRAWING_STROKE_WIDTH } from "@/constants/defaults";
import { mapStores } from "pinia";
import { useEditLayerStore } from "@/stores/edit_layer_store";
import { EditLayerMode } from "@/types/map";

export default {
  name: "ToolsPanel",
  components: {
    EditLayerMenu,
    DrawMenu,
    MeasureMenu,
    SelectMenu,
  },
  props: {
    tool: String,
    editFeatureMode: String,
    color: Object,
    user: Object,
    map: Object,
    drawFeatures: Array,
    removedDrawFeatures: Array,
    config: Object,
    strokeWidth: Number,
    fontSize: Number,
    features: {
      type: Object,
      default: () => {
        return {
          selectarea: true,
          measure: true,
          draw: true,
        };
      },
    },
  },
  computed: {
    ...mapStores(useEditLayerStore),
  },
  data() {
    return {
      showMeasureMenu: false,
      showDrawMenu: false,
      showSelectMenu: false,
      showEditFeatureMenu: false,
      showLineWeightMenu: false,
      showFontSizeMenu: false,
      previousTool: "",
    };
  },
  watch: {
    // This code resets the color, stroke width, and font size to their default values whenever 'showDrawMenu' is turned off
    showDrawMenu: {
      handler(value) {
        if (!value) {
          this.$emit("set-color", DEFAULT_DRAWING_COLOR);
          this.$emit("set-tool", "");
          this.$emit("set-stroke-width", DEFAULT_DRAWING_STROKE_WIDTH);
          this.$emit("set-font-size", DEFAULT_DRAWING_FONT_SIZE);
        }
      },
    },
    showEditFeatureMenu: {
      handler(value) {
        if (!value) {
          this.editLayerStore.resetFeature();
        }
      },
    },
    "editLayerStore.editLayerMode": {
      handler(value) {
        if (value === EditLayerMode.EDIT) {
          this.showEditFeatureMenu = true;
        }
      },
    },
  },
  methods: {
    draw,
    toggleMeasure() {
      if (this.showSelectMenu) {
        this.showSelectMenu = false;
      }

      if (this.showDrawMenu) {
        this.showDrawMenu = false;
      }

      if (this.showEditFeatureMenu) {
        this.showEditFeatureMenu = false;
      }

      if (this.tool === "MEASURE_AREA" || this.tool === "MEASURE_LINE") {
        this.$emit("set-tool", "");
        return;
      }

      this.showMeasureMenu = !this.showMeasureMenu;
    },
    toggleSelectArea() {
      if (this.showMeasureMenu) {
        this.showMeasureMenu = false;
      }

      if (this.showDrawMenu) {
        this.showDrawMenu = false;
      }

      if (this.showEditFeatureMenu) {
        this.showEditFeatureMenu = false;
      }

      if (this.tool === "SELECT_AREA" || this.tool === "SELECT_CIRCLE" || this.tool === "SELECT_FEATURE") {
        this.resetAreaSelect();
        return;
      }

      this.showSelectMenu = !this.showSelectMenu;
    },
    setTool(chosenTool) {
      if (this.tool) {
        this.resetAreaSelect();
      }

      // Reset values on nextTick need to wait for resetAreaSelect to be finished.
      this.$nextTick(() => {
        this.$emit("set-tool", chosenTool);
        this.showMeasureMenu = false;
        this.showSelectMenu = false;
      });
    },
    toggleDraw() {
      if (this.showSelectMenu) {
        this.showSelectMenu = false;
      }

      if (this.showMeasureMenu) {
        this.showMeasureMenu = false;
      }

      if (this.showEditFeatureMenu) {
        this.showEditFeatureMenu = false;
      }

      this.$emit("set-tool", "");
      this.showDrawMenu = !this.showDrawMenu;
    },
    toggleEditLayer() {
      this.setTool("");
      this.resetAreaSelect();
      this.showSelectMenu = false;
      this.showMeasureMenu = false;
      this.showDrawMenu = false;
      this.showEditFeatureMenu = !this.showEditFeatureMenu;
      this.clearDrawing();
    },
    resetAreaSelect() {
      this.$emit("set-selected-area", null);
      this.$emit("set-tool", "");
    },
    setColor(color) {
      this.$emit("set-color", color);
    },
    setStrokeWidth(strokeWidth) {
      this.$emit("set-stroke-width", strokeWidth);
    },
    setFontSize(fontSize) {
      this.$emit("set-font-size", fontSize);
    },
    setInteraction(interaction) {
      this.$emit("set-interaction", interaction);
    },
    clearDrawing() {
      this.$emit("clear-draw");
    },
    disableDrawMenu() {
      this.showDrawMenu = false;
    },
    afterDraw(id) {
      this.$emit("drawing-saved", id);
    },
  },
};
</script>

<style lang="scss">
.tools-panel {
  position: relative;
}

.tools-panel__buttons {
  display: flex;
  background: white;
  border-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);

  & > .tools-panel__button-container {
    position: relative;

    &:first-child,
    &:first-child .tools-panel__button {
      border-radius: var(--radius-normal) 0 0 var(--radius-normal);
    }

    &:last-child,
    &:last-child .tools-panel__button {
      border-radius: 0 var(--radius-normal) var(--radius-normal) 0;
    }
    &:last-child .tools-panel__button--active {
      border-radius: 0 var(--radius-normal) 0 0;
    }

    &:not(:last-child) {
      border-right: 1px solid var(--color-grey-50);
    }
  }
}

.tools-panel__button {
  width: var(--width-button-large);
  height: var(--width-button-large);
  display: flex;
  align-items: center;
  justify-content: center;

  &--active {
    background: var(--color-primary);
    color: var(--color-white);
  }

  &--large {
    position: relative;
    width: 72px;
    height: var(--width-button-large);

    p {
      font-size: 14px;
      margin-left: 4px;
    }
  }

  &:disabled {
    color: var(--color-grey-80);
  }
}

.tools-panel__menu {
  right: 0;
  position: absolute;
  top: var(--width-button-large);
  padding: 6px 0;
  background: white;
  border-radius: var(--radius-small);
  box-shadow: var(--shadow-normal);
}

.tools-panel__list {
  button {
    display: block;
    width: 100%;
    color: black;
    text-decoration: none;
    padding: 4px 12px;
    font-size: var(--font-size-small);

    &:hover {
      background: var(--color-grey-40);
    }

    &:active {
      background: var(--color-grey-50);
    }
  }
}

.tools-panel__draw-bar {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  position: absolute;
  right: 0;
  box-shadow: var(--shadow-normal);
  border-radius: var(--radius-normal);
}

.tools-panel__draw-menu {
  position: relative;

  .tools-panel__button {
    border-radius: 0px !important;
  }
}

.tools-panel__button {
  border-right: 1px solid var(--color-grey-50);
}

.tools-panel__draw-options-menu {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  position: absolute;
  left: 0;
  margin-top: -1px;
  box-shadow: var(--shadow-normal);
  border-radius: var(--radius-small);

  ul {
    border-radius: var(--radius-small);
  }
}

.tools-panel__option {
  display: flex;
  flex-wrap: nowrap;
  gap: 4px;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  border-bottom: none !important;
  border-radius: 0 !important;
  width: 72px;

  &--rectangle {
    width: var(--width-button-large) !important;
    height: var(--width-button-large) !important;
  }

  &--block {
    display: block;
  }

  &--small-text {
    font-size: 14px !important;
  }

  &--middle-text {
    font-size: 18px !important;
  }

  &--large-text {
    font-size: 22px !important;
  }

  &--larger-text {
    font-size: 26px !important;
  }

  &--active {
    background-color: var(--color-grey-40);
    color: var(--color-primary);
  }

  &:hover {
    background: var(--color-grey-40);
  }

  &:active {
    background: var(--color-grey-50);
  }

  &:last-child {
    border-radius: 0 0 var(--radius-small) var(--radius-small) !important;
  }
}

@media (max-width: 576px) {
  .tools-panel__button {
    &--large {
      width: var(--width-button-large);

      p {
        display: none;
      }
    }
  }

  .tools-panel__draw-bar {
    display: grid;
    flex-basis: 20%;
    grid-template-columns: repeat(5, 1fr);
  }

  .tools-panel__draw-bar button:nth-child(-n + 5) {
    border-bottom: 1px solid var(--color-grey-50);
  }
}
</style>
