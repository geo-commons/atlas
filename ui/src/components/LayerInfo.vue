<template>
  <tippy
    ref="tippyRef"
    theme="popover"
    trigger="click"
    :distance="8"
    :delay="[0, 0]"
    :a11y="null"
    :interactive="true"
    :append-to="appendEl ?? undefined"
    boundary="viewport"
    placement="auto"
    :flip="true"
    :shift="true"
    :on-show="onTippyShow"
  >
    <button
      v-tippy="{ content: 'Meer informatie', touch: false }"
      :class="{ iconbutton: true, showAlways: showAlways }"
      aria-label="Toon meer informatie"
    >
      <InformationCircleIcon class="icon __small" />
    </button>
    <template #content>
      <div class="container">
        <div class="heading">
          <h3 class="title">{{ layer.title }}</h3>
          <div v-if="layer.description" class="description">
            <markdown :source="layer.description" />
          </div>
        </div>
        <div v-if="layer.metadataset" class="properties">
          <div v-if="layer.metadataset?.abstract" class="property">
            <div class="key">Toelichting dataset</div>
            <div class="value">
              <markdown :source="layer.metadataset?.abstract" />
            </div>
          </div>
          <div v-if="layer.metadataset?.source_organization" class="property">
            <div class="key">Organisatie</div>
            <div class="value">
              <markdown :source="layer.metadataset?.source_organization" />
            </div>
          </div>
          <div v-if="layer.metadataset?.source_name_internal && isLoggedIn" class="property">
            <div class="key">
              Contactpersoon
              <VisibilityIndicator visibility="Intern" />
            </div>
            <div class="value">
              {{ layer.metadataset.source_name_internal }}
            </div>
          </div>
          <div v-if="layer.metadataset?.source_name_public" class="property">
            <div class="key">Contactpersoon</div>
            <div class="value">
              {{ layer.metadataset.source_name_public }}
            </div>
          </div>
          <div v-if="layer.metadataset?.source_email_public" class="property">
            <div class="key">E-mailadres</div>
            <div class="value">
              <a
                class="tw-text-blue-600 tw-no-underline hover:tw-underline"
                :href="`mailto:${layer.metadataset?.source_email_public?.toLowerCase()}`"
              >
                {{ layer.metadataset?.source_email_public?.toLowerCase() }}
              </a>
            </div>
          </div>
          <div v-if="layer.metadataset?.source_origin" class="property">
            <div class="key">Herkomst dataset</div>
            <div class="value">
              <markdown :source="layer.metadataset?.source_origin" />
            </div>
          </div>
          <div v-if="layer.metadataset?.last_updated" class="property">
            <div class="key">Bijgewerkt</div>
            <div class="value">
              {{ layer.metadataset.last_updated }}
            </div>
          </div>
          <div v-if="layer.metadataset?.update_frequency" class="property">
            <div class="key">Updatefrequentie</div>
            <div class="value">
              {{ layer.metadataset.update_frequency }}
            </div>
          </div>
          <div v-if="layer.metadataset?.statement" class="property">
            <div class="key">Doel van de vervaardiging</div>
            <div class="value">
              <markdown :source="layer.metadataset.statement" />
            </div>
          </div>
          <div class="tw-mt-4">
            <Button outlined class="!tw-font-medium tw-w-full" aria-label="Meer informatie" @click="openModal">
              Meer informatie
            </Button>
          </div>
        </div>
      </div>
    </template>
  </tippy>

  <!-- Modal with all metadataset information -->
  <LayerInfoModal v-model="showModal" :layer="layer" :is-logged-in="isLoggedIn" />
</template>

<script setup lang="ts">
import VisibilityIndicator from "@/components/VisibilityIndicator.vue";
import { useGlobalStore } from "@/stores";
import type { IMetadataset } from "@/types/metadataset";
import { isMobile } from "@/utils/helpers";
import { computed, onMounted, ref } from "vue";
import { Tippy } from "vue-tippy";
import InformationCircleIcon from "../assets/icons/information-circle-icon.svg";
import LayerInfoModal from "./LayerInfoModal.vue";
import Markdown from "./Markdown";

export interface LayerInfoLayer {
  title: string;
  description?: string;
  metadataset?: Partial<IMetadataset>;
}

interface Props {
  layer: LayerInfoLayer;
  showAlways?: boolean;
}

defineProps<Props>();

// Type for Tippy component instance with tippy property
interface TippyInstance extends InstanceType<typeof Tippy> {
  tippy?: {
    hide: () => void;
  };
}

const tippyRef = ref<TippyInstance | null>(null);
const appendEl = ref<Element | null>(null);
const showModal = ref(false);

const globalStore = useGlobalStore();
const isLoggedIn = computed(() => !!globalStore.user);

const openModal = () => {
  // Close the tippy popover when opening the modal
  if (tippyRef.value?.tippy) {
    tippyRef.value.tippy.hide();
  }
  showModal.value = true;
};

// On mobile the popover does not fit well, so open the full modal directly and
// cancel the popover by returning false from this tippy lifecycle hook.
const onTippyShow = (): false | void => {
  const mobile = isMobile();

  if (mobile) {
    showModal.value = true;
    return false;
  }
};

onMounted(() => {
  // The vue tippy pop up does not escape the parent container
  // when the tippy popup is placed in a scrollable container.
  // Using the append-to property on the map-container fixes this.
  appendEl.value = document.getElementById("map-container");
});
</script>

<style scoped>
.iconbutton {
  width: 24px;
  height: 24px;
  border-radius: 50%;
}

.iconbutton:not(.showAlways) {
  opacity: 0;
}

.layer:hover .iconbutton,
.sublayer:hover .iconbutton,
.tippy-active > .iconbutton,
.keyboard-user .iconbutton:focus {
  opacity: 1;
}

.container {
  min-width: 300px;
  max-width: 350px;
  font-weight: normal;
  text-align: left;
}

.heading {
  padding: 10px 16px;
  text-align: center;
  border-bottom: 1px solid var(--color-grey-60);
}

.title {
  margin: 0 0 4px;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-bold);
}

.properties {
  padding: 8px 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.property {
  display: flex;
  flex-direction: column;
  padding: 3px 0;
}

.key {
  padding-right: 8px;
  color: var(--color-text-grey);
}

.value {
  font-weight: var(--font-weight-normal);
  overflow-wrap: break-word;
}
</style>
