import Vuex from "vuex";

export const createStore = (initialState) => {
  return new Vuex.Store({
    state: initialState,
    mutations: {
      setPosition(state, position) {
        state.position = position;
      },
      setLayers(state, layers) {
        state.layers = layers;
      },
      addLayer(state, layer) {
        const layerSet = new Set(state.layers);
        layerSet.add(layer);

        state.layers = [...layerSet];
      },
      deleteLayer(state, layer) {
        const layerSet = new Set(state.layers);
        layerSet.delete(layer);

        state.layers = [...layerSet];
      },
      toggleLayer(state, [layerId, isVisible]) {
        state.layers = state.layers.map((layer) =>
          layer.id === layerId ? { ...layer, is_visible: isVisible } : layer
        );
      },
      setLayerOpacity(state, [layerId, opacity]) {
        state.layers = state.layers.map((layer) =>
          layer.id === layerId ? { ...layer, opacity: opacity } : layer
        );
      },
      setTool(state, tool) {
        state.tool = tool;
      },
      setSelectedArea(state, area) {
        state.selectedArea = area;
      },
      setSearchQuery(state, searchQuery) {
        state.searchQuery = searchQuery;
      },
      setAlert(state, alert) {
        state.alert = alert;
      },
      setUser(state, user) {
        state.user = user;
      },
      setDrawing(state, drawing) {
        state.drawing = drawing;
      },
    },
  });
};
