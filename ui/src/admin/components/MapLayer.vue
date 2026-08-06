<template>
  <AdminSidePanel :loading="loading">
    <template #header>
      <button
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton __normal __outline"
        type="button"
        aria-label="Ga terug"
        content="Terug"
        @click="back()"
      >
        <ArrowLeftIcon class="icon" />
      </button>
      <h1 class="layers-header">
        <LayerIcon class="icon" />
        Lagen
        <span class="layer-wrapper">
          <ChevronRightIcon class="no-margin icon __medium" />
          {{ layerDefaultSettings?.title }}
        </span>
      </h1>
    </template>
    <template #default>
      <div class="margin-content">
        <h3>Kaartlaag instellingen bewerken</h3>
        <div class="layer-setting-toggle">
          <ToggleSwitch
            input-id="customSettings"
            :model-value="mapLayerConfig.settings.customSettings"
            @update:model-value="toggleSettings"
          />
          <label for="customSettings">Kaart specifieke laag instellingen</label>
          <AdminFormInfoText :info-text="toggleSettingsInfo" />
        </div>
        <div v-if="mapLayerConfig.settings.customSettings" class="extra-padding-top">
          <div class="layer-settings">
            <div class="layer-setting-toggle">
              <ToggleSwitch
                input-id="is_base"
                :model-value="mapLayerConfig.settings.is_base"
                @update:model-value="toggleSliderField('is_base')"
              />
              <label for="is_base">Is een basislaag</label>
            </div>
            <div class="layer-setting-toggle">
              <ToggleSwitch
                input-id="is_visible"
                :model-value="mapLayerConfig.settings.is_visible"
                @update:model-value="toggleSliderField('is_visible')"
              />
              <label for="is_visible">Kaartlaag standaard zichtbaar</label>
            </div>
            <div v-if="otherVisibleBaseLayer" class="other-base-layer-visible">
              Merk op: er is al een basislaag met de instelling 'kaartlaag standaard zichtbaar' aanwezig
              <AdminFormInfoText
                :info-text="'Er is al een basislaag met de instelling \'kaartlaag standaard zichtbaar\' aanwezig, wanneer u \'kaartlaag standaard zichtbaar\' activeert wordt deze instelling op de andere basislaag gedeactiveerd.'"
              />
            </div>
            <div class="layer-setting-toggle">
              <ToggleSwitch
                input-id="is_filterable_in_legend"
                :model-value="mapLayerConfig.settings.is_filterable_in_legend"
                @update:model-value="toggleSliderField('is_filterable_in_legend')"
              />
              <label for="is_filterable_in_legend">Kaartlaag filterbaar in legenda</label>
            </div>

            <div class="layer-setting tw-flex tw-flex-col">
              <label for="opacity">Transparantie</label>
              <div class="tw-max-w-full tw-flex tw-items-center tw-gap-4">
                <InputNumber
                  :model-value="mapLayerConfig.settings.opacity"
                  input-id="opacity"
                  locale="en-US"
                  :min="0"
                  :max="1"
                  :max-fraction-digits="1"
                  :step="0.1"
                  show-buttons
                  @update:model-value="(value) => handleInput(value, 'opacity')"
                />
                <Slider
                  id="opacity"
                  :model-value="mapLayerConfig.settings.opacity"
                  name="opacity"
                  :min="0"
                  class="tw-w-full tw-mr-2"
                  :max="1"
                  :step="0.1"
                  fluid
                  @update:model-value="(value) => handleInput(value, 'opacity')"
                />
              </div>
            </div>
          </div>
          <div v-if="!isBaseLayer" class="layer-settings extra-padding-top">
            <div class="layer-setting">
              <label class="question-label" for="zoom_min">Zoomniveau minimum</label>
              <InputNumber
                :model-value="mapLayerConfig.settings.zoom_min"
                input-id="zoom_min"
                name="zoom_min"
                show-buttons
                :step="0.01"
                :min="0"
                :max-fraction-digits="2"
                :use-grouping="false"
                locale="en-US"
                fluid
                @update:model-value="(value) => handleInput(value, 'zoom_min')"
              />
            </div>
            <div class="layer-setting">
              <label class="question-label" for="zoom_max">Zoomniveau maximum</label>
              <InputNumber
                :model-value="mapLayerConfig.settings.zoom_max"
                input-id="zoom_max"
                name="zoom_max"
                show-buttons
                :step="0.01"
                :min="0"
                :max-fraction-digits="2"
                :use-grouping="false"
                locale="en-US"
                fluid
                @update:model-value="(value) => handleInput(value, 'zoom_max')"
              />
            </div>
            <div class="layer-setting">
              <label class="question-label" for="display_properties">Toon deze velden</label>
              <Textarea
                id="display_properties"
                :model-value="displayProperties"
                name="display_properties"
                rows="6"
                @update:model-value="
                  (value) => updateMultiLineField(mapLayerConfig.settings, 'display_properties', value)
                "
              />
            </div>
            <div class="layer-setting">
              <label class="question-label" for="search_properties">Doorzoek deze velden</label>
              <Textarea
                id="search_properties"
                :model-value="searchProperties"
                name="search_properties"
                rows="6"
                @update:model-value="
                  (value) => updateMultiLineField(mapLayerConfig.settings, 'search_properties', value)
                "
              />
            </div>
            <div v-if="checkLayerType(['WMS', 'WMTS'])" class="layer-setting">
              <label class="question-label" for="server_style">Stijlnaam voor WMS / WMTS laag</label>
              <InputText
                id="server_style"
                :model-value="mapLayerConfig.settings.server_style"
                name="server_style"
                @update:model-value="(value) => handleInput(value, 'server_style')"
              />
              <span class="info-text">Stijlnaam zoals beschikbaar op de server</span>
            </div>
            <div v-if="checkLayerType(['WFS', 'WMS_WFS', 'MVT'])" class="layer-setting">
              <label class="question-label" for="client_style">Stijl voor WFS / MVT laag</label>
              <CodeMirror
                id="client_style"
                :model-value="JSON.stringify(mapLayerConfig.settings.client_style, {}, 2)"
                name="client_style"
                basic
                :lang="json()"
                :linter="jsonParseLinter()"
                :extensions="[clouds]"
                gutter
                :wrap="true"
                class="!tw-text-sm"
                @update:model-value="(value) => updateJsonField('client_style', value)"
              />
            </div>
            <div class="layer-setting">
              <label class="question-label" for="friendly_fields">Vriendelijke veldnamen</label>
              <CodeMirror
                id="friendly_fields"
                :model-value="JSON.stringify(mapLayerConfig.settings.friendly_fields, {}, 2)"
                name="friendly_fields"
                basic
                :lang="json()"
                :linter="jsonParseLinter()"
                :extensions="[clouds]"
                gutter
                :wrap="true"
                class="!tw-text-sm"
                @update:model-value="(value) => updateJsonField('friendly_fields', value)"
              />
            </div>
            <div class="layer-setting">
              <label class="question-label" for="templated_properties">Templatevelden</label>
              <CodeMirror
                id="templated_properties"
                :model-value="JSON.stringify(mapLayerConfig.settings.templated_properties, {}, 2)"
                name="templated_properties"
                basic
                :lang="json()"
                :linter="jsonParseLinter()"
                :extensions="[clouds]"
                gutter
                :wrap="true"
                class="!tw-text-sm"
                @update:model-value="(value) => updateJsonField('templated_properties', value)"
              />
            </div>
            <div class="layer-setting">
              <div class="admin-label-button">
                <label for="linked_data">Gerelateerde data</label>
                <Button
                  v-tippy
                  size="small"
                  outlined
                  aria-label="Voeg gekoppelde data toe"
                  content="Voeg gekoppelde data toe"
                  class="!tw-text-sm !tw-font-semibold !tw-bg-white hover:!tw-bg-transparent !tw-px-8"
                  type="button"
                  @click="toggleModal('linkedData')"
                >
                  <AddIcon />
                  Toevoegen
                </Button>
              </div>

              <ul class="admin-list">
                <li v-for="linkedData in mapLayerConfig.settings.linked_data" :key="linkedData.id">
                  {{ linkedData.title }}
                  <div class="admin-list-buttons">
                    <button
                      v-tippy
                      :content="`Bewerk gekoppelde data ${linkedData.title}`"
                      :aria-label="`Bewerk gekoppelde data ${linkedData.title}`"
                      class="iconbutton __normal __round __alt_hover"
                      @click="toggleModal('linkedData', linkedData)"
                    >
                      <EditIcon class="icon __medium"></EditIcon>
                    </button>
                    <button
                      v-tippy
                      :content="`Verwijder gekoppelde data ${linkedData.title}`"
                      :aria-label="`Verwijder gekoppelde data ${linkedData.title}`"
                      class="iconbutton __normal __round __alt_hover"
                      @click="removeLinkedData(linkedData)"
                    >
                      <TrashIcon class="icon __medium"></TrashIcon>
                    </button>
                  </div>
                </li>
              </ul>
            </div>

            <div class="layer-setting">
              <div class="admin-label-button">
                <label for="linked_data">Templates</label>
                <Button
                  v-tippy
                  size="small"
                  outlined
                  aria-label="Voeg template toe"
                  content="Voeg template toe"
                  class="!tw-text-sm !tw-font-semibold !tw-bg-white hover:!tw-bg-transparent !tw-px-8"
                  type="button"
                  @click="toggleModal('templates')"
                >
                  <AddIcon />
                  Toevoegen
                </Button>
              </div>

              <ul class="admin-list">
                <li v-for="template in mapLayerConfig.settings.templates" :key="template.id">
                  {{ template.title }}
                  <div class="admin-list-buttons">
                    <button
                      v-tippy
                      :content="`Bewerk template ${template.title}`"
                      :aria-label="`Bewerk template ${template.title}`"
                      class="iconbutton __normal __round __alt_hover"
                      @click="toggleModal('templates', template)"
                    >
                      <EditIcon class="icon __medium"></EditIcon>
                    </button>
                    <button
                      v-tippy
                      :content="`Verwijder template ${template.title}`"
                      :aria-label="`Verwijder template ${template.title}`"
                      class="iconbutton __normal __round __alt_hover"
                      @click="removeTemplate(template)"
                    >
                      <TrashIcon class="icon __medium"></TrashIcon>
                    </button>
                  </div>
                </li>
              </ul>
            </div>
          </div>
          <Dialog
            v-model:visible="showFormModal"
            modal
            :header="formModalType === 'linkedData' ? 'Gerelateerde data' : 'Templates'"
            :style="{ width: '1200px', marginLeft: '2rem', marginRight: '2rem' }"
          >
            <LinkedDataForm
              v-if="formModalType === 'linkedData'"
              :initial-linked-data="selectedLinkedData"
              @close="closeFormModal"
              @save="saveLinkedData"
            />
            <TemplateForm
              v-else-if="formModalType === 'templates'"
              :initial-template="selectedTemplate"
              @close="closeFormModal"
              @save="saveTemplate"
            />
          </Dialog>
        </div>
      </div>
    </template>
  </AdminSidePanel>
</template>

<script>
import AddIcon from "@/assets/icons/add-icon.svg";
import ArrowLeftIcon from "@/assets/icons/arrow-left-icon.svg";
import ChevronRightIcon from "@/assets/icons/chevron-right-icon.svg";
import EditIcon from "@/assets/icons/edit-icon.svg";
import LayerIcon from "@/assets/icons/layer-icon.svg";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import AdminSidePanel from "@/admin/components/AdminSidePanel.vue";
import LinkedDataForm from "@/admin/components/LinkedDataForm.vue";
import TemplateForm from "@/admin/components/TemplateForm.vue";
import { updateMultiLineField } from "@/utils/admin-form-helpers";
import AdminFormInfoText from "@/admin/components/AdminFormInfoText.vue";
import { getAllObjects } from "@/utils/api-helpers";
import CodeMirror from "vue-codemirror6";
import { json, jsonParseLinter } from "@codemirror/lang-json";
import { clouds } from "thememirror";

export default {
  name: "MapLayer",
  components: {
    CodeMirror,
    AdminFormInfoText,
    TemplateForm,
    LinkedDataForm,
    AddIcon,
    ArrowLeftIcon,
    ChevronRightIcon,
    EditIcon,
    LayerIcon,
    TrashIcon,
    AdminSidePanel,
  },
  props: {
    initialData: Object,
    initialConfiguredLayers: Object,
  },
  emits: ["show-layers", "update-base-layer-status"],
  data() {
    return {
      mapLayerConfig: null,
      allLayers: [],
      selectedMapLayerConfigs: [],
      layerDefaultSettings: null,
      showFormModal: false,
      formModalType: null,
      selectedLinkedData: null,
      selectedTemplate: null,
      loading: false,
      toggleSettingsInfo: "Als deze schakelaar uit staat worden de kaartlaaginstellingen van de kaartlaag overgenomen.",
    };
  },
  computed: {
    clouds() {
      return clouds;
    },
    displayProperties() {
      return this.mapLayerConfig?.settings.display_properties.join("\n");
    },
    searchProperties() {
      return this.mapLayerConfig?.settings.search_properties.join("\n");
    },
    clientStyle() {
      return JSON.stringify(this.mapLayerConfig?.settings.client_style);
    },
    friendlyFields() {
      return JSON.stringify(this.mapLayerConfig?.settings.friendly_fields);
    },
    templatedProperties() {
      return JSON.stringify(this.mapLayerConfig?.settings.templated_properties);
    },
    isBaseLayer() {
      return this.mapLayerConfig?.settings.is_base;
    },
    otherMapLayerConfigs() {
      if (!this.selectedMapLayerConfigs) {
        return [];
      }
      return this.selectedMapLayerConfigs.filter((layer) => layer.layer !== this.mapLayerConfig.layer);
    },
    otherVisibleBaseLayer() {
      // Check if current layer is a base layer.
      if (
        !this.selectedMapLayerConfigs ||
        (!this.mapLayerConfig.settings.customSettings && !this.layerDefaultSettings.is_base) ||
        (this.mapLayerConfig.settings.customSettings && !this.mapLayerConfig.settings.is_base)
      ) {
        return false;
      }

      const otherLayer = this.otherMapLayerConfigs.find((layer) => {
        // Check if layer has custom settings and is a visible base layer.
        if (layer.settings.customSettings && layer.settings.is_base && layer.settings.is_visible) {
          return layer;
        }

        // Check if layer is visible base layer by default
        if (!layer.settings.customSettings) {
          const layerData = this.allLayers.find((l) => l.id === layer.layer);
          if (layerData.is_base && layerData.is_visible) {
            return layer;
          }
        }
      });

      return otherLayer;
    },
  },
  async created() {
    this.mapLayerConfig = this.initialData;
    this.layerDefaultSettings = await this.getLayer(this.mapLayerConfig.layer);
    this.selectedMapLayerConfigs = this.initialConfiguredLayers;
    await this.getLayers();
    if (this.mapLayerConfig.settings.customSettings) {
      /* If there are custom settings, amend the default settings
         with any set custom settings. */
      this.mapLayerConfig.settings = {
        ...this.layerDefaultSettings,
        ...this.mapLayerConfig.settings,
      };
    }
  },
  methods: {
    jsonParseLinter,
    json,
    updateMultiLineField,
    async getLayer(layerId) {
      const result = await fetch(`/atlas/api/v1/layers/${layerId}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layer");
        return;
      }

      return result.json();
    },
    async getLayers() {
      this.loading = true;
      const url = getAllObjects("/atlas/api/v1/layers/");
      const result = await fetch(url, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layers");
      }

      const response = await result.json();
      this.allLayers = response.results;
      this.loading = false;
    },
    async toggleSettings() {
      if (!this.mapLayerConfig.settings.customSettings) {
        // Get layer settings.
        this.mapLayerConfig.settings = {
          customSettings: true,
          ...this.layerDefaultSettings,
        };
      } else {
        // Reset layer settings.
        this.mapLayerConfig.settings = {
          customSettings: false,
          title: this.mapLayerConfig.settings.title,
        };
      }

      this.$emit("update-base-layer-status", this.mapLayerConfig);
    },
    toggleSliderField(field) {
      if (field === "is_visible" && !this.mapLayerConfig.settings[field] && this.otherVisibleBaseLayer) {
        this.resetOtherVisibleBaseLayer();
      }

      this.mapLayerConfig.settings[field] = !this.mapLayerConfig.settings[field];

      if (field === "is_base") {
        this.$emit("update-base-layer-status", this.mapLayerConfig);
      }
    },
    async resetOtherVisibleBaseLayer() {
      if (this.otherVisibleBaseLayer.settings.customSettings) {
        this.otherVisibleBaseLayer.settings.is_visible = false;
      } else {
        const layerData = await this.getLayer(this.otherVisibleBaseLayer.layer);

        this.otherVisibleBaseLayer.settings = {
          ...layerData,
          customSettings: true,
          is_visible: false,
        };
      }
    },
    updateJsonField(field, value) {
      // Set the corresponding field to an empty object when the user
      // clears out the field.
      if (!value || value.trim() === "") {
        this.mapLayerConfig.settings[field] = {};
        return;
      }

      try {
        this.mapLayerConfig.settings[field] = JSON.parse(value);
      } catch {
        // Ignore JSON parse errors.
      }
    },
    checkLayerType(types) {
      return types.includes(this.mapLayerConfig.settings.source_type);
    },
    toggleModal(modalType, editObject = null) {
      this.formModalType = modalType;

      if (modalType === "linkedData") {
        if (editObject) {
          this.selectedLinkedData = { ...editObject, edit: true };
        } else {
          this.selectedLinkedData = {
            title: "",
            url: "",
            name: "",
            source_key: "",
            target_key: "",
            display_properties: [],
            headers: [],
            edit: false,
          };
        }
      } else if (modalType === "templates") {
        if (editObject) {
          this.selectedTemplate = { ...editObject, edit: true };
        } else {
          this.selectedTemplate = {
            title: "",
            source: "",
            endpoint: "",
            method: "",
            list: "",
            headers: [],
            fields: [],
            template: "",
            source_key: "",
            target_key: "",
            edit: false,
          };
        }
      }

      this.showFormModal = true;
    },
    saveLinkedData(newValues) {
      if (!newValues.id && !newValues.randomId) {
        // If newValues has no id it needs to be added to the linked_data array.
        this.mapLayerConfig.settings.linked_data.push({
          ...newValues,
          randomId: crypto.getRandomValues(new Uint32Array(1))[0],
        });
      } else {
        // Otherwise update existing values.
        const index = this.mapLayerConfig.settings.linked_data.findIndex(
          (data) => (data.id && data.id === newValues.id) || (data.randomId && data.randomId === newValues.randomId),
        );

        if (index !== -1) {
          this.mapLayerConfig.settings.linked_data.splice(index, 1, newValues);
        }
      }
      this.closeFormModal();
    },
    saveTemplate(newValues) {
      if (!newValues.id && !newValues.randomId) {
        this.mapLayerConfig.settings.templates.push({
          ...newValues,
          randomId: crypto.getRandomValues(new Uint32Array(1))[0],
        });
      } else {
        const index = this.mapLayerConfig.settings.templates.findIndex(
          (data) => (data.id && data.id === newValues.id) || (data.randomId && data.randomId === newValues.randomId),
        );

        if (index !== -1) {
          this.mapLayerConfig.settings.templates.splice(index, 1, newValues);
        }
      }
      this.closeFormModal();
    },
    removeLinkedData(linkedData) {
      const acknowledged = confirm("Weet je zeker dat je het geselecteerde data object wilt verwijderen?");

      if (acknowledged) {
        const index = this.mapLayerConfig.settings.linked_data.indexOf(linkedData);
        this.mapLayerConfig.settings.linked_data.splice(index, 1);
      }
    },
    removeTemplate(template) {
      const acknowledged = confirm("Weet je zeker dat je het geselecteerde data object wilt verwijderen?");

      if (acknowledged) {
        const index = this.mapLayerConfig.settings.templates.indexOf(template);
        this.mapLayerConfig.settings.templates.splice(index, 1);
      }
    },
    closeFormModal() {
      this.showFormModal = false;
      this.formModalType = null;
      this.selectedLinkedData = null;
    },
    back() {
      this.$emit("show-layers");
    },
    handleInput(value, question) {
      // Opacity should always be stored as a number, if opacity is empty save opacity with default value 0
      if (question === "opacity" && (value === null || value === "")) {
        value = 0;
      }

      if (value === "") {
        value = null;
      }
      this.mapLayerConfig.settings[question] = value;
    },
  },
};
</script>

<style scoped>
.layer-setting label {
  font-weight: 700;
}

.layer-wrapper {
  display: flex;
  gap: 6px;
  align-items: center;
}

.layer-setting-toggle {
  display: flex;
  gap: 8px;
  align-items: center;
}

.layer-settings {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.layer-setting {
  display: flex;
  flex-direction: column;
}

.extra-padding-top {
  padding-top: 20px;
}

.info-text {
  font-size: var(--font-size-small);
}

.admin-label-button {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.admin-list > li {
  display: flex;
  align-items: center;
  background: var(--color-white);
  padding: 4px 12px;
}

.admin-list > li:hover {
  background-color: var(--color-primary-hover);
}

.admin-list > li:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-60);
}

.admin-list-buttons {
  display: flex;
  gap: 6px;
  margin-left: auto;
}

.other-base-layer-visible {
  display: flex;
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-bold);
  gap: 4px;
}
</style>
