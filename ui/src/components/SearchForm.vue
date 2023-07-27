<template>
  <div class="search-wrapper" :class="{ showBorder }">
    <form class="search" autocomplete="off" method="GET" @submit="onSubmit">
      <DataPanelButton
        v-if="
          $listeners['show-data-panel'] &&
          !isEmbed &&
          hasVisibleLayers &&
          hasDatapanel
        "
        @show-data-panel="showDataPanel()"
      />

      <slot></slot>

      <div class="buttons">
        <button
          v-tippy="{ placement: 'bottom', theme: 'primary' }"
          class="iconbutton search-button"
          type="submit"
          content="Zoek"
          aria-label="Zoek"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24"
            viewBox="0 0 24 24"
            width="24"
          >
            <path d="M0 0h24v24H0V0z" fill="none" />
            <path
              fill="currentColor"
              d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
            />
          </svg>
        </button>
      </div>
    </form>
    <slot name="suggestions"></slot>
  </div>
</template>

<script>
import { mapState } from "vuex";
import DataPanelButton from "./DataPanelButton.vue";

export default {
  name: "SearchForm",
  components: {
    DataPanelButton,
  },
  props: {
    showBorder: Boolean,
    hasVisibleLayers: Boolean,
    features: Object,
  },
  computed: {
    ...mapState({
      isEmbed: (state) => state.isEmbed,
    }),
    hasDatapanel() {
      // Check if the feature config datapanel exists and is of type bolean otherwise default to true.
      if (typeof this.features["datapanel"] == "boolean") {
        return this.features.datapanel;
      }

      return true;
    },
  },
  methods: {
    onSubmit(e) {
      e.preventDefault();
      this.$emit("on-submit");
    },
    showDataPanel() {
      this.$emit("show-data-panel");
    },
    onClose() {
      this.$emit("on-close");
    },
  },
};
</script>

<style scoped>
.search-wrapper {
  position: relative;
  width: 100%;
  background: white;
  border-radius: var(--radius-normal);
  overflow: hidden;
  transition: box-shadow 0.1s;
}

.search-wrapper:not(.showBorder) {
  box-shadow: var(--shadow-normal);
}

.search-wrapper.showBorder {
  border: 1px solid var(--color-grey-60);
}

.search-wrapper.showBorder .search {
  height: calc(var(--width-button-large) - 2px);
}

.search {
  display: flex;
  height: var(--width-button-large);
  width: 100%;
}

.search > *,
.buttons > * {
  height: 100%;
}

.search input {
  width: 100%;
  padding-left: 16px;
}

.buttons {
  flex-shrink: 0;
  display: flex;
}

.toggle-button {
  width: var(--width-button-large);
  border-right: 1px solid var(--color-grey-50);
}

.search-button {
  position: relative;
  width: 48px;
}

.search-button > * {
  position: relative;
}

.search-button:not([disabled]):hover {
  background: transparent;
}

.search-button:not([disabled]):active {
  background: transparent;
}

.search-button:before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: var(--width-button-large);
  height: var(--width-button-large);
  margin: auto;
  border-radius: 50%;
}

.iconbutton:not([disabled]):hover:before {
  background: var(--color-grey-40);
}

.iconbutton:not([disabled]):active:before {
  background: var(--color-grey-50);
}

.search-button:not([disabled]) {
  color: var(--color-primary);
}

.clear-button {
  width: var(--width-button-large);
  border-left: 1px solid var(--color-grey-50);
}

.results {
  width: 100%;
  border-top: 1px solid var(--color-grey-50);
  padding: 12px 0;
}

.list a {
  display: block;
  color: #4285f4;
  text-decoration: none;
  padding: 3px 16px;
}

.list a:hover {
  text-decoration: underline;
}
</style>
