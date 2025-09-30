<template>
  <tippy
    theme="popover"
    trigger="click"
    :distance="8"
    :delay="[0, 0]"
    :a11y="null"
    :interactive="true"
    :append-to="appendEl"
  >
    <button
      v-tippy
      content="Meer informatie"
      :class="{ iconbutton: true, showAlways: showAlways }"
      aria-label="Toon meer informatie"
    >
      <InformationCircleIcon class="icon __small" />
    </button>
    <template #content>
      <div class="container">
        <div class="heading">
          <h3 class="title">{{ layer.title }}</h3>
          <!-- Use metadataset abstract if available, fallback to old metadata description -->
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
          <div v-if="layer.metadataset?.source_email_public" class="property">
            <div class="key">Contactpersoon</div>
            <div class="value">
              <markdown :source="layer.metadataset?.source_email_public" />
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
              <markdown :source="layer.metadataset?.last_updated" />
            </div>
          </div>
          <div v-if="layer.metadataset?.update_frequency" class="property">
            <div class="key">Updatefrequentie</div>
            <div class="value">
              <markdown :source="layer.metadataset.update_frequency" />
            </div>
          </div>
          <div v-if="layer.metadataset?.statement" class="property">
            <div class="key">Doel van de vervaardiging</div>
            <div class="value">
              <markdown :source="layer.metadataset.statement" />
            </div>
          </div>
        </div>
      </div>
    </template>
  </tippy>
</template>

<script>
import Markdown from "./Markdown";
import InformationCircleIcon from "../assets/icons/information-circle-icon.svg";
import { Tippy } from "vue-tippy";

export default {
  name: "LayerInfo",
  components: {
    Tippy,
    Markdown,
    InformationCircleIcon,
  },
  props: {
    layer: Object,
    showAlways: Boolean,
  },
  data() {
    return {
      appendEl: null,
    };
  },
  mounted() {
    // The vue tippy pop up does not escape the parent container
    // when the tippy popup is placed in a scrollable container.
    // Using the append-to property on the map-container fixes this.
    this.appendEl = document.getElementById("map-container");
    this.markdownOptions = {
      linkify: true,
    };
  },
};
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
}
</style>
