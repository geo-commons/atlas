<template>
  <div class="wrapper">
    <div class="buttons" :class="{ showMeasureMenu, showDrawMenu }">
      <button
        v-if="features.selectarea"
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton __inverse"
        :class="{ isActive: tool === 'SELECT_AREA' || tool === 'SELECT_CIRCLE' }"
        content="Selecteer gebied"
        aria-label="Selecteer gebied"
        @click="toggleSelectArea"
      >
        <AreaSelectIcon class="icon __smedium" />
      </button>

      <button
        v-if="features.measure"
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton __inverse"
        :class="{
          isActive: tool === 'MEASURE_AREA' || tool === 'MEASURE_LINE',
        }"
        content="Opmeten"
        aria-label="Opmeten"
        @click="toggleMeasure"
      >
        <RulerIcon class="icon" />
      </button>

      <button
        v-if="config && config.features.draw && features.draw && user"
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton __inverse"
        :class="{
          isActive: showDrawMenu,
        }"
        content="Tekenen"
        aria-label="Tekenen"
        @click="toggleDraw"
      >
        <BrushIcon class="icon" />
      </button>

      <button
        v-if="config && config.features.edit_layer_features && features.edit_layer_features && user"
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton __inverse"
        :class="{
          isActive: showAddFeatureMenu,
        }"
        content="Laag objecten bewerken"
        aria-label="Laag objecten bewerken"
        @click="toggleAddFeature"
      >
        <EditLocationIcon class="icon" />
      </button>
    </div>

    <SelectMenu :show-select-menu="showSelectMenu" :set-tool="setTool" />

    <MeasureMenu :show-measure-menu="showMeasureMenu" :set-tool="setTool" />

    <DrawMenu
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
    />
  </div>
</template>

<script>
import RulerIcon from "../../assets/icons/ruler-icon.svg";
import AreaSelectIcon from "../../assets/icons/area-select-icon.svg";
import BrushIcon from "../../assets/icons/brush-icon.svg";
import EditLocationIcon from "../../assets/icons/edit-location-icon.svg";
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
    RulerIcon,
    AreaSelectIcon,
    BrushIcon,
    EditLocationIcon,
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
          edit_layer_features: true,
        };
      },
    },
  },
  data() {
    return {
      showMeasureMenu: false,
      showDrawMenu: false,
      showSelectMenu: false,
      showAddFeatureMenu: false,
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
      this.showSelectMenu = false;
      this.showMeasureMenu = false;
      this.showAddFeatureMenu = false;

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
    toggleAddFeature() {
      this.showSelectMenu = false;
      this.showMeasureMenu = false;
      this.showDrawMenu = false;
      this.showAddFeatureMenu = !this.showAddFeatureMenu;
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

<style scoped>
.wrapper {
  position: relative;
}

.buttons {
  display: flex;
  background: white;
  overflow: hidden;
  border-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);
}

.buttons.showMeasureMenu {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.iconbutton {
  width: var(--width-button-large);
  height: var(--width-button-large);
  display: flex;
  align-items: center;
  justify-content: center;
}

.iconbutton:not(:last-child),
.menu-wrapper .iconbutton {
  border-right: 1px solid var(--color-grey-50);
}

.iconbutton.isActive {
  color: var(--color-primary);
}

.iconbutton:disabled {
  color: var(--color-grey-80);
}
</style>
