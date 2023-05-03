<template>
  <div class="content">
    <div class="header">
      <button
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton __normal __outline"
        type="button"
        aria-label="Ga terug"
        content="Terug"
        @click="() => $emit('show-form')"
      >
        <svg
          width="24px"
          height="24px"
          viewBox="0 0 24 24"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
        >
          <title>arrow_back_black_24dp</title>
          <g
            id="Admin"
            stroke="none"
            stroke-width="1"
            fill="none"
            fill-rule="evenodd"
          >
            <g
              id="Kaart---Zoekbalk"
              transform="translate(-24.000000, -24.000000)"
            >
              <g
                id="arrow_back_black_24dp"
                transform="translate(16.000000, 16.000000)"
              >
                <g transform="translate(8.000000, 8.000000)">
                  <polygon id="Path" points="0 0 24 0 24 24 0 24"></polygon>
                  <polygon
                    id="Path"
                    fill="#000000"
                    fill-rule="nonzero"
                    points="20 11 7.83 11 13.42 5.41 12 4 4 12 12 20 13.41 18.59 7.83 13 20 13"
                  ></polygon>
                </g>
              </g>
            </g>
          </g>
        </svg>
      </button>
      <h1>Filters</h1>
      <div class="header-spacer" />
    </div>
    <div class="filters">
      <p v-if="!layer">
        Kies eerst een laag voordat je de filters instelt.
      </p>

      <div v-for="facet in availableFacets" :key="facet">
        <input
          :id="`facet-${facet}`"
          v-model="data.settings.facets"
          type="checkbox"
          :name="`facet-${facet}`"
          :value="facet"
        />
        <label :for="`facet-${facet}`">{{ facet }}</label>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FiltersAdmin",
  props: {
    initialData: Object,
    layer: Object,
    user: Object,
  },
  data() {
    return {
      data: this.initialData,
      availableFacets: [],
    };
  },
  computed: {},
  mounted() {
    if (this.layer) {
      this.fetchFeatureType();
    }
  },
  methods: {
    async fetchFeatureType() {
      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "1.0.0"],
        ["request", "DescribeFeatureType"],
        ["typename", this.layer.name],
        ["outputFormat", "application/json"],
      ]);

      try {
        const url = new URL(this.layer.url);
        url.search = params.toString();

        const result = await fetch(url.toString(), this.getFetchParameters());

        const data = await result.json();
        const featureType = data.featureTypes[0];

        this.availableFacets = featureType.properties
          .filter((ft) => ft.type == "xsd:string")
          .map((ft) => ft.name);
      } catch (e) {
        console.error(e);
      }
    },
    getFetchParameters() {
      if (
        this.layer.source &&
        this.layer.source.authenticate &&
        this.user &&
        this.user.token
      ) {
        return {
          headers: { Authorization: `Bearer ${this.user.token}` },
        };
      }

      return {};
    },
  },
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
}

.header-spacer {
  width: 40px;
}

.filters {
  margin-top: 24px;
}
</style>
