// src/store/index.js
import { createStore } from 'vuex';
import { useCookies } from 'vue3-cookies';



// const savedState = JSON.parse(localStorage.getItem('vuex-state')) 

//gerência de estados do vuex

const store = createStore({
  state:{
    cookies: useCookies(),
    urlBackend: "http://127.0.0.1:5000",
    sharedData: null
},
  mutations: {
    setSharedData(state, data) {
      state.sharedData = data;
    },
    setUrlBackend(state, data) {
      state.urlBackend = data;
    },
    setCookie(state, data){
        state.cookies.set(data.cookieName, data.cookieValue, data.timeString);
    }
  },
  actions: {
    updateUrlBackend({ commit }, data) {
      commit('setUrlBackend', data);
    },
    updateCookie({ commit }, data) {
        commit('setCookie', data);
      }
  },
  getters: {
    getUrlCadastro: (state) => (state.urlBackend + "/cadastro"),
    getUrlLogin: (state) => (state.urlBackend + "/login"),
    getUrlChecklogin: (state) => (state.urlBackend + "/val_login"),

    
    getCookies: (state) => {state.cookies},
  }
});

store.subscribe((_mutation, state) => {
  localStorage.setItem('vuex-state', JSON.stringify(state));
});


export default store;
