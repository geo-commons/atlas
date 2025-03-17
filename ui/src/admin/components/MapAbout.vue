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
        <i class="pi pi-file-edit icon tw-flex tw-items-center" />
        Kaartomschrijving
      </h1>
    </template>
    <template #default>
      <div class="tw-px-3">
        <ExplainerMessage class="tw-pt-4">
          <template #icon>
            <InformationCircleIcon />
          </template>
          <template #explainer>
            De kaartomschrijving biedt extra context en details over de kaart in een zijbalk.
            <br />
            <br />
            Voeg hier extra uitleg toe om gebruikers beter te informeren over het thema of de inhoud van de kaart.
          </template>
        </ExplainerMessage>
        <div class="layer-setting-toggle tw-flex tw-items-center tw-justify-between tw-gap-2 tw-my-4">
          <label for="show-about">Toon kaartomschrijving</label>
          <ToggleSwitch v-model="data.features.showAbout" input-id="show-about" />
        </div>
      </div>

      <div v-if="data?.features?.showAbout" class="tw-px-3">
        <hr class="tw-my-4 tw-border-t tw-border-grey-60" />

        <div class="layer-setting-toggle tw-flex tw-items-center tw-justify-between tw-gap-2 tw-my-4">
          <div class="tw-flex tw-items-center tw-gap-2">
            <label for="show-thumbnail">Toon thumbnail in header</label>
            <i
              v-if="!data?.thumbnail"
              v-tippy="{ content: 'Selecteer eerst een thumbnail afbeelding om deze optie te kunnen gebruiken' }"
              class="pi pi-info-circle tw-text-grey-80"
            />
          </div>
          <ToggleSwitch v-model="thumbnailEnabled" input-id="show-thumbnail" :disabled="!data?.thumbnail" />
        </div>

        <div class="layer-setting-toggle tw-flex tw-items-center tw-justify-between tw-gap-2 tw-my-4">
          <label for="show-button">Toon 'Kaart delen' knop</label>
          <ToggleSwitch v-model="data.features.showAboutButton" input-id="show-button" />
        </div>

        <div class="title-wrapper">
          <label for="title" class="setting-label">Header titel</label>
          <input v-model="data.about_title" type="text" name="title" placeholder="Titel" maxlength="128" />
        </div>

        <div class="tw-my-3">
          <label for="editor" class="setting-label">Zijbalk tekst</label>
          <Editor id="editor" v-model="data.about" editor-style="height: 420px">
            <template #toolbar>
              <span class="ql-formats">
                <select class="ql-header" defaultValue="0">
                  <option value="2">Titel</option>
                  <option value="">Normaal</option>
                </select>
              </span>
              <span class="ql-formats">
                <button v-tooltip.bottom="'Bold'" class="ql-bold"></button>
                <button v-tooltip.bottom="'Nummerlijst'" class="ql-list" value="ordered"></button>
              </span>
              <span class="ql-formats">
                <button v-tooltip.bottom="'Link'" class="ql-link"></button>
                <button v-tooltip.bottom="'Image'" class="ql-image"></button>
              </span>
            </template>
          </Editor>
        </div>
      </div>
    </template>
  </AdminSidePanel>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import AdminSidePanel from "@/admin/components/AdminSidePanel.vue";
import ArrowLeftIcon from "@/assets/icons/arrow-left-icon.svg";
import { MapAboutData, MapAboutEmits, MapEvents } from "@/types/models";
import InformationCircleIcon from "@/assets/icons/information-circle-icon.svg";
import ExplainerMessage from "@/components/ExplainerMessage.vue";

const props = defineProps<{
  initialData: MapAboutData;
}>();

const emit = defineEmits<MapAboutEmits>();

const loading = ref<boolean>(false);
const data = ref<MapAboutData>(props.initialData);

const thumbnailEnabled = computed({
  get: () => {
    const { thumbnail, features } = data.value || {};
    return thumbnail ? features?.showAboutThumbnail : false;
  },
  set: (val) => {
    data.value.features.showAboutThumbnail = val;
    emitUpdate();
  },
});

const back = () => {
  emit(MapEvents.SHOW_FORM);
};

const emitUpdate = () => {
  const { about, about_title, thumbnail, features } = data.value;
  emit(MapEvents.UPDATE_ABOUT, {
    about,
    about_title,
    thumbnail,
    features: { ...features },
  });
};
</script>

<style lang="scss">
label {
  font-weight: var(--font-weight-bold);
  width: 100%;
}

.p-toggleswitch {
  flex-shrink: 0;
}

.p-editor {
  .ql-container {
    font-family: var(--font-family-admin);
  }

  .p-editor-content .ql-editor {
    p {
      line-height: 1.5;
      margin: 1rem 0;
      font-size: 1rem;
    }

    a {
      color: var(--color-primary);
      text-decoration: none;

      &:hover {
        text-decoration: underline;
      }
    }

    .content__link-icon {
      font-size: 0.8rem;
    }

    img {
      width: 100%;
      border-radius: 0.5rem;
    }
  }
}
</style>
