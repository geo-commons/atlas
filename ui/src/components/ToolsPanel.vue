<template>
  <div class="wrapper">
    <div class="buttons" :class="{ showMeasureMenu, showDrawMenu }">
      <button
        v-if="features.selectarea"
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton __inverse"
        :class="{ isActive: tool === 'SELECT_AREA' }"
        content="Selecteer gebied"
        aria-label="Selecteer gebied"
        @click="toggleSelectArea"
      >
        <AreaSelectIcon class="icon __medium" />
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
          isActive: tool === 'DRAW_POINT' || tool === 'DRAW_LINE' || tool === 'DRAW_POLYGON' || tool === 'DRAW_LABEL',
        }"
        content="Tekenen"
        aria-label="Tekenen"
        @click="toggleDraw"
      >
        <BrushIcon class="icon" />
      </button>
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

    <div v-if="showDrawMenu" class="menu">
      <transition name="fade">
        <ul class="list">
          <li>
            <button aria-label="Teken punt" @click="() => setTool('DRAW_POINT')">Teken punt</button>
          </li>
          <li>
            <button aria-label="Teken lijn" @click="() => setTool('DRAW_LINE')">Teken lijn</button>
          </li>
          <li>
            <button aria-label="Teken polygoon" @click="() => setTool('DRAW_POLYGON')">Teken polygoon</button>
          </li>
          <li>
            <button aria-label="Teken label" @click="() => setTool('DRAW_LABEL')">Teken label</button>
          </li>
          <li>
            <button aria-label="Verwijder tekening" @click="clearDraw">Verwijder tekening</button>
            <button aria-label="Sla tekening op" @click="saveDrawing">Sla tekening op</button>
          </li>
        </ul>
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

export default {
  name: "ToolsPanel",
  components: {
    RulerIcon,
    AreaSelectIcon,
    BrushIcon,
  },
  props: {
    tool: String,
    user: Object,
    map: Object,
    drawFeatures: Array,
    config: Object,
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
      selectAreaToggled: false,
    };
  },
  methods: {
    /*
     * Note: the interaction between toggling select area and the dropdown menus of draw and measure seems to have weird side effects.
     *       It seems to be working with $nextTick() as it is implemented right now but, it might be nice to refactor this after we implement
     *       select area to also support selecting by radius. After we have implemented that all options work very similar therefor,
     *       we should be able to simplify things a little.
     * */
    toggleMeasure() {
      if (this.tool) {
        this.resetAreaSelect();
        return;
      }

      this.showMeasureMenu = !this.showMeasureMenu;
    },
    toggleSelectArea() {
      this.selectAreaToggled = !this.selectAreaToggled;

      if (this.tool) {
        this.resetAreaSelect();
      }

      this.$nextTick(() => {
        if (this.selectAreaToggled) {
          this.$emit("set-tool", "SELECT_AREA");
        }
      });
    },
    setTool(chosenTool) {
      if (this.tool) {
        this.resetAreaSelect();
      }

      this.$nextTick(() => {
        this.selectAreaToggled = false;
        this.$emit("set-tool", chosenTool);
        this.showMeasureMenu = false;
        this.showDrawMenu = false;
      });
    },
    toggleDraw() {
      if (
        this.tool === "DRAW_POINT" ||
        this.tool === "DRAW_LINE" ||
        this.tool === "DRAW_POLYGON" ||
        this.tool === "DRAW_LABEL"
      ) {
        this.$emit("set-tool", "");
      } else {
        this.showDrawMenu = !this.showDrawMenu;
      }
    },
    clearDraw() {
      const result = confirm("Weet je zeker dat je de tekening wilt verwijderen?");
      if (result) {
        this.$emit("clear-draw");
        this.showDrawMenu = !this.showDrawMenu;
      }
    },
    async saveDrawing() {
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
}

.iconbutton:not(:last-child) {
  border-right: 1px solid var(--color-grey-50);
}

.iconbutton.isActive {
  color: var(--color-primary);
}

.menu {
  position: absolute;
  top: var(--width-button-large);
  right: 0;
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
</style>
