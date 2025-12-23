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
          <switch-slider
            aria-label="Kaartlaag specifieke instellingen"
            :initial-checked-status="mapLayerConfig.settings.customSettings"
            @toggleSwitch="toggleSettings"
          />
          <div>Kaart specifieke laag instellingen</div>
          <AdminFormInfoText :info-text="toggleSettingsInfo" />
        </div>
        <div v-if="mapLayerConfig.settings.customSettings" class="extra-padding-top">
          <div class="layer-settings">
            <div class="layer-setting-toggle">
              <switch-slider
                aria-label="Basislaag"
                :initial-checked-status="mapLayerConfig.settings.is_base"
                @toggleSwitch="toggleSliderField('is_base')"
              />
              <div>Is een basislaag</div>
            </div>
            <div class="layer-setting-toggle">
              <switch-slider
                aria-label="Standaard zichtbaar"
                :initial-checked-status="mapLayerConfig.settings.is_visible"
                @toggleSwitch="toggleSliderField('is_visible')"
              />
              <div>Kaartlaag standaard zichtbaar</div>
            </div>
            <div v-if="otherVisibleBaseLayer" class="other-base-layer-visible">
              Merk op: er is al een basislaag met de instelling 'kaartlaag standaard zichtbaar' aanwezig
              <AdminFormInfoText
                :info-text="'Er is al een basislaag met de instelling \'kaartlaag standaard zichtbaar\' aanwezig, wanneer u \'kaartlaag standaard zichtbaar\' activeert wordt deze instelling op de andere basislaag gedeactiveerd.'"
              />
            </div>

            <div class="opacity-wrapper">
              <label for="opacity">Transparantie</label>
              <vee-field
                id="opacity"
                name="opacity"
                class="opacity-slider"
                type="range"
                :value="mapLayerConfig.settings.opacity * 100"
              >
                <input
                  id="opacity"
                  class="opacity-slider"
                  type="range"
                  name="opacity"
                  min="0"
                  max="100"
                  step="10"
                  aria-label="Transparantie instellen"
                  :value="mapLayerConfig.settings.opacity * 100"
                  @change="(e) => changeLayerOpacity(e.target.value / 100)"
                />
              </vee-field>
              <span class="tw-text-sm tw-font-semibold">{{ mapLayerConfig.settings.opacity * 100 }}</span>
            </div>
          </div>
          <div v-if="!isBaseLayer" class="layer-settings extra-padding-top">
            <div class="layer-setting">
              <label class="question-label" for="zoom_min">Zoomniveau minimum</label>
              <input
                id="zoom_min"
                :value="mapLayerConfig.settings.zoom_min"
                name="zoom_min"
                type="number"
                @change="(e) => handleInput(e, 'zoom_min')"
              />
            </div>
            <div class="layer-setting">
              <label class="question-label" for="zoom_man">Zoomniveau maximum</label>
              <input
                id="zoom_max"
                :value="mapLayerConfig.settings.zoom_max"
                name="zoom_max"
                type="number"
                @change="(e) => handleInput(e, 'zoom_max')"
              />
            </div>
            <div class="layer-setting">
              <label class="question-label" for="display_properties">Toon deze velden</label>
              <textarea
                id="display_properties"
                name="display_properties"
                rows="6"
                :value="displayProperties"
                @change="(e) => updateMultiLineField(mapLayerConfig.settings, 'display_properties', e.target.value)"
              />
            </div>
            <div class="layer-setting">
              <label class="question-label" for="search_properties">Doorzoek deze velden</label>
              <textarea
                id="search_properties"
                name="search_properties"
                rows="6"
                :value="searchProperties"
                @change="(e) => updateMultiLineField(mapLayerConfig.settings, 'search_properties', e.target.value)"
              />
            </div>
            <div v-if="checkLayerType(['WMS', 'WMTS'])" class="layer-setting">
              <label class="question-label" for="server_style">Stijlnaam voor WMS / WMTS laag</label>
              <input
                id="server_style"
                v-model.trim="mapLayerConfig.settings.server_style"
                name="server_style"
                type="text"
              />
              <span class="info-text">Stijlnaam zoals beschikbaar op de server</span>
            </div>
            <div v-if="checkLayerType(['WFS', 'WMS_WFS', 'MVT'])" class="layer-setting">
              <label class="question-label" for="client_style">Stijl voor WFS / MVT laag</label>
              <textarea
                id="client_style"
                :value="clientStyle"
                name="client_style"
                rows="6"
                @change="(e) => updateJsonField('client_style', e.target.value)"
              />
            </div>
            <div class="layer-setting">
              <label class="question-label" for="friendly_fields">Vriendelijke veldnamen</label>
              <textarea
                id="friendly_fields"
                :value="friendlyFields"
                name="friendly_fields"
                rows="6"
                @change="(e) => updateJsonField('friendly_fields', e.target.value)"
              />
            </div>
            <div class="layer-setting">
              <label class="question-label" for="templated_properties">Templatevelden</label>
              <textarea
                id="templated_properties"
                :value="templatedProperties"
                name="templated_properties"
                rows="6"
                @change="(e) => updateJsonField('templated_properties', e.target.value)"
              />
            </div>
            <div class="layer-setting">
              <div class="admin-label-button">
                <label for="linked_data">Gerelateerde data</label>
                <button
                  v-tippy
                  content="Voeg gekoppelde data toe"
                  aria-label="Voeg gekoppelde data toe"
                  class="button __small __secondary_admin"
                  @click="toggleModal('linkedData')"
                >
                  <AddIcon />
                  Voeg toe
                </button>
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
                <button
                  v-tippy
                  content="Voeg template toe"
                  aria-label="Voeg template toe"
                  class="button __small __secondary_admin"
                  @click="toggleModal('templates')"
                >
                  <AddIcon />
                  Voeg toe
                </button>
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
          <FormModal v-if="showFormModal" :toggle-modal="showFormModal" @close="closeFormModal">
            <template #header>
              <h3 v-if="formModalType === 'linkedData'">Gerelateerde data</h3>
              <h3 v-else-if="formModalType === 'templates'">Templates</h3>
            </template>
            <template #body>
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
            </template>
          </FormModal>
        </div>
      </div>
    </template>
  </AdminSidePanel>
</template>

<script>
import FormModal from "@/components/FormModal.vue";
import AddIcon from "@/assets/icons/add-icon.svg";
import ArrowLeftIcon from "@/assets/icons/arrow-left-icon.svg";
import ChevronRightIcon from "@/assets/icons/chevron-right-icon.svg";
import EditIcon from "@/assets/icons/edit-icon.svg";
import LayerIcon from "@/assets/icons/layer-icon.svg";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import AdminSidePanel from "@/admin/components/AdminSidePanel.vue";
import LinkedDataForm from "@/admin/components/LinkedDataForm.vue";
import TemplateForm from "@/admin/components/TemplateForm.vue";
import { Field as VeeField } from "vee-validate";
import { updateMultiLineField } from "@/utils/admin-form-helpers";
import SwitchSlider from "@/components/SwitchSlider.vue";
import AdminFormInfoText from "@/admin/components/AdminFormInfoText.vue";
import { getAllObjects } from "@/utils/api-helpers";

export default {
  name: "MapLayer",
  components: {
    AdminFormInfoText,
    SwitchSlider,
    TemplateForm,
    LinkedDataForm,
    AddIcon,
    FormModal,
    ArrowLeftIcon,
    ChevronRightIcon,
    EditIcon,
    LayerIcon,
    TrashIcon,
    AdminSidePanel,
    VeeField,
  },
  props: {
    initialData: Object,
    initialConfiguredLayers: Object,
  },
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
      toggleSettingsInfo:
        "Als deze schakelaar uit staat worden de kaartlaag instellingen van de hoofdkaart overgenomen.",
    };
  },
  computed: {
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
    this.selectedMapLayerConfigs = this.initialConfiguredLayers;

    await this.getLayers();

    this.layerDefaultSettings = this.allLayers.find((layer) => this.mapLayerConfig.layer === layer.id);
  },
  methods: {
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
        const layerData = await this.getLayer(this.mapLayerConfig.layer);
        this.mapLayerConfig.settings = {
          customSettings: true,
          ...layerData,
        };
      } else {
        // Reset layer settings.
        this.mapLayerConfig.settings = {
          customSettings: false,
          title: this.mapLayerConfig.settings.title,
        };
      }
    },
    toggleSliderField(field) {
      if (field === "is_visible" && !this.mapLayerConfig.settings[field] && this.otherVisibleBaseLayer) {
        this.resetOtherVisibleBaseLayer();
      }

      this.mapLayerConfig.settings[field] = !this.mapLayerConfig.settings[field];
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
    changeLayerOpacity(newValue) {
      this.mapLayerConfig.settings.opacity = newValue;
    },
    updateJsonField(field, newValue) {
      // Set the corresponding field to an empty object when the user
      // clears out the field.
      if (!newValue || newValue.trim() === "") {
        this.mapLayerConfig.settings[field] = {};
        return;
      }

      try {
        this.mapLayerConfig.settings[field] = JSON.parse(newValue);
      } catch {
        // todo: maak nettere foutmelding
        console.error("geen geldige json");
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
    handleInput(event, question) {
      let value = event.target.value;
      if (value === "") {
        value = null;
      }
      this.mapLayerConfig.settings[question] = value;
    },
  },
};
</script>

<style scoped>
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

.opacity-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.opacity-input {
  width: 22px;
  flex-shrink: 0;
  padding: 0;
  font-size: 12px;
  font-weight: var(--font-weight-bold);
  border: none;
  background: transparent;
}

.opacity-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.opacity-input[type="number"] {
  -moz-appearance: textfield;
}

.opacity-slider {
  flex-shrink: 0;
  width: 80px;
  margin: 0;
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
