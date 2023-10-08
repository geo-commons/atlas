import Vuex from "vuex";

export const createStore = (initialState) => {
  return new Vuex.Store({
    state: initialState,
  });
};
