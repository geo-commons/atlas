<template>
  <SidePanel
    initial-size-medium
    :show-panel="showPanel && features?.showAbout"
    class="about-panel tw-flex tw-flex-col tw-overflow-y-auto"
    :expandable="false"
    @close-side-panel="closeAbout"
  >
    <template #header>
      <header
        class="about-panel__header tw-flex tw-flex-col tw-relative tw-z-[1] tw-shrink-0"
        :style="
          features?.showAboutThumbnail && (map?.thumbnail || thumbnail || '')
            ? `--header-bg: url('${map?.thumbnail || thumbnail || ''}')`
            : ''
        "
      >
        <div class="tw-p-4 tw-mt-auto tw-text-white">
          <h1>{{ aboutTitle || map?.about_title || "" }}</h1>
        </div>

        <button
          v-tippy="{ placement: 'right' }"
          class="iconbutton __normal __outline tw-absolute tw-top-4 tw-right-4 tw-z-2"
          type="button"
          content="Sluit paneel"
          aria-label="Sluit paneel"
          @click="closeAbout"
        >
          <close-icon class="icon" />
        </button>
      </header>
    </template>
    <template #default>
      <markdown
        v-if="about || map?.about"
        class="about-panel__content tw-p-4"
        :source="processedAbout"
        :inline="false"
      />
    </template>

    <template v-if="features?.showAboutButton" #footer>
      <div class="tw-p-4">
        <Button
          :label="copyButtonLabel"
          outlined
          severity="secondary"
          :icon="copyButtonIcon"
          class="tw-w-full"
          @click="copyMapLink()"
        />
      </div>
    </template>
  </SidePanel>
</template>

<script setup lang="ts">
import CloseIcon from "@/assets/icons/close-icon.svg";
import { useGlobalStore } from "@/stores";
import { AboutPanelData, AboutPanelEmits, MapEvents } from "@/types/models";
import { computed, ref } from "vue";
import SidePanel from "./SidePanel.vue";
import Markdown from "./Markdown";

const props = defineProps<AboutPanelData>();

type IMapGlobalStore = {
  about?: string;
  about_title?: string;
  thumbnail?: string;
  slug?: string;
  features?: {
    showAbout?: boolean;
    showAboutButton?: boolean;
    showAboutThumbnail?: boolean;
  };
};

const map = computed(() => {
  return useGlobalStore().map as IMapGlobalStore | null;
});

const emit = defineEmits<AboutPanelEmits>();

const copyButtonLabel = ref("Kaart delen");
const copyButtonIcon = ref("pi pi-upload");

const copyMapLink = () => {
  const mapLink = `${window.location.origin}/atlas/maps/${map.value?.slug}`;
  navigator.clipboard.writeText(mapLink);

  copyButtonLabel.value = "Kaartlink gekopieerd";
  copyButtonIcon.value = "pi pi-copy";

  setTimeout(() => {
    copyButtonLabel.value = "Kaart delen";
    copyButtonIcon.value = "pi pi-upload";
  }, 2000);
};

const closeAbout = () => {
  emit(MapEvents.TOGGLE_ABOUT);
};

const processedAbout = computed(() => {
  if (!props.about && !map.value?.about) return "";

  if (props.about) return props.about;

  if (map.value && map.value.about) return map.value.about;

  return "";
});
</script>

<style lang="scss">
.about-panel__header {
  background-size: cover;
  background-image: linear-gradient(rgba(2, 0, 40, 0.2) 20%, rgba(2, 0, 40, 0.75)), var(--header-bg);
  background-position: center;
  background-repeat: no-repeat;
  height: 14rem;
  width: 100%;
  background-color: var(--color-primary);
}

.about-panel__content {
  p {
    line-height: 1.5;
    margin: 0 0 1rem 0;
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
  strong {
    font-weight: 700;
  }
  ul, ol {
    @apply tw-list-disc tw-pl-4;
  }

  h1:not(:first-child),
  h2:not(:first-child),
  h3:not(:first-child),
  h4:not(:first-child),
  h5:not(:first-child),
  h6:not(:first-child) {
    line-height: 1.5;
    margin: 1rem 0 0.5rem 0;
  }

  h1:is(:first-child),
  h2:is(:first-child),
  h3:is(:first-child),
  h4:is(:first-child),
  h5:is(:first-child),
  h6:is(:first-child) {
    line-height: 1.5;
    margin: 0 0 0.5rem 0;
  }

  img {
    width: 100%;
    border-radius: 0.5rem;
  }
}
</style>
