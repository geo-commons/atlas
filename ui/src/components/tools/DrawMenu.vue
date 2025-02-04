<template>
  <div v-if="showDrawMenu">
    <transition name="fade">
      <div class="draw-toolbar">
        <div class="menu-wrapper">
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Teken punt"
            class="iconbutton"
            :class="{
              isActive: tool === 'DRAW_POINT' || previousTool === 'DRAW_POINT',
            }"
            content="Teken punt"
            @click="() => setTool('DRAW_POINT')"
          >
            <DotIcon />
          </button>
          <div
            v-if="
              showDrawMenu &&
              (tool === 'DRAW_POINT' ||
                previousTool === 'DRAW_POINT' ||
                tool === 'DRAW_COORDINATE' ||
                previousTool === 'DRAW_COORDINATE')
            "
          >
            <transition name="fade">
              <div class="detail-menu">
                <ul class="list">
                  <li>
                    <button
                      v-tippy="{ placement: 'bottom' }"
                      aria-label="Teken punt met coordinaat"
                      class="text-button small-text is-fixed-size"
                      :class="{
                        isActive: tool === 'DRAW_COORDINATE' || previousTool === 'DRAW_COORDINATE',
                      }"
                      content="Teken punt met coordinaat"
                      @click="() => setTool('DRAW_COORDINATE')"
                    >
                      <AddLocationIcon />
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
            aria-label="Teken lijn"
            class="iconbutton"
            :class="{
              isActive: tool === 'DRAW_LINE' || previousTool === 'DRAW_LINE',
            }"
            content="Teken lijn"
            @click="() => setTool('DRAW_LINE')"
          >
            <LineIcon />
          </button>
          <div v-if="showDrawMenu && (tool === 'DRAW_LINE' || previousTool === 'DRAW_LINE')">
            <transition name="fade">
              <div class="detail-menu">
                <ul class="list">
                  <li>
                    <button
                      v-tippy="{ placement: 'bottom' }"
                      content="Verwijder laatste punt"
                      aria-label="Verwijder laatste punt"
                      class="text-button small-text is-fixed-size"
                      @click="() => emitKeyDown()"
                    >
                      <UndoIcon />
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
            aria-label="Teken polygoon"
            class="iconbutton"
            :class="{
              isActive: tool === 'DRAW_POLYGON' || previousTool === 'DRAW_POLYGON',
            }"
            content="Teken polygoon"
            @click="() => setTool('DRAW_POLYGON')"
          >
            <PolyGonIcon />
          </button>
          <div v-if="showDrawMenu && (tool === 'DRAW_POLYGON' || previousTool === 'DRAW_POLYGON')">
            <transition name="fade">
              <div class="detail-menu">
                <ul class="list">
                  <li>
                    <button
                      v-tippy="{ placement: 'bottom' }"
                      content="Verwijder laatste punt"
                      aria-label="Verwijder laatste punt"
                      class="text-button small-text is-fixed-size"
                      @click="() => emitKeyDown()"
                    >
                      <UndoIcon />
                    </button>
                  </li>
                </ul>
              </div>
            </transition>
          </div>
        </div>
        <button
          v-tippy="{ placement: 'bottom' }"
          aria-label="Teken label"
          class="iconbutton"
          :class="{
            isActive: tool === 'DRAW_LABEL' || previousTool === 'DRAW_LABEL',
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
          <input ref="colorpicker" type="color" class="colorpicker" @change="(e) => changeColor(e)" />
          <DropIcon class="colorpicker-icon" :style="{ color: `rgb(${color.red}, ${color.green}, ${color.blue})` }" />
        </button>
        <div class="menu-wrapper">
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Kies een tekstgrootte"
            class="iconbutton lineweight-toggle"
            content="Kies een tekstgrootte"
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
                      @click="() => changeFontSize(14)"
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
                      @click="() => changeFontSize(18)"
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
                      @click="() => changeFontSize(22)"
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
                      @click="() => changeFontSize(26)"
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
                      @click="() => changeStrokeWidth(1)"
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
                      @click="() => changeStrokeWidth(2)"
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
                      @click="() => changeStrokeWidth(3)"
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
                      @click="() => changeStrokeWidth(4)"
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
                      @click="() => changeStrokeWidth(5)"
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
          @click="() => changeInteraction('UNDO')"
        >
          <UndoIcon />
        </button>
        <button
          v-tippy="{ placement: 'bottom' }"
          aria-label="Redo"
          class="iconbutton"
          :disabled="removedDrawFeatures.length < 1"
          content="Redo"
          @click="() => changeInteraction('REDO')"
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
</template>

<script setup lang="ts">
import AddLocationIcon from "@/assets/icons/add-location-icon.svg";
import FormatSizeIcon from "@/assets/icons/format-size-icon.svg";
import PolyGonIcon from "@/assets/icons/polygon-icon.svg";
import SaveIcon from "@/assets/icons/save-icon.svg";
import OnePxLineIcon from "@/assets/icons/1px-line-icon.svg";
import DotIcon from "@/assets/icons/dot-icon.svg";
import ThreePxLineIcon from "@/assets/icons/3px-line-icon.svg";
import DeleteIcon from "@/assets/icons/delete-icon.svg";
import UndoIcon from "@/assets/icons/undo-icon.svg";
import LineWeightIcon from "@/assets/icons/lineweight-icon.svg";
import RedoIcon from "@/assets/icons/redo-icon.svg";
import TwoPxLineIcon from "@/assets/icons/2px-line-icon.svg";
import LineIcon from "@/assets/icons/line-icon.svg";
import FivePxLineIcon from "@/assets/icons/5px-line-icon.svg";
import DropIcon from "@/assets/icons/drop-icon.svg";
import FourPxLineIcon from "@/assets/icons/4px-line-icon.svg";
import TextIcon from "@/assets/icons/text-icon.svg";
import hexRgb, { RgbaObject } from "hex-rgb";
import { ref } from "vue";
import GeoJSON from "ol/format/GeoJSON";
import Cookies from "js-cookie";

interface DrawMenuProps {
  showDrawMenu: boolean;
  tool: string;
  color: RgbaObject;
  strokeWidth: number;
  fontSize: number;
  drawFeatures: Array<any>;
  removedDrawFeatures: Array<any>;
  setTool: (tool: string) => void;
  setColor: (color: RgbaObject) => void;
  setStrokeWidth: (strokeWidth: number) => void;
  setFontSize: (fontSize: number) => void;
  setInteraction: (interaction: "REDO" | "UNDO") => void;
  clearDrawing: () => void;
  disableDrawMenu: () => void;
  afterDraw: (id: string) => void;
}

const {
  showDrawMenu,
  tool,
  color,
  strokeWidth,
  fontSize,
  drawFeatures,
  removedDrawFeatures,
  setTool,
  setColor,
  setStrokeWidth,
  setFontSize,
  setInteraction,
  clearDrawing,
  disableDrawMenu,
  afterDraw,
} = defineProps<DrawMenuProps>();

const previousTool = ref<string>("");
const showLineWeightMenu = ref<boolean>(false);
const showFontSizeMenu = ref<boolean>(false);

const colorpicker = ref<HTMLInputElement | null>(null);

const triggerColorPicker = () => {
  previousTool.value = tool;
  setTool("");

  colorpicker.value?.click();
};

const changeColor = (e: Event) => {
  setColor(hexRgb((e.target as HTMLInputElement).value));
  setTool(previousTool.value);
  previousTool.value = "";
};

const toggleLineWeightMenu = () => {
  previousTool.value = tool;
  setTool("");
  showLineWeightMenu.value = !showLineWeightMenu.value;
  showFontSizeMenu.value = false;
};

const toggleFontSizeMenu = () => {
  previousTool.value = tool;
  setTool("");
  showFontSizeMenu.value = !showFontSizeMenu.value;
  showLineWeightMenu.value = false;
};

const changeStrokeWidth = (strokeWidth: number) => {
  showLineWeightMenu.value = !showLineWeightMenu.value;
  setStrokeWidth(strokeWidth);
  setTool(previousTool.value);
  previousTool.value = "";
};

const changeFontSize = (fontSize: number) => {
  showFontSizeMenu.value = !showFontSizeMenu.value;
  setFontSize(fontSize);
  setTool(previousTool.value);
  previousTool.value = "";
};

const emitKeyDown = () => {
  const keyDownEvent = new KeyboardEvent("keydown", { key: "Backspace" });

  document.dispatchEvent(keyDownEvent);
};

const clearDraw = () => {
  setTool("");

  const result = confirm("Weet je zeker dat je de tekening wilt verwijderen?");
  if (result) {
    clearDrawing();
    disableDrawMenu();
  }
};

const changeInteraction = (interaction: "REDO" | "UNDO") => {
  setInteraction(interaction);
  setTool("");
};

const saveDrawing = async () => {
  setTool("");

  const geojsonFormat = new GeoJSON();
  const result = await fetch(`/atlas/api/v1/drawings/`, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": Cookies.get("csrftoken") || "",
    },
    body: geojsonFormat.writeFeatures(drawFeatures),
  });

  const resultData = await result.json();

  if (result.ok) {
    afterDraw(resultData.id);
    disableDrawMenu();
  }
};
</script>

<style scoped>
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

.iconbutton:disabled {
  color: var(--color-grey-80);
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

.detail-menu button.is-fixed-size {
  width: var(--width-button-large);
  height: var(--width-button-large);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 20;
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
