// src/store/index.js
import { createStore } from 'vuex';



// const savedState = JSON.parse(localStorage.getItem('vuex-state')) 

//gerencia de estados do vuex

const store = createStore({
  state:{
    urlBackend: "http://127.0.0.1:5000",
    sharedData: null
},
  mutations: {
    setSharedData(state, data) {
      state.sharedData = data;
    },
    setUrlBackend(state, data) {
      state.urlBackend = data;
    }
  },
  actions: {
    updateUrlBackend({ commit }, data) {
      commit('setUrlBackend', data);
    }
  },
  getters: {
    getUrlBackend: (state) => state.urlBackend,
    getUrlCadastro: (state) => (state.urlBackend + "/cadastro"),
    getSharedData: (state) => state.sharedData
  }
});

store.subscribe((_mutation, state) => {
  localStorage.setItem('vuex-state', JSON.stringify(state));
});


export default store;
