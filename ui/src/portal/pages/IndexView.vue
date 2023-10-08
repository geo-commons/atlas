<template>
  <div class="container">
    <div class="section">
      <h2>Selecties</h2>
      <div class="grid">
        <a href="/atlas/">
          <div class="item">Maak eigen selectie</div>
        </a>
        <a v-for="selection in selections" :key="selection.id" :href="getSelectionURL(selection)">
          <div class="item">
            {{ selection.title }}
          </div>
        </a>
      </div>
    </div>
    <div v-if="maps.length > 0" class="section">
      <h2>Kaarten</h2>
      <div class="grid">
        <a v-for="map in maps" :key="map.id" :href="`/atlas/maps/${map.slug}`">
          <div class="item">
            {{ map.title }}
          </div>
        </a>
      </div>
    </div>
    <div v-if="tables.length > 0" class="section">
      <h2>Tabellen</h2>
      <div class="grid">
        <a v-for="table in tables" :key="table.id" :href="`/tables/#/${table.slug}`">
          <div class="item">
            {{ table.title }}
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "IndexView",
  components: {},
  computed: {
    ...mapState({
      config: (state) => state.config,
      selections: (state) => state.selections,
      tables: (state) => state.tables,
      maps: (state) => state.maps,
    }),
  },
  methods: {
    getSelectionURL(selection) {
      const position = this.config.position;
      return `/atlas/@${encodeURIComponent(position.center.x.toFixed(2))},${encodeURIComponent(position.center.y.toFixed(2))},${encodeURIComponent(
        position.zoom
      )}z/layers=${selection.layers.map((l) => encodeURIComponent(l.id)).join(",")}/base=`;
    },
  },
};
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  row-gap: 14px;
  column-gap: 14px;
}

.grid a {
  text-decoration: none;
}

.item {
  padding: 20px;
  border: 2px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
  font-weight: var(--font-weight-bold);
  color: black;
}
</style>
