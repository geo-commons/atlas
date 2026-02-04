<template>
  <AdminSidePanel>
    <template #header>
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
          <g id="Admin" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
            <g id="Kaart---Zoekbalk" transform="translate(-24.000000, -24.000000)">
              <g id="arrow_back_black_24dp" transform="translate(16.000000, 16.000000)">
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
          <g id="Artboard" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
            <g id="lagen" transform="translate(3.000000, 2.000000)" fill="#000000" fill-rule="nonzero">
              <path
                id="Shape"
                d="M8.99,17.7805 L1.62,11.62075 L0,12.97525 L9,20.50025 L18,12.97525 L16.37,11.61 L8.99,17.7805 Z M9,15.05 L16.36,8.89025 L18,7.525 L9,0 L0,7.525 L1.63,8.89025 L9,15.05 Z M9,2.71975 L14.74,7.525 L9,12.33025 L3.26,7.525 L9,2.71975 Z"
              ></path>
            </g>
          </g>
        </svg>
        Lijstweergave
      </h1>
    </template>
    <template #default>
      <div class="margin-content">
        <div class="select-wrapper">
          <Select
            :model-value="selectedLayerTitle"
            :options="availableLayers"
            option-label="title"
            option-value="id"
            placeholder="Selecteer een laag"
            show-clear
            filter
            fluid
            class="tw-mb-2"
            filter-placeholder="Zoek een laag"
            @update:model-value="(value) => onListLayerChange(value)"
          />
        </div>

        <p v-if="!selectedLayerTitle">Kies eerst een laag voordat je de lijstweergave instelt.</p>

        <div v-if="selectedLayerTitle" class="list-config-wrapper">
          <div>
            <label class="tw-font-bold">Template naam:</label>
            <InputText
              :model-value="data.settings.title"
              placeholder="Template titel"
              name="title"
              fluid
              @update:model-value="(value) => (data.settings.title = value)"
            />
          </div>

          <div>
            <label class="tw-font-bold">Korte beschrijving:</label>
            <Textarea
              :model-value="data.settings.short_description"
              placeholder="Template korte beschrijving"
              name="short_description"
              fluid
              rows="5"
              @update:model-value="(value) => (data.settings.short_description = value)"
            />
          </div>
        </div>

        <p class="help-text">
          Voor het instellen van variabele naam (e.g. kolom naam van een laag) dient dat als volgt te gebeuren:
          <br />
          <br />
          <i>{{ columnExample }}</i>
          <br />
          <br />
          Waarbij "kolom_naam" de naam van de gewenste kolom is.
        </p>
      </div>
    </template>
  </AdminSidePanel>
</template>

<!-- Todo: check if shared code can be moved to base/abstract class together with ListPanelAdmin. -->
<script>
import AdminSidePanel from "@/admin/components/AdminSidePanel.vue";

export default {
  name: "ListPanelAdmin",
  components: { AdminSidePanel },
  props: {
    initialData: Object,
    layers: Array,
  },
  emits: ["show-form"],
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
      this.selectedLayerTitle = this.selectedLayer ? this.selectedLayer.id : "";
    }
  },
  methods: {
    onListLayerChange(e) {
      // todo: kijken of dit wel wenselijk is.
      this.data.settings.title = "";
      this.data.settings.short_description = "";

      const layerId = e;
      this.selectedLayerTitle = layerId;
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
.margin-content {
  padding-top: 20px;
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
