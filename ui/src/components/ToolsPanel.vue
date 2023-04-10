<template>
  <div class="wrapper">
    <div class="buttons" :class="{ showDrawMenu, showMeasureMenu }">
      <button
        v-if="this.features.selectarea"
        class="iconbutton"
        :class="{ isActive: tool === 'SELECT_AREA' }"
        @click="toggleSelectArea"
        v-tippy="{ placement: 'bottom' }"
        content="Selecteer gebied"
        aria-label="Selecteer gebied"
      >
        <svg width="18" height="18" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M14 2h-2V0h2v2zm-2 16h2v-2.59L16.59 18 18 16.59 15.41 14H18v-2h-6v6zm4-12h2V4h-2v2zm0 4h2V8h-2v2zm-8 8h2v-2H8v2zM4 2h2V0H4v2zM0 14h2v-2H0v2zm2 4v-2H0c0 1.1.9 2 2 2zM16 0v2h2c0-1.1-.9-2-2-2zM8 2h2V0H8v2zM0 6h2V4H0v2zm4 12h2v-2H4v2zm-4-8h2V8H0v2zm0-8h2V0C.9 0 0 .9 0 2z"
            fill="currentColor"
            fill-rule="nonzero"
          />
        </svg>
      </button>

      <button
        v-if="this.features.draw"
        class="iconbutton"
        :class="{ isActive: tool === 'DRAW_POINT' || tool === 'DRAW_LINE' || tool === 'DRAW_POLYGON' || tool === 'DRAW_CIRCLE' || tool === 'DRAW_LABEL' }"
        @click="toggleDraw"
        v-tippy="{ placement: 'bottom' }"
        content="Tekenen"
        aria-label="Tekenen"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 96 960 960"
        >
          <path
            fill="currentColor"
            d="M215 939q-33.835 0-66.917-11.5Q115 916 90 890q35-12 50-35t15-62q0-43.75 30.676-74.375Q216.353 688 260.176 688 304 688 334.5 718.625T365 793q0 64-43.5 105T215 939Zm0-60q35 0 62.5-25t27.5-61q0-20-12.5-32.5T260 748q-20 0-32.5 12.5T215 793q0 39-8.5 57.5T175 873q6 1 20 3.5t20 2.5Zm230-177-90-95 376-376q14-14 31-14.5t32 14.5l29 29q15 15 14.5 32.5T823 324L445 702Zm-185 91Z"
          />
        </svg>
      </button>

      <button
        v-if="this.features.measure"
        class="iconbutton"
        :class="{
          isActive: tool === 'MEASURE_AREA' || tool === 'MEASURE_LINE',
        }"
        @click="toggleMeasure"
        v-tippy="{ placement: 'bottom' }"
        content="Opmeten"
        aria-label="Opmeten"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="24"
          viewBox="0 0 24 24"
          width="24"
        >
          <path d="M0 0h24v24H0z" fill="none" />
          <path
            fill="currentColor"
            d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 10H3V8h2v4h2V8h2v4h2V8h2v4h2V8h2v4h2V8h2v8z"
          />
        </svg>
      </button>
    </div>

    <div class="menu" v-if="showMeasureMenu">
      <transition name="fade">
        <ul class="list">
          <li>
            <button
              @click="() => setTool('MEASURE_AREA')"
              aria-label="Meet oppervlakte"
            >
              Oppervlakte
            </button>
          </li>
          <li>
            <button
              @click="() => setTool('MEASURE_LINE')"
              aria-label="Meet afstand"
            >
              Afstand
            </button>
          </li>
        </ul>
      </transition>
    </div>

    <div class="menu" v-if="showDrawMenu">
      <transition name="fade">
        <ul class="list">
          <li>
            <button
              @click="() => setTool('DRAW_POINT')"
              aria-label="Teken punt"
            >
              Teken punt
            </button>
          </li>
          <li>
            <button @click="() => setTool('DRAW_LINE')" aria-label="Teken lijn">
              Teken lijn
            </button>
          </li>
          <li>
            <button
              @click="() => setTool('DRAW_POLYGON')"
              aria-label="Teken polygoon"
            >
              Teken polygoon
            </button>
          </li>
          <li>
            <button
              @click="() => setTool('DRAW_CIRCLE')"
              aria-label="Teken cirkel"
            >
              Teken cirkel
            </button>
          </li>
          <li>
            <button
              @click="() => setTool('DRAW_LABEL')"
              aria-label="Teken label"
            >
              Teken label
            </button>
          </li>
          <li>
            <button
              @click="clearDraw"
              aria-label="Verwijder tekening"
            >
              Verwijder tekening
            </button>
          </li>
        </ul>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: "ToolsPanel",
  data() {
    return {
      showMeasureMenu: false,
      showDrawMenu: false,
    };
  },
  methods: {
    toggleDraw() {
      if (this.tool === "DRAW_POINT" || this.tool === "DRAW_LINE" || this.tool === "DRAW_POLYGON" || this.tool === "DRAW_CIRCLE" || this.tool === "DRAW_LABEL") {
        this.$emit("set-tool", "");
      } else {
        this.showDrawMenu = !this.showDrawMenu;
      }
    },
    clearDraw() {
        const result = confirm('Weet je zeker dat je de tekening wil verwijderen?')
        if (result) {
            this.$emit('clear-draw')
            this.showDrawMenu = !this.showDrawMenu;
        }
    },
    toggleMeasure() {
      if (this.tool === "MEASURE_AREA" || this.tool === "MEASURE_LINE") {
        this.$emit("set-tool", "");
      } else {
        this.showMeasureMenu = !this.showMeasureMenu;
      }
    },
    toggleSelectArea() {
      if (this.tool !== "SELECT_AREA") {
        this.$emit("set-tool", "SELECT_AREA");
      } else {
        // toggle off when the user is currently selecting an area
        this.$emit("set-tool", "");
        this.$emit("set-selected-area", null);
      }
    },
    setTool(chosenTool) {
      this.$emit("set-tool", this.tool !== chosenTool ? chosenTool : "");
      this.showMeasureMenu = false;
      this.showDrawMenu = false;
    },
  },
  props: {
    tool: String,
    features: {
      type: Object,
      default: () => {
        return {
          draw: true,
          selectarea: true,
          measure: true,
        };
      },
    },
  },
};
</script>

<style scoped>
.wrapper {
  position: relative;
  margin-right: 12px;
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
