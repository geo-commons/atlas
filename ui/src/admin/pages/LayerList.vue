<template>
  <div class="container">
    <div class="section">
      <button>
        <router-link to="/layer/create" class="button __tertiary __large">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24px"
            viewBox="0 0 24 24"
            width="24px"
            fill="#000000"
          >
            <path d="M0 0h24v24H0V0z" fill="none" />
            <path
              d="M13 7h-2v4H7v2h4v4h2v-4h4v-2h-4V7zm-1-5C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"
            />
          </svg>
          Maak laag
        </router-link>
      </button>
    </div>
    <div class="search-wrapper">
      <svg
        width="18px"
        height="18px"
        viewBox="0 0 18 18"
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
      >
        <g
          id="Admin"
          stroke="none"
          stroke-width="1"
          fill="none"
          fill-rule="evenodd"
        >
          <g
            id="Kaart---Lagen"
            transform="translate(-45.000000, -183.000000)"
            fill="#000000"
            fill-rule="nonzero"
          >
            <g
              id="search_black_24dp"
              transform="translate(42.000000, 180.000000)"
            >
              <path
                id="Shape"
                d="M15.5,14 L14.71,14 L14.43,13.73 C15.41,12.59 16,11.11 16,9.5 C16,5.91 13.09,3 9.5,3 C5.91,3 3,5.91 3,9.5 C3,13.09 5.91,16 9.5,16 C11.11,16 12.59,15.41 13.73,14.43 L14,14.71 L14,15.5 L19,20.49 L20.49,19 L15.5,14 Z M9.5,14 C7.01,14 5,11.99 5,9.5 C5,7.01 7.01,5 9.5,5 C11.99,5 14,7.01 14,9.5 C14,11.99 11.99,14 9.5,14 Z"
              ></path>
            </g>
          </g>
        </g>
      </svg>
      <input
        id="layers-search"
        v-model="searchQuery"
        type="search"
        name="query"
        placeholder="Zoek laag"
      />
    </div>
    <div v-if="layers.length > 0" class="section">
      <!-- v-for="layer in layers" :key="layer.id" -->
      <ul>
        <li v-for="layer in visibleLayers" :key="layer.id">
          {{ layer.title }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "LayerList",
  data() {
    return {
      layers: [],
      searchQuery: "",
    };
  },
  computed: {
    visibleLayers() {
      if (!this.searchQuery) {
        return this.layers;
      }

      return this.layers.filter(
        (layer) =>
          layer.title.toLowerCase().search(this.searchQuery.toLowerCase()) !==
          -1
      );
    },
  },
  created() {
    this.getLayers();
  },
  methods: {
    async getLayers() {
      const result = await fetch("/atlas/api/v1/layers/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layers");
      }

      this.layers = await result.json();
    },
  },
};
</script>

<style scoped>
.buttons {
  display: flex;
}

.button {
  max-width: 300px;
}

.search-wrapper {
  width: clamp(250px, 35%, 400px);
  position: relative;
  border: 2px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
}

.search-wrapper svg {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 16px;
  margin: auto 0;
  pointer-events: none;
}

.search-wrapper input {
  width: 100%;
  height: 48px;
  padding: 0 0 0 48px;
}

/* source? */
.source {
  display: flex;
  align-items: center;
  border: 2px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
  margin-top: 16px;
}

.source a {
  padding: 12px 0 12px 20px;
  flex-grow: 1;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  text-decoration: none;
}

.source a:hover,
.source a:focus {
  text-decoration: underline;
}

.source .iconbutton {
  margin-right: 8px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
</style>
