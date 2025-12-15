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
        <div class="tw-mx-4">
          <div class="input-wrapper">
            <label for="title" class="setting-label">Titel</label>
            <vee-field id="title" name="title" type="text" as="input" rules="required" />
            <span class="warning-text">
              <vee-error-message name="title" />
            </span>
          </div>
          <div class="input-wrapper">
            <label for="slug" class="setting-label tw-flex tw-items-center tw-gap-2">
              Kort kenmerk
              <AdminFormInfoText
                :info-text="'Dit is een korte, unieke naam voor de kaart die in de URL zal worden gebruikt. Het mag geen spaties en speciale tekens bevatten.'"
              />
            </label>
            <vee-field id="slug" name="slug" type="text" as="input" rules="required" />
            <span class="warning-text">
              <vee-error-message name="slug" />
            </span>
          </div>
        </div>

        <div class="settings">
          <div class="setting __hover">
            <input id="published" v-model="data.published" type="checkbox" name="published" />
            <label for="published">Publiceer kaart</label>
            <AdminFormInfoText
              :info-text="'Markeer dit veld als Gepubliceerd om de kaart te publiceren en beschikbaar te maken voor andere gebruikers. Zet dit veld uit om de kaart te bewaren als concept en nog niet beschikbaar te maken voor andere gebruikers.'"
            />
          </div>
          <div class="setting __hover">
            <input id="show_in_overview" v-model="data.show_in_overview" type="checkbox" name="show_in_overview" />
            <label for="show_in_overview">Toon kaart in overzicht weergave</label>
            <AdminFormInfoText
              :info-text="'Schakel dit veld in om de kaart weer te geven in het overzicht van het dataportaal. Laat het uitgeschakeld om de kaart te verbergen in het overzicht, zelfs als deze gepubliceerd is.'"
            />
          </div>
          <button type="button" class="button __chevron setting" @click="() => $emit('show-panel', 'layers')">
            <LayerIcon class="icon setting-icon" />
            Lagen
            <ChevronRightIcon class="icon setting-chevron" />
          </button>
          <button type="button" class="button __chevron setting" @click="() => $emit('show-panel', 'thumbnail')">
            <ImageIcon class="icon setting-icon" />
            Thumbnail
            <ChevronRightIcon class="icon setting-chevron" />
          </button>
          <button type="button" class="button __chevron setting" @click="() => $emit('show-panel', 'about')">
            <i class="pi pi-file-edit icon setting-icon"></i>
            Kaartomschrijving
            <ChevronRightIcon class="icon setting-chevron" />
          </button>
        </div>

        <div class="settings">
          <div class="setting __hover">
            <input
              id="features.searchbar"
              v-model="data.features.searchbar"
              type="checkbox"
              name="features.searchbar"
            />
            <label for="features.searchbar">Toon zoekbalk</label>
          </div>

          <div class="setting __hover">
            <input
              id="features.datapanel"
              v-model="data.features.datapanel"
              type="checkbox"
              name="features.datapanel"
            />
            <label for="features.datapanel">Toon dataweergave</label>
          </div>

          <div class="setting __hover">
            <input
              id="features.selectarea"
              v-model="data.features.selectarea"
              type="checkbox"
              name="features.selectarea"
            />
            <label for="features.selectarea">Selecteer gebied</label>
          </div>

          <div class="setting __hover">
            <input id="features.measure" v-model="data.features.measure" type="checkbox" name="features.measure" />
            <label for="features.measure">Opmeten</label>
          </div>

          <div class="setting __hover">
            <input
              id="features.morepanel"
              v-model="data.features.morepanel"
              type="checkbox"
              name="features.morepanel"
            />
            <label for="features.morepanel">Meer opties</label>
          </div>

          <div class="setting __hover">
            <input id="features.gps" v-model="data.features.gps" type="checkbox" name="features.gps" />
            <label for="features.gps">GPS knop</label>
          </div>

          <div class="setting __hover">
            <input id="features.zoom" v-model="data.features.zoom" type="checkbox" name="features.zoom" />
            <label for="features.zoom">Zoomfunctie</label>
          </div>

          <div class="setting __hover">
            <input id="features.scale" v-model="data.features.scale" type="checkbox" name="features.scale" />
            <label for="features.scale">Toon schaal</label>
          </div>

          <div class="setting __hover">
            <input
              id="features.markerOnClick"
              v-model="data.features.markerOnClick"
              type="checkbox"
              name="features.markerOnClick"
            />
            <label for="features.markerOnClick">Prikker bij klik</label>
          </div>

          <div class="setting __hover">
            <input
              id="features.baselayer"
              v-model="data.features.baselayer"
              type="checkbox"
              name="features.baselayer"
            />
            <label for="features.baselayer">Basislagen</label>
          </div>

          <div class="setting __hover">
            <input
              id="features.layerlist"
              v-model="data.features.layerlist"
              type="checkbox"
              name="features.layerlist"
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
            <input id="features.legend" v-model="data.features.legend" type="checkbox" name="features.legend" />
            <label for="features.legend">Legenda</label>
          </div>

          <div class="setting __hover">
            <input id="features.list" v-model="data.features.list" type="checkbox" name="features.list" />
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
            <input id="features.filters" v-model="data.features.filters" type="checkbox" name="features.filters" />
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
            <input
              id="features.compareLayers"
              v-model="data.features.compareLayers"
              type="checkbox"
              name="features.compareLayers"
            />
            <label for="features.compareLayers">Kaartlagen vergelijken</label>
          </div>

          <div class="setting __hover">
            <input id="features.draw" v-model="data.features.draw" type="checkbox" name="features.draw" />
            <label for="features.draw">Tekenen</label>
          </div>

          <div class="setting __hover">
            <input
              id="features.edit_layer_features"
              v-model="data.features.edit_layer_features"
              type="checkbox"
              name="features.edit_layer_features"
            />
            <label for="features.edit_layer_features">CRUD Functionaliteit</label>
          </div>

          <div class="setting __hover">
            <input
              id="features.panoramaViewers"
              v-model="data.features.panoramaViewers"
              type="checkbox"
              name="features.panoramaViewers"
            />
            <label for="features.panoramaViewers">Rondkijkfoto</label>
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
        const formData = { ...this.data, title: formValues.title, slug: formValues.slug };
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

.setting-label {
  font-weight: var(--font-weight-bold);
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
