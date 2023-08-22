<template>
  <form method="POST" @submit="submitForm">
    <h1>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        height="24px"
        viewBox="0 0 24 24"
        width="24px"
        fill="#000000"
      >
        <path d="M0 0h24v24H0V0z" fill="none" />
        <path
          d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM10 5.47l4 1.4v11.66l-4-1.4V5.47zm-5 .99l3-1.01v11.7l-3 1.16V6.46zm14 11.08l-3 1.01V6.86l3-1.16v11.84z"
        />
      </svg>
      Kaart
    </h1>

    <input
      v-model="data.title"
      type="text"
      name="title"
      class="title-input"
      placeholder="Titel van de kaart"
      required
    />

    <div class="settings">
      <button type="button" class="setting" @click="() => $emit('show-layers')">
        <svg
          class="setting-icon"
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
        <svg
          class="setting-chevron"
          width="6px"
          height="9px"
          viewBox="0 0 6 9"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
        >
          <title>icon/chevron-right</title>
          <g
            id="Symbols"
            stroke="none"
            stroke-width="1"
            fill="none"
            fill-rule="evenodd"
          >
            <g
              id="setting-icon"
              transform="translate(-284.000000, -16.000000)"
              fill="#000000"
              fill-rule="nonzero"
            >
              <g id="Path" transform="translate(284.000000, 16.000000)">
                <polygon
                  points="1.0575 0 0 1.0575 3.435 4.5 0 7.9425 1.0575 9 5.5575 4.5"
                ></polygon>
              </g>
            </g>
          </g>
        </svg>
      </button>
    </div>

    <div class="settings">
      <div class="setting">
        <input
          id="features.searchbar"
          v-model="data.features.searchbar"
          type="checkbox"
          name="features.searchbar"
        />
        <label for="features.searchbar">Toon zoekbalk</label>
      </div>

      <div class="setting">
        <input
          id="features.datapanel"
          v-model="data.features.datapanel"
          type="checkbox"
          name="features.datapanel"
        />
        <label for="features.datapanel">Toon dataweergave</label>
      </div>

      <div class="setting">
        <input
          id="features.selectarea"
          v-model="data.features.selectarea"
          type="checkbox"
          name="features.selectarea"
        />
        <label for="features.selectarea">Selecteer gebied</label>
      </div>

      <div class="setting">
        <input
          id="features.measure"
          v-model="data.features.measure"
          type="checkbox"
          name="features.measure"
        />
        <label for="features.measure">Opmeten</label>
      </div>

      <div class="setting">
        <input
          id="features.gps"
          v-model="data.features.gps"
          type="checkbox"
          name="features.gps"
        />
        <label for="features.gps">GPS knop</label>
      </div>

      <div class="setting">
        <input
          id="features.zoom"
          v-model="data.features.zoom"
          type="checkbox"
          name="features.zoom"
        />
        <label for="features.zoom">Zoomfunctie</label>
      </div>

      <div class="setting">
        <input
          id="features.scale"
          v-model="data.features.scale"
          type="checkbox"
          name="features.scale"
        />
        <label for="features.scale">Toon schaal</label>
      </div>

      <div class="setting">
        <input
          id="features.markerOnClick"
          v-model="data.features.markerOnClick"
          type="checkbox"
          name="features.markerOnClick"
        />
        <label for="features.markerOnClick">Prikker bij klik</label>
      </div>

      <div class="setting">
        <input
          id="features.layerlist"
          v-model="data.features.layerlist"
          type="checkbox"
          name="features.layerlist"
        />
        <label for="features.layerlist">Lagenlijst</label>
      </div>

      <div class="setting">
        <input
          id="features.legend"
          v-model="data.features.legend"
          type="checkbox"
          name="features.legend"
        />
        <label for="features.legend">Legenda</label>
      </div>

      <div class="setting">
        <input
          id="features.list"
          v-model="data.features.list"
          type="checkbox"
          name="features.list"
        />
        <label for="features.list">Lijstweergave</label>

        <button
          v-if="data.features.list"
          type="button"
          class="setting"
          @click="() => $emit('show-list')"
        >
          <svg
            class="setting-chevron"
            width="6px"
            height="9px"
            viewBox="0 0 6 9"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
          >
            <title>icon/chevron-right</title>
            <g
              id="Symbols"
              stroke="none"
              stroke-width="1"
              fill="none"
              fill-rule="evenodd"
            >
              <g
                id="setting-icon"
                transform="translate(-284.000000, -16.000000)"
                fill="#000000"
                fill-rule="nonzero"
              >
                <g id="Path" transform="translate(284.000000, 16.000000)">
                  <polygon
                    points="1.0575 0 0 1.0575 3.435 4.5 0 7.9425 1.0575 9 5.5575 4.5"
                  ></polygon>
                </g>
              </g>
            </g>
          </svg>
        </button>
      </div>

      <div class="setting">
        <input
          id="features.detail"
          v-model="data.features.detail"
          type="checkbox"
          name="features.detail"
        />
        <label for="features.detail">Detailweergave</label>
      </div>

      <div class="setting">
        <input
          id="features.filters"
          v-model="data.features.filters"
          type="checkbox"
          name="features.filters"
        />
        <label for="features.filters">Filters</label>

        <button
          v-if="data.features.filters"
          type="button"
          class="setting"
          @click="() => $emit('show-filters')"
        >
          <svg
            class="setting-chevron"
            width="6px"
            height="9px"
            viewBox="0 0 6 9"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
          >
            <title>icon/chevron-right</title>
            <g
              id="Symbols"
              stroke="none"
              stroke-width="1"
              fill="none"
              fill-rule="evenodd"
            >
              <g
                id="setting-icon"
                transform="translate(-284.000000, -16.000000)"
                fill="#000000"
                fill-rule="nonzero"
              >
                <g id="Path" transform="translate(284.000000, 16.000000)">
                  <polygon
                    points="1.0575 0 0 1.0575 3.435 4.5 0 7.9425 1.0575 9 5.5575 4.5"
                  ></polygon>
                </g>
              </g>
            </g>
          </svg>
        </button>
      </div>
    </div>

    <div class="flexer">
      <router-link to="/maps" class="button __tertiary">Annuleer</router-link>
      <button type="submit" class="button __primary">Opslaan</button>
    </div>
  </form>
</template>

<script>
export default {
  name: "MapForm",
  props: {
    initialData: Object,
  },
  data() {
    return {
      data: this.initialData || { features: {} },
    };
  },
  methods: {
    submitForm(e) {
      e.preventDefault();
      this.$emit("submit", this.data);
    },
  },
};
</script>

<style scoped>
.map-form {
  width: 100%;
}

.title-input {
  margin-top: 16px;
}

.settings {
  margin-top: 32px;
}

.flexer {
  position: absolute;
  bottom: var(--padding-screen);
  left: 0;
  right: 0;
}

.setting-icon {
  margin-right: 10px;
}

.setting-chevron {
  width: 32px;
  margin-left: auto;
}

.setting input[type="checkbox"] {
  width: 24px;
  margin-right: 10px;
  cursor: pointer;
}

.setting input[type="checkbox"] + label {
  flex-grow: 1;
  align-self: stretch;
  display: flex;
  align-items: center;
  cursor: pointer;
}
</style>
