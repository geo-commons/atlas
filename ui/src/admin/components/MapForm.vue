<template>
  <AdminSidePanel>
    <template #header>
      <h1>
        <MapIcon class="icon" />
        Kaart
      </h1>
    </template>

    <template #default>
      <vee-form ref="mapForm" method="POST" class="map-form" :initial-values="initialData" @submit="submitForm">
        <div v-if="!data.is_main" class="tw-mx-4">
          <div class="input-wrapper">
            <label for="title" class="tw-font-bold">Titel</label>
            <vee-field id="title" v-slot="{ value, handleChange, handleBlur }" name="title" rules="required">
              <InputText id="title" :model-value="value" @update:model-value="handleChange" @blur="handleBlur" />
            </vee-field>
            <span class="warning-text">
              <vee-error-message name="title" />
            </span>
          </div>
          <div class="input-wrapper">
            <label for="slug" class="setting-label tw-flex tw-items-center tw-gap-2 tw-font-bold">
              Kort kenmerk
              <AdminFormInfoText
                :info-text="'Dit is een korte, unieke naam voor de kaart die in de URL zal worden gebruikt. Het mag geen spaties en speciale tekens bevatten.'"
              />
            </label>
            <vee-field id="slug" v-slot="{ value, handleChange, handleBlur }" name="slug" rules="required">
              <InputText id="slug" :model-value="value" @update:model-value="handleChange" @blur="handleBlur" />
            </vee-field>
            <span class="warning-text">
              <vee-error-message name="slug" />
            </span>
          </div>
          <div class="input-wrapper">
            <label for="slug" class="setting-label tw-flex tw-items-center tw-gap-2 tw-font-bold">
              Portaal beschrijving
              <AdminFormInfoText
                :info-text="'Dit is de beschrijving van de kaart die in het dataportaal wordt getoond.'"
              />
            </label>
            <vee-field id="description" v-slot="{ value, handleChange, handleBlur }" name="description">
              <Textarea id="description" :model-value="value" @update:model-value="handleChange" @blur="handleBlur" />
            </vee-field>
            <span class="warning-text">
              <vee-error-message name="description" />
            </span>
          </div>
          <div class="input-wrapper">
            <label for="slug" class="setting-label tw-flex tw-items-center tw-gap-2 tw-font-bold">
              Zoektermen
              <AdminFormInfoText
                :info-text="'Dit is de lijst van zoektermen die gebruikt worden om de kaart te vinden in het dataportaal. Voer één zoekterm per regel in.'"
              />
            </label>
            <vee-field id="keywords" v-slot="{ value, handleChange, handleBlur }" name="keywords">
              <Textarea id="keywords" :model-value="value" @update:model-value="handleChange" @blur="handleBlur" />
            </vee-field>
            <span class="warning-text">
              <vee-error-message name="keywords" />
            </span>
          </div>
        </div>

        <div class="settings">
          <div v-if="!data.is_main" class="setting __hover">
            <Checkbox
              input-id="published"
              :model-value="data.published"
              name="published"
              binary
              @update:model-value="(value) => (data.published = value)"
            />
            <label for="published">Publiceer kaart</label>
            <AdminFormInfoText
              :info-text="'Markeer dit veld als Gepubliceerd om de kaart te publiceren en beschikbaar te maken voor andere gebruikers. Zet dit veld uit om de kaart te bewaren als concept en nog niet beschikbaar te maken voor andere gebruikers.'"
            />
          </div>
          <div v-if="!data.is_main" class="setting __hover">
            <Checkbox
              input-id="show_in_overview"
              :model-value="data.show_in_overview"
              name="show_in_overview"
              binary
              @update:model-value="(value) => (data.show_in_overview = value)"
            />
            <label for="show_in_overview">Toon kaart in het dataportaal</label>
            <AdminFormInfoText
              :info-text="'Schakel dit veld in om de kaart weer te geven in het overzicht van het dataportaal. Laat het uitgeschakeld om de kaart te verbergen in het overzicht, zelfs als deze gepubliceerd is.'"
            />
          </div>
          <div class="tw-p-4">
            <Message v-if="data.is_main">
              Dit is de hoofdkaart. Deze is altijd gepubliceerd, wordt niet in het dataportaal getoond en is alleen via
              /atlas/ bereikbaar.
            </Message>
          </div>
          <button
            type="button"
            class="button __chevron setting !tw-font-normal"
            @click="() => $emit('show-panel', 'layers')"
          >
            <LayerIcon class="icon setting-icon" />
            Lagen
            <ChevronRightIcon class="icon setting-chevron" />
          </button>
          <button
            type="button"
            class="button __chevron setting !tw-font-normal"
            @click="() => $emit('show-panel', 'thumbnail')"
          >
            <ImageIcon class="icon setting-icon" />
            Thumbnail
            <ChevronRightIcon class="icon setting-chevron" />
          </button>
          <button
            type="button"
            class="button __chevron setting !tw-font-normal"
            @click="() => $emit('show-panel', 'about')"
          >
            <i class="pi pi-file-edit icon setting-icon"></i>
            Kaartomschrijving
            <ChevronRightIcon class="icon setting-chevron" />
          </button>
        </div>

        <div class="settings">
          <div class="setting __hover">
            <Checkbox
              input-id="features.searchbar"
              :model-value="data.features.searchbar"
              name="features.searchbar"
              binary
              @update:model-value="(value) => (data.features.searchbar = value)"
            />
            <label for="features.searchbar">Toon zoekbalk</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.datapanel"
              :model-value="data.features.datapanel"
              name="features.datapanel"
              binary
              @update:model-value="(value) => (data.features.datapanel = value)"
            />
            <label for="features.datapanel">Toon dataweergave</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.selectarea"
              :model-value="data.features.selectarea"
              name="features.selectarea"
              binary
              @update:model-value="(value) => (data.features.selectarea = value)"
            />
            <label for="features.selectarea">Selecteer gebied</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.measure"
              :model-value="data.features.measure"
              name="features.measure"
              binary
              @update:model-value="(value) => (data.features.measure = value)"
            />
            <label for="features.measure">Opmeten</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.morepanel"
              :model-value="data.features.morepanel"
              name="features.morepanel"
              binary
              @update:model-value="(value) => (data.features.morepanel = value)"
            />
            <label for="features.morepanel">Meer opties</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.gps"
              :model-value="data.features.gps"
              name="features.gps"
              binary
              @update:model-value="(value) => (data.features.gps = value)"
            />
            <label for="features.gps">GPS knop</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.zoom"
              :model-value="data.features.zoom"
              name="features.zoom"
              binary
              @update:model-value="(value) => (data.features.zoom = value)"
            />
            <label for="features.zoom">Zoomfunctie</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.scale"
              :model-value="data.features.scale"
              name="features.scale"
              binary
              @update:model-value="(value) => (data.features.scale = value)"
            />
            <label for="features.scale">Toon schaal</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.markerOnClick"
              :model-value="data.features.markerOnClick"
              name="features.markerOnClick"
              binary
              @update:model-value="(value) => (data.features.markerOnClick = value)"
            />
            <label for="features.markerOnClick">Prikker bij klik</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.baselayer"
              :model-value="data.features.baselayer"
              name="features.baselayer"
              binary
              @update:model-value="(value) => (data.features.baselayer = value)"
            />
            <label for="features.baselayer">Basislagen</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.layerlist"
              :model-value="data.features.layerlist"
              name="features.layerlist"
              binary
              @update:model-value="(value) => (data.features.layerlist = value)"
            />
            <label for="features.layerlist">Lagenlijst</label>
            <button
              v-if="data.features.layerlist"
              type="button"
              class="button __transparent-bg __no-hover __chevron"
              @click="() => $emit('show-panel', 'layerList')"
            >
              <ChevronRightIcon class="icon setting-chevron" />
            </button>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.legend"
              :model-value="data.features.legend"
              name="features.legend"
              binary
              @update:model-value="(value) => (data.features.legend = value)"
            />
            <label for="features.legend">Legenda</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.layerPanelCollapsed"
              :model-value="data.features.layerPanelCollapsed"
              name="features.layerPanelCollapsed"
              binary
              @update:model-value="(value) => (data.features.layerPanelCollapsed = value)"
            />
            <label for="features.layerPanelCollapsed">Lagenlijst en legenda standaard gesloten</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.list"
              :model-value="data.features.list"
              name="features.list"
              binary
              @update:model-value="(value) => (data.features.list = value)"
            />
            <label for="features.list">Lijstweergave</label>

            <button
              v-if="data.features.list"
              type="button"
              class="button __transparent-bg __no-hover __chevron"
              @click="() => $emit('show-panel', 'list')"
            >
              <ChevronRightIcon class="icon setting-chevron" />
            </button>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.filters"
              :model-value="data.features.filters"
              name="features.filters"
              binary
              @update:model-value="(value) => (data.features.filters = value)"
            />
            <label for="features.filters">Filters</label>

            <button
              v-if="data.features.filters"
              type="button"
              class="button __transparent-bg __no-hover __chevron"
              @click="() => $emit('show-panel', 'filters')"
            >
              <ChevronRightIcon class="icon setting-chevron" />
            </button>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.compareLayers"
              :model-value="data.features.compareLayers"
              name="features.compareLayers"
              binary
              @update:model-value="(value) => (data.features.compareLayers = value)"
            />
            <label for="features.compareLayers">Kaartlagen vergelijken</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.draw"
              :model-value="data.features.draw"
              name="features.draw"
              binary
              @update:model-value="(value) => (data.features.draw = value)"
            />
            <label for="features.draw">Tekenen</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.edit_layer_features"
              :model-value="data.features.edit_layer_features"
              name="features.edit_layer_features"
              binary
              @update:model-value="(value) => (data.features.edit_layer_features = value)"
            />
            <label for="features.edit_layer_features">CRUD Functionaliteit</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.panoramaViewers"
              :model-value="data.features.panoramaViewers"
              name="features.panoramaViewers"
              binary
              @update:model-value="(value) => (data.features.panoramaViewers = value)"
            />
            <label for="features.panoramaViewers">Rondkijkfoto</label>
          </div>

          <div class="setting __hover">
            <Checkbox
              input-id="features.resetButton"
              :model-value="data.features.resetButton"
              name="features.resetButton"
              binary
              @update:model-value="(value) => (data.features.resetButton = value)"
            />
            <label for="features.resetButton">Herstelknop</label>
          </div>
        </div>
      </vee-form>
    </template>

    <template #footer>
      <div class="tw-flex tw-gap-2 tw-justify-end tw-w-full">
        <router-link to="/maps" class="button __tertiary">Annuleren</router-link>
        <SplitButton label="Opslaan" :model="items" @click="submitForm(true)" />
      </div>
    </template>
  </AdminSidePanel>
</template>

<script>
import LayerIcon from "../../assets/icons/layer-icon.svg";
import ImageIcon from "../../assets/icons/image-icon.svg";
import ChevronRightIcon from "../../assets/icons/chevron-right-icon.svg";
import MapIcon from "../../assets/icons/map-icon.svg";
import AdminSidePanel from "@/admin/components/AdminSidePanel.vue";
import AdminFormInfoText from "@/admin/components/AdminFormInfoText.vue";
import { ErrorMessage as VeeErrorMessage, Field as VeeField, Form as VeeForm } from "vee-validate";

export default {
  name: "MapForm",
  components: {
    AdminFormInfoText,
    LayerIcon,
    ImageIcon,
    ChevronRightIcon,
    MapIcon,
    AdminSidePanel,
    VeeForm,
    VeeField,
    VeeErrorMessage,
  },
  props: {
    initialData: Object,
    errors: Object,
  },
  emits: ["submit", "show-panel"],
  data() {
    return {
      data: this.initialData || { features: {} },
      items: [
        {
          label: "Opslaan en sluiten",
          command: () => this.submitForm(false),
        },
      ],
    };
  },
  watch: {
    initialData: {
      handler(newInitialData) {
        this.data = newInitialData || { features: {} };
      },
    },
    errors: {
      handler(newErrors) {
        if (newErrors) {
          this.setServerErrors(newErrors);
        }
      },
    },
  },
  methods: {
    async submitForm(continueEditing = false) {
      // Note: not the nicest solution but for now the best way without refactoring the entire form to vee-validate.
      const values = await this.$refs.mapForm.validate();
      if (values.valid) {
        const formValues = this.$refs.mapForm.values;
        const formData = {
          ...this.data,
          title: formValues.title,
          slug: formValues.slug,
          description: formValues.description,
          keywords: formValues.keywords,
        };
        this.$emit("submit", formData, continueEditing);
      }
    },
    setServerErrors(errors) {
      Object.keys(errors).forEach((fieldName) => {
        const errorMessage = errors[fieldName][0];
        this.$refs.mapForm.setFieldError(fieldName, errorMessage);
      });
    },
  },
};
</script>

<style scoped>
.map-form {
  display: flex;
  flex-direction: column;
  gap: 32px;
  height: 100%;
}

.input-wrapper {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
}

.button.setting {
  background: var(--color-backdrop);
  background: transparent;
  border-radius: 0;
}

.button.setting:not([disabled]):hover {
  background-color: var(--color-admin-primary-hover);
}

.admin-button-wrapper {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 12px;
  margin-top: auto;
}

.setting-icon {
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
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
