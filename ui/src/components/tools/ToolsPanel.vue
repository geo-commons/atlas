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
    </div>
  </div>
</template>

<script>
import draw from "@/utils/draw";
import SelectMenu from "@/components/tools/SelectMenu.vue";
import MeasureMenu from "@/components/tools/MeasureMenu.vue";
import DrawMenu from "@/components/tools/DrawMenu.vue";

export default {
  name: "ToolsPanel",
  components: {
    DrawMenu,
    MeasureMenu,
    SelectMenu,
  },
  props: {
    tool: String,
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
  data() {
    return {
      showMeasureMenu: false,
      showDrawMenu: false,
      showSelectMenu: false,
      showLineWeightMenu: false,
      showFontSizeMenu: false,
      previousTool: "",
    };
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

      if (this.tool === "SELECT_AREA" || this.tool === "SELECT_CIRCLE") {
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

      if (
        this.tool === "DRAW_POINT" ||
        this.tool === "DRAW_LINE" ||
        this.tool === "DRAW_POLYGON" ||
        this.tool === "DRAW_LABEL"
      ) {
        this.$emit("set-tool", "");
        this.showDrawMenu = !this.showDrawMenu;
      } else {
        this.showDrawMenu = !this.showDrawMenu;
      }
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
  overflow: hidden;
  border-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);
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

  &:not(:last-child) {
    border-right: 1px solid var(--color-grey-50);
  }
}

.tools-panel__menu {
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

@media (max-width: 576px) {
  .tools-panel__button {
    &--large {
      width: var(--width-button-large);

      p {
        display: none;
      }
    }
  }
}
</style>
