// src/store/index.js
import { createStore } from 'vuex';
const savedState = JSON.parse(localStorage.getItem('vuex-state')) || {};


//gerencia de estados do vuex

const store = createStore({
  state: {
      // Centralized state for video files
      videoFile: savedState.videoFile || null,
  },
  mutations: {
    setSharedData(state, data) {
      state.sharedData = data;
    },
    setVideoFile(state, file){
      state.videoFile = file;
    },
  },
  actions: {
    updateVideoFile({ commit }, data) {
      commit('setvideoFile', data);
    }
  },
  getters: {
    getVideoFile: (state) => state.videoFile,
    getSharedData: (state) => state.sharedData
  }
});

store.subscribe((mutation, state) => {
  localStorage.setItem('vuex-state', JSON.stringify(state));
});


export default store;
