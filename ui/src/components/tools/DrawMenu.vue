<template>
  <div class="select-menu tools-panel__button-container !tw-border-r-0">
    <button
      v-tippy="{ placement: 'bottom' }"
      class="tools-panel__button"
      :class="{
        'tools-panel__button--active': showDrawMenu,
      }"
      content="Tekenen"
      aria-label="Tekenen"
      @click="toggleDraw"
    >
      <BrushIcon class="icon" />
    </button>

    <div v-if="showDrawMenu">
      <transition name="fade">
        <div class="tools-panel__draw-bar">
          <div class="tools-panel__draw-menu">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Teken punt"
              class="tools-panel__button"
              :class="{
                'tools-panel__button--active': tool === 'DRAW_POINT' || previousTool === 'DRAW_POINT',
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
                <div class="tools-panel__draw-options-menu">
                  <ul>
                    <li>
                      <button
                        v-tippy="{ placement: 'bottom' }"
                        aria-label="Teken punt met coordinaat"
                        class="tools-panel__option tools-panel__option--rectangle"
                        :class="{
                          'tools-panel__button--active':
                            tool === 'DRAW_COORDINATE' || previousTool === 'DRAW_COORDINATE',
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
          <div class="tools-panel__draw-menu">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Teken lijn"
              class="tools-panel__button"
              :class="{
                'tools-panel__button--active': tool === 'DRAW_LINE' || previousTool === 'DRAW_LINE',
              }"
              content="Teken lijn"
              @click="() => setTool('DRAW_LINE')"
            >
              <LineIcon />
            </button>
            <div v-if="showDrawMenu && (tool === 'DRAW_LINE' || previousTool === 'DRAW_LINE')">
              <transition name="fade">
                <div class="tools-panel__draw-options-menu">
                  <ul>
                    <li>
                      <button
                        v-tippy="{ placement: 'bottom' }"
                        content="Verwijder laatste punt"
                        aria-label="Verwijder laatste punt"
                        class="tools-panel__option tools-panel__option--rectangle"
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
          <div class="tools-panel__draw-menu">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Teken polygoon"
              class="tools-panel__button"
              :class="{
                'tools-panel__button--active': tool === 'DRAW_POLYGON' || previousTool === 'DRAW_POLYGON',
              }"
              content="Teken polygoon"
              @click="() => setTool('DRAW_POLYGON')"
            >
              <PolyGonIcon />
            </button>
            <div v-if="showDrawMenu && (tool === 'DRAW_POLYGON' || previousTool === 'DRAW_POLYGON')">
              <transition name="fade">
                <div class="tools-panel__draw-options-menu">
                  <ul>
                    <li>
                      <button
                        v-tippy="{ placement: 'bottom' }"
                        content="Verwijder laatste punt"
                        aria-label="Verwijder laatste punt"
                        class="tools-panel__option tools-panel__option--rectangle"
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
            class="tools-panel__button"
            :class="{
              'tools-panel__button--active': tool === 'DRAW_LABEL' || previousTool === 'DRAW_LABEL',
            }"
            content="Teken label"
            @click="() => setTool('DRAW_LABEL')"
          >
            <TextIcon />
          </button>
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Kies een kleur"
            class="tools-panel__button"
            content="Kies een kleur"
            @click="() => triggerColorPicker()"
          >
            <input ref="colorpicker" type="color" class="tools-panel__color-picker" @change="(e) => changeColor(e)" />
            <DropIcon
              class="tools-panel__color-picker-icon"
              :style="{ color: `rgb(${color.red}, ${color.green}, ${color.blue})` }"
            />
          </button>
          <div class="tools-panel__draw-menu">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Kies een tekstgrootte"
              class="tools-panel__button tools-panel__button--large"
              content="Kies een tekstgrootte"
              @click="toggleFontSizeMenu"
            >
              <FormatSizeIcon />
              <p>{{ fontSize }}px</p>
            </button>
            <div v-if="showDrawMenu && showFontSizeMenu">
              <transition name="fade">
                <div class="tools-panel__draw-options-menu">
                  <ul>
                    <li>
                      <button
                        aria-label="Kies kleine tekst"
                        class="tools-panel__option tools-panel__option--small-text tools-panel__option--block"
                        :class="{
                          'tools-panel__option--active': fontSize === 14,
                        }"
                        @click="() => changeFontSize(14)"
                      >
                        Klein
                      </button>
                    </li>
                    <li>
                      <button
                        aria-label="Kies middel tekst"
                        class="tools-panel__option tools-panel__option--middle-text tools-panel__option--block"
                        :class="{
                          'tools-panel__option--active': fontSize === 18,
                        }"
                        @click="() => changeFontSize(18)"
                      >
                        Middel
                      </button>
                    </li>
                    <li>
                      <button
                        aria-label="Kies grote tekst"
                        class="tools-panel__option tools-panel__option--large-text tools-panel__option--block"
                        :class="{
                          'tools-panel__option--active': fontSize === 22,
                        }"
                        @click="() => changeFontSize(22)"
                      >
                        Groot
                      </button>
                    </li>
                    <li>
                      <button
                        aria-label="Kies extra grote tekst"
                        class="tools-panel__option tools-panel__option--larger-text tools-panel__option--block"
                        :class="{
                          'tools-panel__option--active': fontSize === 26,
                        }"
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
          <div class="tools-panel__draw-menu">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Kies een lijndikte"
              class="tools-panel__button tools-panel__button--large"
              content="Kies een lijndikte"
              @click="toggleLineWeightMenu"
            >
              <LineWeightIcon />
              <p>{{ strokeWidth }}px</p>
            </button>
            <div v-if="showDrawMenu && showLineWeightMenu">
              <transition name="fade">
                <div class="tools-panel__draw-options-menu">
                  <ul>
                    <li>
                      <button
                        class="tools-panel__option"
                        aria-label="Kies lijndikte van 1px"
                        :class="{
                          'tools-panel__option--active': strokeWidth === 1,
                        }"
                        @click="() => changeStrokeWidth(1)"
                      >
                        <OnePxLineIcon />
                        1px
                      </button>
                    </li>
                    <li>
                      <button
                        class="tools-panel__option"
                        aria-label="Kies lijndikte van 2px"
                        :class="{
                          'tools-panel__option--active': strokeWidth === 2,
                        }"
                        @click="() => changeStrokeWidth(2)"
                      >
                        <TwoPxLineIcon />
                        2px
                      </button>
                    </li>
                    <li>
                      <button
                        class="tools-panel__option"
                        aria-label="Kies lijndikte van 3px"
                        :class="{
                          'tools-panel__option--active': strokeWidth === 3,
                        }"
                        @click="() => changeStrokeWidth(3)"
                      >
                        <ThreePxLineIcon />
                        3px
                      </button>
                    </li>
                    <li>
                      <button
                        class="tools-panel__option"
                        aria-label="Kies lijndikte van 4px"
                        :class="{
                          'tools-panel__option--active': strokeWidth === 4,
                        }"
                        @click="() => changeStrokeWidth(4)"
                      >
                        <FourPxLineIcon />
                        4px
                      </button>
                    </li>
                    <li>
                      <button
                        class="tools-panel__option"
                        aria-label="Kies lijndikte van 5px"
                        :class="{
                          'tools-panel__option--active': strokeWidth === 5,
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
            class="tools-panel__button"
            :disabled="drawFeatures.length < 1"
            content="Undo"
            @click="() => changeInteraction('UNDO')"
          >
            <UndoIcon />
          </button>
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Redo"
            class="tools-panel__button"
            :disabled="removedDrawFeatures.length < 1"
            content="Redo"
            @click="() => changeInteraction('REDO')"
          >
            <RedoIcon />
          </button>
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Verwijder tekening"
            class="tools-panel__button"
            content="Verwijder tekening"
            @click="clearDraw"
          >
            <DeleteIcon />
          </button>
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Sla tekening op"
            class="tools-panel__button"
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
import BrushIcon from "@/assets/icons/brush-icon.svg";

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
  toggleDraw: () => void;
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
  toggleDraw,
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

<style scoped lang="scss">
.tools-panel__draw-bar {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  position: absolute;
  right: 0;
  box-shadow: var(--shadow-normal);
  border-radius: var(--radius-normal);

  .tools-panel__button {
    border-radius: 0 !important;
  }
}

.tools-panel__draw-menu {
  position: relative;
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

.tools-panel__color-picker {
  visibility: hidden;
}

.tools-panel__color-picker-icon {
  border-radius: 999px;
  min-width: 16px;
  min-height: 16px;
  margin-right: 7px;
}
</style>
