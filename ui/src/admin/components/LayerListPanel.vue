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
        <ArrowLeftIcon class="icon" />
      </button>
      <h1>
        <LayerIcon class="icon" />
        Lagenlijst
      </h1>
    </template>
    <template #default>
      <div class="settings">
        <div class="setting __hover">
          <Checkbox
            input-id="features.layerlistsearch"
            :model-value="data.features.layerlistsearch"
            name="features.layerlistsearch"
            binary
            @update:modelValue="(value) => (data.features.layerlistsearch = value)"
          />
          <label for="features.layerlistsearch">Verberg zoekbalk lagenlijst</label>
        </div>

        <div class="setting __hover">
          <Checkbox
            input-id="features.layerlistsimple"
            :model-value="data.features.layerlistsimple"
            name="features.layerlistsimple"
            binary
            @update:modelValue="(value) => (data.features.layerlistsimple = value)"
          />
          <label for="features.layerlistsimple">Versimpelde weergave lagenlijst</label>
        </div>
      </div>
    </template>
  </AdminSidePanel>
</template>

<script>
import ArrowLeftIcon from "../../assets/icons/arrow-left-icon.svg";
import LayerIcon from "../../assets/icons/layer-icon.svg";
import AdminSidePanel from "@/admin/components/AdminSidePanel.vue";

export default {
  name: "LayerListPanel",
  components: { AdminSidePanel, ArrowLeftIcon, LayerIcon },
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
