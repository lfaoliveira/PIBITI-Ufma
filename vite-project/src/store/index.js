// src/store/index.js
import { createStore } from 'vuex';


//gerencia de estados do vuex

export default createStore({
  state: {
      videoURL: null // Centralized state for video URLs
  },
  mutations: {
    setSharedData(state, data) {
      state.sharedData = data;
    },
    setVideoURL(state, url) {
      state.videoURL = url;
    }
  },
  actions: {
    updateVideoURL({ commit }, url) {
      commit('setVideoURL', url);
    },
    updateSharedData({ commit }, data) {
      commit('setSharedData', data);
    }
  },
  getters: {
    /* getVideoURL(state) {
      return state.videoURL;
    }, */
    getVideoURL: (state) => state.videoURL,
    getSharedData: (state) => state.sharedData
  }
});