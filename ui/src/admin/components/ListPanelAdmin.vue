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
        Lijstweergave
      </h1>
      <div class="header-spacer" />
    </div>

    <div class="select-wrapper">
      <select
        v-model="selectedLayerTitle"
        class="layer-select edit-field-border"
        @change="onListLayerChange"
      >
        <option disabled value="">Selecteer een laag</option>
        <option v-for="l in availableLayers" :key="l.id" :value="l.id">
          {{ l.title }}
        </option>
      </select>
    </div>

    <p v-if="!selectedLayerTitle">
      Kies eerst een laag voordat je de lijstweergave instelt.
    </p>

    <div v-if="selectedLayerTitle" class="list-config-wrapper">
      <div>
        <label>Template naam:</label>
        <input
          v-model="data.settings.title"
          type="text"
          name="title"
          class="title-input edit-field-border"
          placeholder="Template titel"
        />
      </div>

      <div>
        <label>Korte beschrijving:</label>
        <textarea
          v-model="data.settings.short_description"
          type="text"
          name="title"
          class="short-description-input edit-field-border"
          placeholder="Template korte beschrijving"
        />
      </div>
    </div>

    <p class="help-text">
      Voor het instellen van variabele naam (e.g. kolom naam van een laag) dient
      dat als volgt te gebeuren:
      <br />
      <br />
      <i>{{ columnExample }}</i>
      <br />
      <br />
      Waarbij "kolom_naam" de naam van de gewenste kolom is.
    </p>
  </div>
</template>

<!-- Todo: check if shared code can be moved to base/abstract class together with ListPanelAdmin. -->
<script>
export default {
  name: "ListPanelAdmin",
  props: {
    initialData: Object,
    layers: [],
  },
  data() {
    return {
      data: this.initialData,
      selectedLayerTitle: "",
      selectedLayer: {},
      columnExample: "{{ kolom_naam }}",
    };
  },
  computed: {
    availableLayers() {
      return this.layers.filter((layer) => {
        return layer.source_type === "WMS_WFS";
      });
    },
  },
  mounted() {
    if (this.data.settings.listLayerId) {
      this.selectedLayer = this.getLayerById(this.data.settings.listLayerId);
      this.selectedLayerTitle = this.selectedLayer.id;
    }
  },
  methods: {
    onListLayerChange(e) {
      // todo: kijken of dit wel wenselijk is.
      this.data.settings.title = "";
      this.data.settings.short_description = "";

      const layerId = e.target.value;
      this.selectedLayer = this.getLayerById(layerId);
      this.data.settings.listLayerId = layerId;
      this.data.settings.listLayerDisplayName = this.selectedLayerTitle;
    },
    getLayerById(id) {
      return this.layers.find((layer) => {
        return layer.id === id;
      });
    },
  },
};
</script>

<style scoped>
.content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
}

.header-spacer {
  width: 40px;
}

.settings + .settings {
  margin-top: 40px;
}

.setting .iconbutton {
  margin-left: auto;
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

.short-description-input {
  width: 100%;
  min-height: 100px;
}

.layer-select {
  width: 100%;
  height: 40px;
  font-size: 16px;
}

.layer-select:hover {
  background: var(--color-grey-40);
}

.list-config-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.help-text {
  font-size: 14px;
}
</style>
