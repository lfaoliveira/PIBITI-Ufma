// src/store/index.js
import { createStore } from "vuex";
import { useCookies } from "vue3-cookies";
import { modal } from "./modules/modal";
import { websocket } from "./modules/websocket";


//gerência de estados do vuex

const MAX_LINKS = 3;

const store = createStore({
    modules: {
        modal,
        websocket,
    },
    state: {
        urlBackend: import.meta.env.VITE_BACKEND_URL + "/api",
        urlWebSocket: import.meta.env.VITE_BACKEND_WS,
        sharedData: null,
        logado: false,
        formDiag: null,
        linksAnalise: {}, //array funciona como fila
        wsDict: {},
    },
    mutations: {
        setSharedData(state, data) {
            state.sharedData = data;
        },
        setUrlBackend(state, data) {
            state.urlBackend = data;
        },
        setCookie(state, data) {
            state.cookies.set(data.cookieName, data.cookieValue, data.timeString);
        },
        setLogado(state, data) {
            state.logado = data;
        },
        setFormDiag(state, data) {
            state.formDiag = data;
        },
        addLink(state, data) {
            const link = data["link"];
            if (state.linksAnalise.length >= MAX_LINKS) {
                state.linksAnalise.shift();
            }
            state.linksAnalise.push(link);
        },
        removeLink(state) {
            if (state.linksAnalise.length > 0) {
                const removido = state.linksAnalise.shift();
                console.log(`LINK REMOVIDO: ${removido}`);
            } else {
                console.warn("ARRAY DE LINKS VAZIO!\n");
            }
        },

    },
    actions: {
        updateUrlBackend({ commit }, data) {
            commit("setUrlBackend", data);
        },
        updateCookie({ commit }, data) {
            commit("setCookie", data);
        },

        updateFormDiag({ commit }, data) {
            commit("setFormDiag", data);
        },
        addLinkAnalise({ commit }, data) {
            commit("addLink", data);
        },
        removeLinkAnalise({ commit }) {
            commit("removeLink");
        },
        handleWebSocket({ state, dispatch, commit }, { wsURL, taskId }) {
            dispatch('websocket/initWebSocket', {
                uuid: taskId, url: wsURL
            }, { root: true })
        },
    },
    getters: {
        //websocket
        getWSBackend: (state) => state.urlWebSocket,
        getAnaliseWS: (state) => state.urlBackend + "/analise-ws",
        getWSUuid: (state) => (taskId) => state.websocket.sockets[taskId],
        //urls
        getUrlBackend: (state) => state.urlBackend,
        getUrlCadastro: (state) => state.urlBackend + "/auth?tipo=cadastro",
        getUrlLogin: (state) => state.urlBackend + "/auth?tipo=login",
        getUrlChecklogin: (state) => state.urlBackend + "/val_login",
        getUrlEsqueciSenha: (state) => state.urlBackend + "/esqueci_senha",
        getUrlMudarSenha: (state) => state.urlBackend + "/mudar_senha",
        getUrlDeslogar: (state) => state.urlBackend + "/logout",
        getDiag: (state) => state.urlBackend + "/envia_diag",
        getPerfil: (state) => state.urlBackend + "/pega_perfil",
        getAnalise: (state) => state.urlBackend + "/analise",
        getTaskStatus: (state) => state.urlBackend + "/status/",
        //estados auxiliares e objetos
        getLogado: (state) => state.logado,
        getFormDiag: (state) => state.formDiag,
        //dict de links
        getLink: (state, taskId) => state.linksAnalise[taskId],
    },
});

store.subscribe((_mutation, state) => {
    localStorage.setItem("vuex-state", JSON.stringify(state));
});

export default store;
