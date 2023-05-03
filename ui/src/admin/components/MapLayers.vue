<template>
  <div class="content">
    <div class="header">
      <button
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton __normal __outline"
        type="button"
        aria-label="Ga terug"
        content="Terug"
        @click="() => $emit('show-form')"
      >
        <svg
          width="24px"
          height="24px"
          viewBox="0 0 24 24"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
        >
          <title>arrow_back_black_24dp</title>
          <g
            id="Admin"
            stroke="none"
            stroke-width="1"
            fill="none"
            fill-rule="evenodd"
          >
            <g
              id="Kaart---Zoekbalk"
              transform="translate(-24.000000, -24.000000)"
            >
              <g
                id="arrow_back_black_24dp"
                transform="translate(16.000000, 16.000000)"
              >
                <g transform="translate(8.000000, 8.000000)">
                  <polygon id="Path" points="0 0 24 0 24 24 0 24"></polygon>
                  <polygon
                    id="Path"
                    fill="#000000"
                    fill-rule="nonzero"
                    points="20 11 7.83 11 13.42 5.41 12 4 4 12 12 20 13.41 18.59 7.83 13 20 13"
                  ></polygon>
                </g>
              </g>
            </g>
          </g>
        </svg>
      </button>
      <h1>
        <svg
          width="24px"
          height="24px"
          viewBox="0 0 24 24"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
        >
          <title>Artboard</title>
          <g
            id="Artboard"
            stroke="none"
            stroke-width="1"
            fill="none"
            fill-rule="evenodd"
          >
            <g
              id="lagen"
              transform="translate(3.000000, 2.000000)"
              fill="#000000"
              fill-rule="nonzero"
            >
              <path
                id="Shape"
                d="M8.99,17.7805 L1.62,11.62075 L0,12.97525 L9,20.50025 L18,12.97525 L16.37,11.61 L8.99,17.7805 Z M9,15.05 L16.36,8.89025 L18,7.525 L9,0 L0,7.525 L1.63,8.89025 L9,15.05 Z M9,2.71975 L14.74,7.525 L9,12.33025 L3.26,7.525 L9,2.71975 Z"
              ></path>
            </g>
          </g>
        </svg>
        Lagen
      </h1>
      <div class="header-spacer" />
    </div>

    <ul v-if="selectedLayers.length > 0" class="settings">
      <li
        v-for="selectedLayer in selectedLayers"
        :key="selectedLayer.id"
        class="setting"
      >
        {{ selectedLayer.title }}
        <button
          v-tippy="{ placement: 'bottom' }"
          class="iconbutton __normal"
          type="button"
          aria-label="Verwijder laag"
          content="Verwijder"
          @click="deselectLayer(selectedLayer)"
        >
          <svg
            width="24px"
            height="24px"
            viewBox="0 0 24 24"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
          >
            <title>icon/layer-remove</title>
            <g
              id="icon/layer-remove"
              stroke="none"
              stroke-width="1"
              fill="none"
              fill-rule="evenodd"
            >
              <g id="highlight_off_black_24dp">
                <polygon id="Path" points="0 0 24 0 24 24 0 24"></polygon>
                <path
                  id="Shape"
                  d="M4,6 L2,6 L2,20 C2,21.1 2.9,22 4,22 L18,22 L18,20 L4,20 L4,6 Z M20,2 L8,2 C6.9,2 6,2.9 6,4 L6,16 C6,17.1 6.9,18 8,18 L20,18 C21.1,18 22,17.1 22,16 L22,4 C22,2.9 21.1,2 20,2 Z M20,16 L8,16 L8,4 L20,4 L20,16 Z M18,11 L18,9 L10,9 L10,11 L18,11 Z"
                  fill="#000000"
                  fill-rule="nonzero"
                ></path>
              </g>
            </g>
          </svg>
        </button>
      </li>
    </ul>

    <div class="settings">
      <div class="search-wrapper">
        <svg
          width="18px"
          height="18px"
          viewBox="0 0 18 18"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
        >
          <g
            id="Admin"
            stroke="none"
            stroke-width="1"
            fill="none"
            fill-rule="evenodd"
          >
            <g
              id="Kaart---Lagen"
              transform="translate(-45.000000, -183.000000)"
              fill="#000000"
              fill-rule="nonzero"
            >
              <g
                id="search_black_24dp"
                transform="translate(42.000000, 180.000000)"
              >
                <path
                  id="Shape"
                  d="M15.5,14 L14.71,14 L14.43,13.73 C15.41,12.59 16,11.11 16,9.5 C16,5.91 13.09,3 9.5,3 C5.91,3 3,5.91 3,9.5 C3,13.09 5.91,16 9.5,16 C11.11,16 12.59,15.41 13.73,14.43 L14,14.71 L14,15.5 L19,20.49 L20.49,19 L15.5,14 Z M9.5,14 C7.01,14 5,11.99 5,9.5 C5,7.01 7.01,5 9.5,5 C11.99,5 14,7.01 14,9.5 C14,11.99 11.99,14 9.5,14 Z"
                ></path>
              </g>
            </g>
          </g>
        </svg>
        <input
          id="layers-search"
          v-model="searchQuery"
          type="search"
          name="query"
          placeholder="Zoek laag"
        />
      </div>

      <ul>
        <li
          v-for="layer in visibleUnselectedLayers"
          :key="layer.id"
          class="setting"
        >
          {{ layer.title }}
          <button
            v-tippy="{ placement: 'bottom' }"
            class="iconbutton __normal"
            type="button"
            aria-label="Voeg laag toe"
            content="Voeg toe"
            @click="selectLayer(layer)"
          >
            <svg
              width="24px"
              height="24px"
              viewBox="0 0 24 24"
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              xmlns:xlink="http://www.w3.org/1999/xlink"
            >
              <title>Group 4</title>
              <g
                id="Symbols"
                stroke="none"
                stroke-width="1"
                fill="none"
                fill-rule="evenodd"
              >
                <g id="layer" transform="translate(-314.000000, -4.000000)">
                  <g id="Group" transform="translate(314.000000, 4.000000)">
                    <polygon id="Path" points="0 0 24 0 24 24 0 24"></polygon>
                    <path
                      id="Shape"
                      d="M4,6 L2,6 L2,20 C2,21.1 2.9,22 4,22 L18,22 L18,20 L4,20 L4,6 Z M20,2 L8,2 C6.9,2 6,2.9 6,4 L6,16 C6,17.1 6.9,18 8,18 L20,18 C21.1,18 22,17.1 22,16 L22,4 C22,2.9 21.1,2 20,2 Z M20,16 L8,16 L8,4 L20,4 L20,16 Z M13,14 L15,14 L15,11 L18,11 L18,9 L15,9 L15,6 L13,6 L13,9 L10,9 L10,11 L13,11 L13,14 Z"
                      fill="#000000"
                      fill-rule="nonzero"
                    ></path>
                  </g>
                </g>
              </g>
            </svg>
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "MapLayers",
  props: {
    initialData: Object,
  },
  data() {
    return {
      allLayers: [],
      selectedLayers: [],
      searchQuery: "",
    };
  },
  computed: {
    unselectedLayers() {
      return this.allLayers.filter(
        (layer) =>
          this.selectedLayers.filter(
            (selectedLayer) => selectedLayer.id === layer.id
          ).length === 0
      );
    },
    visibleUnselectedLayers() {
      if (!this.searchQuery) {
        return this.unselectedLayers;
      }

      return this.unselectedLayers.filter(
        (layer) =>
          layer.title.toLowerCase().search(this.searchQuery.toLowerCase()) !==
          -1
      );
    },
    selectedLayerIds() {
      return this.selectedLayers.map((layer) => layer.id);
    },
  },
  async created() {
    await this.getLayers();

    if (this.initialData.layers) {
      this.selectedLayers = this.allLayers.filter((layer) =>
        this.initialData.layers.includes(layer.id)
      );
    }
  },
  methods: {
    async getLayers() {
      const result = await fetch("/atlas/api/v1/layers/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layers");
      }

      this.allLayers = await result.json();
    },
    selectLayer(layer) {
      this.selectedLayers.push(layer);

      this.$emit("change", this.selectedLayerIds);
    },
    deselectLayer(layerToDeselect) {
      this.selectedLayers = this.selectedLayers.filter(
        (selectedLayer) => selectedLayer.id !== layerToDeselect.id
      );

      this.$emit("change", this.selectedLayerIds);
    },
  },
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
}

.header-spacer {
  width: 40px;
}

.settings {
  margin-top: 24px;
}

.settings + .settings {
  margin-top: 40px;
}

.setting .iconbutton {
  margin-left: auto;
}

.search-wrapper {
  position: relative;
  border-top: 1px solid var(--color-grey-80);
  border-bottom: 1px solid var(--color-grey-80);
  margin-bottom: -1px;
}

.search-wrapper svg {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 16px;
  margin: auto 0;
  pointer-events: none;
}

.search-wrapper input {
  width: 100%;
  height: 48px;
  padding: 0 0 0 48px;
}
</style>
