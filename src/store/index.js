// src/store/index.js
import { createStore } from 'vuex';


//gerencia de estados do vuex

export default createStore({
  state: {
    sharedData: null
  },
  mutations: {
    setSharedData(state, data) {
      state.sharedData = data;
    }
  },
  actions: {
    updateSharedData({ commit }, data) {
      commit('setSharedData', data);
    }
  },
  getters: {
    getSharedData: (state) => state.sharedData
  }
});