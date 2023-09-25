<template>
  <SidePanel :show-panel="showPanel">
    <template #search>
      <button
        v-tippy="{ placement: 'right' }"
        class="iconbutton close-button"
        type="button"
        content="Sluit detailweergave"
        aria-label="Sluit detailweergave"
        @click="closePanel"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="24"
          viewBox="0 0 24 24"
          width="24"
        >
          <path d="M0 0h24v24H0z" fill="none" />
          <path
            d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
          />
        </svg>
      </button>
      <h1></h1>
    </template>

    <template #default>
      <img
        v-if="firstFeature.image"
        :src="firstFeature.image"
        class="featured-image"
      />
      <div class="details">
        <h3>{{ firstFeature.title }}</h3>

        <markdown
          v-if="firstFeature.description"
          class="description"
          :source="firstFeature.description"
          :inline="false"
        />
      </div>

      <div class="links">
        <a v-if="firstFeature.link" :href="firstFeature.link" target="_parent">
          <svg
            width="20px"
            height="20px"
            viewBox="0 0 20 20"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
          >
            <g
              id="Page-1"
              stroke="none"
              stroke-width="1"
              fill="none"
              fill-rule="evenodd"
            >
              <g
                id="public_black_24dp"
                transform="translate(-2.000000, -2.000000)"
                fill="currentColor"
                fill-rule="nonzero"
              >
                <path
                  id="Shape"
                  d="M12,2 C6.48,2 2,6.48 2,12 C2,17.52 6.48,22 12,22 C17.52,22 22,17.52 22,12 C22,6.48 17.52,2 12,2 Z M4,12 C4,11.39 4.08,10.79 4.21,10.22 L8.99,15 L8.99,16 C8.99,17.1 9.89,18 10.99,18 L10.99,19.93 C7.06,19.43 4,16.07 4,12 Z M17.89,17.4 C17.63,16.59 16.89,16 15.99,16 L14.99,16 L14.99,13 C14.99,12.45 14.54,12 13.99,12 L7.99,12 L7.99,10 L9.99,10 C10.54,10 10.99,9.55 10.99,9 L10.99,7 L12.99,7 C14.09,7 14.99,6.1 14.99,5 L14.99,4.59 C17.92,5.77 20,8.65 20,12 C20,14.08 19.19,15.98 17.89,17.4 Z"
                ></path>
              </g>
            </g>
          </svg>
          Lees het verhaal op de website
          <svg
            width="14px"
            height="14px"
            viewBox="0 0 14 14"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
          >
            <g
              id="Page-1"
              stroke="none"
              stroke-width="1"
              fill="none"
              fill-rule="evenodd"
            >
              <g
                id="open_in_new_black_18dp-(1)"
                transform="translate(-2.000000, -2.000000)"
                fill="#000000"
                fill-rule="nonzero"
              >
                <path
                  id="Shape"
                  d="M14.25,14.25 L3.75,14.25 L3.75,3.75 L9,3.75 L9,2.25 L3.75,2.25 C2.9175,2.25 2.25,2.925 2.25,3.75 L2.25,14.25 C2.25,15.075 2.9175,15.75 3.75,15.75 L14.25,15.75 C15.075,15.75 15.75,15.075 15.75,14.25 L15.75,9 L14.25,9 L14.25,14.25 Z M10.5,2.25 L10.5,3.75 L13.1925,3.75 L5.82,11.1225 L6.8775,12.18 L14.25,4.8075 L14.25,7.5 L15.75,7.5 L15.75,2.25 L10.5,2.25 Z"
                ></path>
              </g>
            </g>
          </svg>
        </a>
      </div>
    </template>
  </SidePanel>
</template>

<script>
import Markdown from "./Markdown";
import SidePanel from "./SidePanel";

export default {
  name: "DetailPanel",
  components: {
    SidePanel,
    Markdown,
  },
  props: {
    features: Array,
    showPanel: Boolean,
  },
  computed: {
    firstFeature() {
      if (this.features && this.features.length > 0) {
        return this.features[0].getProperties();
      }

      return null;
    },
  },
  methods: {
    closePanel() {
      this.$emit("features-selected", []);
    },
  },
};
</script>

<style scoped>
h1 {
  font-size: var(--font-size-normal);
}

.close-button {
  width: var(--width-button-large);
  height: var(--width-button-large);
  border-radius: var(--radius-normal);
  border: 1px solid var(--color-grey-60);
}
.details {
  padding: var(--padding-screen);
}

.details ::v-deep(a) {
  color: var(--color-primary);
  text-decoration: none;
}

.details ::v-deep(a:hover),
.details ::v-deep(a:active) {
  text-decoration: underline;
}

h3 {
  margin: 0;
  font-size: var(--font-size-large);
}

p {
  margin: 16px 0 0;
}

dl {
  margin: 0;
}

dt {
  display: block;
  margin: 0 0 4px;
  font-weight: var(--font-weight-bold);
}

dd {
  margin: 0 0 16px;
}

a {
  color: var(--color-primary);
}

.description >>> ul {
  margin: 20px;
  list-style-type: disc;
}

.featured-image {
  width: 100%;
  margin-top: calc(var(--padding-screen) * -1 + var(--width-button-large) * -1);
}

.type {
  display: flex;
  align-items: center;
  font-size: var(--font-size-small);
  color: var(--color-text-grey);
}

.type img {
  margin-left: 5px;
}

.address {
  margin-top: 2px;
  font-size: var(--font-size-small);
}

.hide-button {
  margin-left: auto;
}

.links > * {
  box-sizing: border-box;
  min-height: 40px;
  display: flex;
  align-items: center;
  border-top: 1px solid var(--color-grey-30);
  padding: 8px var(--padding-screen) 9px;
  text-decoration: none;
}

.links > a {
  color: var(--color-primary);
}

.links > *:last-child {
  border-bottom: 1px solid var(--color-grey-30);
}

.links a:hover,
.links a:active {
  text-decoration: underline;
}

.links svg {
  flex-shrink: 0;
}

.links svg:first-child {
  margin-right: 8px;
}

.links svg:last-child:not(:first-child) {
  margin-left: auto;
}
</style>
