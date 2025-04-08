// src/store/index.js
import { createStore } from 'vuex';
import { useCookies } from 'vue3-cookies';



// const savedState = JSON.parse(localStorage.getItem('vuex-state')) 

//gerência de estados do vuex

const store = createStore({
    state:{
        urlBackend: "http://127.0.0.1:5000",
        sharedData: null,
        logado: false,
        formDiag: null,
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
        },
        setLogado(state, data){
                state.logado = data;
        },
        setFormDiag(state, data) {
            state.formDiag = data;
        }
    },
    actions: {
        updateUrlBackend({ commit }, data) {
            commit('setUrlBackend', data);
        },
        updateCookie({ commit }, data) {
                commit('setCookie', data);
        },
        updateLogado({ commit }, data) {
                commit('setLoado', data);
        },
        updateFormDiag({ commit }, data) {
            commit('setformDiag', data);
        }
    },
    getters: {
        getUrlCadastro: (state) => (state.urlBackend + "/auth?tipo=cadastro"),
        getUrlLogin: (state) => (state.urlBackend + "/auth?tipo=login"),
        getUrlChecklogin: (state) => (state.urlBackend + "/val_login"),
        getUrlEsqueciSenha: (state) => (state.urlBackend + "/esqueci_senha"),
        getDiag: (state) => (state.urlBackend + "/envia_diag"),
        getPerfil:  (state) => (state.urlBackend + "/pega_perfil"),
        getAnalise: (state) => (state.urlBackend + "/analise"),
        getLogado: (state) => (state.logado),
        getFormDiag: (state) => (state.formDiag),
    }
});

store.subscribe((_mutation, state) => {
  localStorage.setItem('vuex-state', JSON.stringify(state));
});


export default store;
