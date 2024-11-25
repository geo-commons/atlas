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
          <div class="description">
            <markdown :source="layer.metadata.description" />
          </div>
          <div v-if="layer.metadata.link" class="link">
            <a :href="layer.metadata.link" target="_blank">Meer informatie</a>
          </div>
        </div>
        <div v-if="layer.metadata" class="properties">
          <div v-if="layer.metadata.organization" class="property">
            <div class="key">Organisatie</div>
            <div class="value">
              <markdown :source="layer.metadata.organization" />
            </div>
          </div>
          <div v-if="layer.metadata.contact" class="property">
            <div class="key">Contactpersoon</div>
            <div class="value">
              <markdown :source="layer.metadata.contact" />
            </div>
          </div>
          <div v-if="layer.metadata.lineage" class="property">
            <div class="key">Herkomst dataset</div>
            <div class="value">
              <markdown :source="layer.metadata.lineage" />
            </div>
          </div>
          <div v-if="layer.metadata.updated" class="property">
            <div class="key">Bijgewerkt</div>
            <div class="value">
              <markdown :source="layer.metadata.updated" />
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
