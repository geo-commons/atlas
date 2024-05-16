import { defineStore } from "pinia";

export const useGlobalStore = defineStore({
  id: "global",
  state: () => ({
    position: null,
    layers: [],
    tool: null,
    selectedArea: null,
    searchQuery: null,
    alert: null,
    user: null,
    drawing: null,
    isEmbed: null,
    config: null,
    initiallyShowLayerList: null,
    selections: null,
    tables: null,
    maps: null,
    map: null,
  }),
  getters: {
    // getters
  },
  actions: {
    setInitialState(initialState) {
      Object.assign(this, initialState);
    },
    setPosition(position) {
      this.position = position;
    },
    setLayers(layers) {
      this.layers = layers;
    },
    addLayer(layer) {
      if (!this.layers.includes(layer)) {
        this.layers.push(layer);
      }
    },
    deleteLayer(layer) {
      const index = this.layers.indexOf(layer);
      if (index !== -1) {
        this.layers.splice(index, 1);
      }
    },
    toggleLayer([layerId, isVisible]) {
      this.layers = this.layers.map((layer) => (layer.id === layerId ? { ...layer, is_visible: isVisible } : layer));
    },
    setLayerOpacity([layerId, opacity]) {
      this.layers = this.layers.map((layer) => (layer.id === layerId ? { ...layer, opacity: opacity } : layer));
    },
    setTool(tool) {
      this.tool = tool;
    },
    setSelectedArea(area) {
      this.selectedArea = area;
    },
    setSearchQuery(searchQuery) {
      this.searchQuery = searchQuery;
    },
    setAlert(alert) {
      this.alert = alert;
    },
    setUser(user) {
      this.user = user;
    },
    setDrawing(drawing) {
      this.drawing = drawing;
    },
  },
});
