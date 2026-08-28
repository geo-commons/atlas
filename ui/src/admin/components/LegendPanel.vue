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
        Legenda
      </h1>
    </template>
    <template #default>
      <div class="settings">
        <div class="setting __hover">
          <Checkbox
            input-id="features.show_toggle_all_layers_in_legend"
            :model-value="data.features.show_toggle_all_layers_in_legend !== false"
            name="features.show_toggle_all_layers_in_legend"
            binary
            @update:model-value="(value) => (data.features.show_toggle_all_layers_in_legend = value)"
          />
          <label for="features.show_toggle_all_layers_in_legend">Toon lagen in- en uitklappen</label>
        </div>

        <div class="setting __hover">
          <Checkbox
            input-id="features.show_sort_layers_in_legend"
            :model-value="data.features.show_sort_layers_in_legend !== false"
            name="features.show_sort_layers_in_legend"
            binary
            @update:model-value="(value) => (data.features.show_sort_layers_in_legend = value)"
          />
          <label for="features.show_sort_layers_in_legend">Toon kaartvolgorde aanpassen</label>
        </div>

        <div class="setting __hover">
          <Checkbox
            input-id="features.show_transparency_in_legend"
            :model-value="data.features.show_transparency_in_legend !== false"
            name="features.show_transparency_in_legend"
            binary
            @update:model-value="(value) => (data.features.show_transparency_in_legend = value)"
          />
          <label for="features.show_transparency_in_legend">Toon transparantie</label>
        </div>

        <div class="setting __hover">
          <Checkbox
            input-id="features.show_not_selectable_in_legend"
            :model-value="data.features.show_not_selectable_in_legend !== false"
            name="features.show_not_selectable_in_legend"
            binary
            @update:model-value="(value) => (data.features.show_not_selectable_in_legend = value)"
          />
          <label for="features.show_not_selectable_in_legend">Toon niet-selecteerbaar</label>
        </div>

        <div class="setting __hover">
          <Checkbox
            input-id="features.show_information_in_legend"
            :model-value="data.features.show_information_in_legend !== false"
            name="features.show_information_in_legend"
            binary
            @update:model-value="(value) => (data.features.show_information_in_legend = value)"
          />
          <label for="features.show_information_in_legend">Toon informatie</label>
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
  name: "LegendPanel",
  components: { AdminSidePanel, ArrowLeftIcon, LayerIcon },
  props: {
    initialData: Object,
  },
  emits: ["show-form"],
  data() {
    return {
      data: this.initialData || { features: {} },
    };
  },
};
</script>

<style scoped>
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
