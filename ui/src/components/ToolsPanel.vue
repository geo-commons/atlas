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
    </div>

    <div v-if="showSelectMenu" class="menu">
      <transition name="fade">
        <ul class="list">
          <li>
            <button aria-label="Selecteer gebied met behulp van cirkel" @click="() => setTool('SELECT_CIRCLE')">
              Cirkel
            </button>
          </li>
          <li>
            <button aria-label="Selecteer gebied met behulp van polygoon" @click="() => setTool('SELECT_AREA')">
              Polygoon
            </button>
          </li>
        </ul>
      </transition>
    </div>

    <div v-if="showMeasureMenu" class="menu">
      <transition name="fade">
        <ul class="list">
          <li>
            <button aria-label="Meet oppervlakte" @click="() => setTool('MEASURE_AREA')">Oppervlakte</button>
          </li>
          <li>
            <button aria-label="Meet afstand" @click="() => setTool('MEASURE_LINE')">Afstand</button>
          </li>
        </ul>
      </transition>
    </div>

    <div v-if="showDrawMenu">
      <transition name="fade">
        <div class="draw-toolbar">
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Teken punt"
            class="iconbutton"
            :class="{
              isActive: tool === 'DRAW_POINT',
            }"
            content="Teken punt"
            @click="() => setTool('DRAW_POINT')"
          >
            <DotIcon />
          </button>
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Teken lijn"
            class="iconbutton"
            :class="{
              isActive: tool === 'DRAW_LINE',
            }"
            content="Teken lijn"
            @click="() => setTool('DRAW_LINE')"
          >
            <LineIcon />
          </button>
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Teken polygoon"
            class="iconbutton"
            :class="{
              isActive: tool === 'DRAW_POLYGON',
            }"
            content="Teken polygoon"
            @click="() => setTool('DRAW_POLYGON')"
          >
            <PolyGonIcon />
          </button>
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Teken label"
            class="iconbutton"
            :class="{
              isActive: tool === 'DRAW_LABEL',
            }"
            content="Teken label"
            @click="() => setTool('DRAW_LABEL')"
          >
            <TextIcon />
          </button>
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Kies een kleur"
            class="iconbutton"
            content="Kies een kleur"
            @click="() => triggerColorPicker()"
          >
            <input ref="colorpicker" type="color" class="colorpicker" @change="(e) => setColor(e)" />
            <DropIcon class="colorpicker-icon" :style="{ color: `rgb(${color.red}, ${color.green}, ${color.blue})` }" />
          </button>
          <div class="menu-wrapper">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Kies een tekst grote"
              class="iconbutton lineweight-toggle"
              content="Kies een tekst grote"
              @click="toggleFontSizeMenu"
            >
              <FormatSizeIcon />
              <p>{{ fontSize }}px</p>
            </button>
            <div v-if="showDrawMenu && showFontSizeMenu">
              <transition name="fade">
                <div class="detail-menu">
                  <ul class="list">
                    <li>
                      <button
                        aria-label="Kies kleine tekst"
                        :class="{
                          isActive: fontSize === 14,
                        }"
                        class="text-button small-text"
                        @click="() => setFontSize(14)"
                      >
                        Klein
                      </button>
                    </li>
                    <li>
                      <button
                        aria-label="Kies middel tekst"
                        :class="{
                          isActive: fontSize === 18,
                        }"
                        class="text-button middle-text"
                        @click="() => setFontSize(18)"
                      >
                        Middel
                      </button>
                    </li>
                    <li>
                      <button
                        aria-label="Kies grote tekst"
                        :class="{
                          isActive: fontSize === 22,
                        }"
                        class="text-button large-text"
                        @click="() => setFontSize(22)"
                      >
                        Groot
                      </button>
                    </li>
                    <li>
                      <button
                        aria-label="Kies extra grote tekst"
                        :class="{
                          isActive: fontSize === 26,
                        }"
                        class="text-button larger-text"
                        @click="() => setFontSize(26)"
                      >
                        Extra groot
                      </button>
                    </li>
                  </ul>
                </div>
              </transition>
            </div>
          </div>
          <div class="menu-wrapper">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Kies een lijndikte"
              class="iconbutton lineweight-toggle"
              content="Kies een lijndikte"
              @click="toggleLineWeightMenu"
            >
              <LineWeightIcon />
              <p>{{ strokeWidth }}px</p>
            </button>
            <div v-if="showDrawMenu && showLineWeightMenu">
              <transition name="fade">
                <div class="detail-menu">
                  <ul class="list">
                    <li>
                      <button
                        aria-label="Kies lijndikte van 1px"
                        :class="{
                          isActive: strokeWidth === 1,
                        }"
                        @click="() => setStrokeWidth(1)"
                      >
                        <OnePxLineIcon />
                        1px
                      </button>
                    </li>
                    <li>
                      <button
                        aria-label="Kies lijndikte van 2px"
                        :class="{
                          isActive: strokeWidth === 2,
                        }"
                        @click="() => setStrokeWidth(2)"
                      >
                        <TwoPxLineIcon />
                        2px
                      </button>
                    </li>
                    <li>
                      <button
                        aria-label="Kies lijndikte van 3px"
                        :class="{
                          isActive: strokeWidth === 3,
                        }"
                        @click="() => setStrokeWidth(3)"
                      >
                        <ThreePxLineIcon />
                        3px
                      </button>
                    </li>
                    <li>
                      <button
                        aria-label="Kies lijndikte van 4px"
                        :class="{
                          isActive: strokeWidth === 4,
                        }"
                        @click="() => setStrokeWidth(4)"
                      >
                        <FourPxLineIcon />
                        4px
                      </button>
                    </li>
                    <li>
                      <button
                        aria-label="Kies lijndikte van 5px"
                        :class="{
                          isActive: strokeWidth === 5,
                        }"
                        @click="() => setStrokeWidth(5)"
                      >
                        <FivePxLineIcon />
                        5px
                      </button>
                    </li>
                  </ul>
                </div>
              </transition>
            </div>
          </div>
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Undo"
            class="iconbutton"
            :disabled="drawFeatures.length < 1"
            content="Undo"
            @click="() => setInteraction('UNDO')"
          >
            <UndoIcon />
          </button>
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Redo"
            class="iconbutton"
            :disabled="removedDrawFeatures.length < 1"
            content="Redo"
            @click="() => setInteraction('REDO')"
          >
            <RedoIcon />
          </button>
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Verwijder tekening"
            class="iconbutton"
            content="Verwijder tekening"
            @click="clearDraw"
          >
            <DeleteIcon />
          </button>
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Sla tekening op"
            class="iconbutton"
            content="Sla tekening op"
            @click="saveDrawing"
          >
            <SaveIcon />
          </button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import GeoJSON from "ol/format/GeoJSON";
import RulerIcon from "../assets/icons/ruler-icon.svg";
import AreaSelectIcon from "../assets/icons/area-select-icon.svg";
import BrushIcon from "../assets/icons/brush-icon.svg";
import DotIcon from "../assets/icons/dot-icon.svg";
import LineIcon from "../assets/icons/line-icon.svg";
import RedoIcon from "../assets/icons/redo-icon.svg";
import UndoIcon from "../assets/icons/undo-icon.svg";
import TextIcon from "../assets/icons/text-icon.svg";
import DeleteIcon from "../assets/icons/delete-icon.svg";
import SaveIcon from "../assets/icons/save-icon.svg";
import PolyGonIcon from "../assets/icons/polygon-icon.svg";
import DropIcon from "../assets/icons/drop-icon.svg";
import LineWeightIcon from "../assets/icons/lineweight-icon.svg";
import OnePxLineIcon from "../assets/icons/1px-line-icon.svg";
import TwoPxLineIcon from "../assets/icons/2px-line-icon.svg";
import ThreePxLineIcon from "../assets/icons/3px-line-icon.svg";
import FourPxLineIcon from "../assets/icons/4px-line-icon.svg";
import FivePxLineIcon from "../assets/icons/5px-line-icon.svg";
import FormatSizeIcon from "../assets/icons/format-size-icon.svg";
import hexRgb from "hex-rgb";
import draw from "@/utils/draw";

export default {
  name: "ToolsPanel",
  components: {
    RulerIcon,
    AreaSelectIcon,
    BrushIcon,
    DotIcon,
    LineIcon,
    UndoIcon,
    RedoIcon,
    TextIcon,
    DeleteIcon,
    SaveIcon,
    PolyGonIcon,
    DropIcon,
    LineWeightIcon,
    OnePxLineIcon,
    TwoPxLineIcon,
    ThreePxLineIcon,
    FourPxLineIcon,
    FivePxLineIcon,
    FormatSizeIcon,
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
    clearDraw() {
      this.$emit("set-tool", "");

      const result = confirm("Weet je zeker dat je de tekening wilt verwijderen?");
      if (result) {
        this.$emit("clear-draw");
        this.showDrawMenu = !this.showDrawMenu;
      }
    },
    setInteraction(interaction) {
      this.$emit("setInteraction", interaction);
      this.$emit("set-tool", "");
    },
    async saveDrawing() {
      this.$emit("set-tool", "");

      const geojsonFormat = new GeoJSON();
      const result = await fetch(`/atlas/api/v1/drawings/`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: geojsonFormat.writeFeatures(this.drawFeatures),
      });

      const resultData = await result.json();

      if (result.ok) {
        this.$emit("drawing-saved", resultData.id);
        this.showDrawMenu = !this.showDrawMenu;
      }
    },
    resetAreaSelect() {
      this.$emit("set-selected-area", null);
      this.$emit("set-tool", "");
    },
    triggerColorPicker() {
      this.$emit("set-tool", "");
      this.$refs.colorpicker.click();
    },
    setColor(e) {
      this.$emit("set-color", hexRgb(e.target.value));
    },
    toggleLineWeightMenu() {
      this.$emit("set-tool", "");
      this.showLineWeightMenu = !this.showLineWeightMenu;
      this.showFontSizeMenu = false;
    },
    toggleFontSizeMenu() {
      this.$emit("set-tool", "");
      this.showFontSizeMenu = !this.showFontSizeMenu;
      this.showLineWeightMenu = false;
    },
    setStrokeWidth(strokeWidth) {
      this.showLineWeightMenu = !this.showLineWeightMenu;
      this.$emit("set-stroke-width", strokeWidth);
    },
    setFontSize(fontSize) {
      this.showFontSizeMenu = !this.showFontSizeMenu;
      this.$emit("set-font-size", fontSize);
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

.menu-wrapper {
  position: relative;
}

.menu-wrapper .iconbutton {
  border-radius: 0px !important;
}

.iconbutton.isActive {
  color: var(--color-primary);
}

.menu {
  position: absolute;
  top: var(--width-button-large);
  padding: 6px 0;
  background: white;
  border-radius: var(--radius-small);
  border-top-right-radius: 0;
  box-shadow: var(--shadow-normal);
}

.list a,
.list button {
  display: block;
  width: 100%;
  color: black;
  text-decoration: none;
  padding: 4px 12px;
  font-size: var(--font-size-small);
}

.list a:hover,
.list button:hover {
  background: var(--color-grey-40);
}

.list a:active,
.list button:active {
  background: var(--color-grey-50);
}

.draw-toolbar {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  position: absolute;
  right: 0;
  margin-top: 12px;
  box-shadow: var(--shadow-normal);
  border-radius: var(--radius-normal);
}

.iconbutton.lineweight-toggle {
  position: relative;
  width: 72px;
  height: var(--width-button-large);
}

.iconbutton.lineweight-toggle p {
  font-size: 14px;
  margin-left: 4px;
}

.iconbutton:disabled {
  color: var(--color-grey-80);
}

.detail-menu {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  position: absolute;
  left: 0;
  margin-top: -1px;
  box-shadow: var(--shadow-normal);
  border-radius: var(--radius-small);
}

.detail-menu .list {
  border-radius: var(--radius-small);
}

.detail-menu button {
  display: flex;
  flex-wrap: nowrap;
  gap: 4px;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  border-bottom: none !important;
  border-radius: 0 !important;
}

.detail-menu .text-button {
  display: block;
}

.detail-menu button:last-child {
  border-radius: 0 0 var(--radius-small) var(--radius-small) !important;
}

.detail-menu button.isActive {
  background-color: var(--color-grey-40);
  color: var(--color-primary);
}

.detail-menu button:last-child {
  border-radius: 0 0 var(--radius-normal) var(--radius-normal);
}

.draw-toolbar button:first-child {
  border-radius: var(--radius-normal) 0 0 var(--radius-normal);
}

.draw-toolbar button:last-child {
  border-radius: 0 var(--radius-normal) var(--radius-normal) 0;
}

.draw-toolbar .iconbutton.isActive {
  color: var(--color-primary);
  background: var(--color-grey-40);
}

.colorpicker {
  visibility: hidden;
}

.colorpicker-icon {
  border-radius: 999px;
  min-width: 16px;
  min-height: 16px;
  margin-right: 7px;
}

.small-text {
  font-size: 14px !important;
}

.middle-text {
  font-size: 18px !important;
}

.large-text {
  font-size: 22px !important;
}

.larger-text {
  font-size: 26px !important;
}

@media (max-width: 576px) {
  .draw-toolbar {
    display: grid;
    flex-basis: 20%;
    grid-template-columns: repeat(5, 1fr);
  }

  .draw-toolbar button:first-child {
    border-radius: var(--radius-normal) 0 0 0;
  }

  .draw-toolbar button:nth-child(5) {
    border-radius: 0 var(--radius-normal) 0 0;
  }

  .draw-toolbar button:nth-child(6) {
    border-radius: 0 0 0 var(--radius-normal);
  }

  .draw-toolbar button:last-child {
    border-radius: 0 0 var(--radius-normal) 0;
  }

  .iconbutton.lineweight-toggle {
    width: var(--width-button-large);
  }

  .iconbutton.lineweight-toggle p {
    display: none;
  }

  .draw-toolbar button:nth-child(-n + 5) {
    border-bottom: 1px solid var(--color-grey-50);
  }
}
</style>
