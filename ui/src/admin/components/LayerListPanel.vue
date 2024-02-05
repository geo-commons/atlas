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
        <ArrowLeftIcon class="icon" />
      </button>
      <h1>
        <LayerIcon class="icon" />
        Lagenlijst
      </h1>
      <div class="header-spacer" />
    </div>

    <div class="settings">
      <div class="setting __hover">
        <input
          id="features.layerlistsearch"
          v-model="data.features.layerlistsearch"
          type="checkbox"
          name="features.layerlistsearch"
        />
        <label for="features.layerlistsearch">Verberg zoekbalk lagenlijst</label>
      </div>

      <div class="setting __hover">
        <input
          id="features.layerlistsimple"
          v-model="data.features.layerlistsimple"
          type="checkbox"
          name="features.layerlistsimple"
        />
        <label for="features.layerlistsimple">Versimpelde weergave lagenlijst</label>
      </div>
    </div>
  </div>
</template>

<script>
import ArrowLeftIcon from "../../assets/icons/arrow-left-icon.svg";
import LayerIcon from "../../assets/icons/layer-icon.svg";

export default {
  name: "LayerListPanel",
  components: { ArrowLeftIcon, LayerIcon },
  props: {
    initialData: Object,
  },
  data() {
    return {
      data: this.initialData || { features: {} },
    };
  },
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  padding-bottom: 16px;
}

.header-spacer {
  width: 40px;
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
