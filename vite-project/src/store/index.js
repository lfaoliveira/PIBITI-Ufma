// src/store/index.js
import { createStore } from "vuex";
import { useCookies } from "vue3-cookies";
import { modal } from "./modules/modal";

import { WsHandler } from "./websocket";

//gerência de estados do vuex

const MAX_LINKS = 3;

const store = createStore({
    modules: {
        modal,
    },
    state: {
        urlBackend: import.meta.env.VITE_BACKEND_URL + "/api",
        urlWebSocket: import.meta.env.VITE_BACKEND_WS,
        sharedData: null,
        logado: false,
        formDiag: null,
        linksAnalise: [], //array funciona como fila
        listaWebSockets: [],
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
        addWS(state, ws) {
            if (state.listaWebSockets.length >= MAX_LINKS) {
                state.listaWebSockets.shift();
            }
            state.listaWebSockets.push(ws);
            return state.listaWebSockets.length - 1; //retorna indice do novo WS
        },
        removeWS(state, ws) {
            const index = state.listaWebSockets.indexOf(ws);
            if (index > -1) {
                array.splice(index, 1);
            }
            return index;
        },
    },
    actions: {
        updateUrlBackend({ commit }, data) {
            commit("setUrlBackend", data);
        },
        updateCookie({ commit }, data) {
            commit("setCookie", data);
        },
        updateLogado({ commit }, data) {
            commit("setLoado", data);
        },
        updateFormDiag({ commit }, data) {
            commit("setformDiag", data);
        },
        addLinkAnalise({ commit }, data) {
            commit("addLink", data);
        },
        removeLinkAnalise({ commit }) {
            commit("removeLink");
        },
        handleWebSocket({ dispatch }, rawMessage, popupMessageObject) {
            try {
                const data = JSON.parse(rawMessage);
                if (!popupMessageObject instanceof Object) {
                    if (
                        !popupMessageObject?.titulo ||
                        !popupMessageObject?.subtexto ||
                        !popupMessageObject?.srcImg ||
                        !popupMessageObject?.link
                    ) {
                        throw new Error("MENSAGEM DEVE TER CAMPOS VALIDOS!");
                    }
                }

                // Decide qual modal abrir (exemplo: se vier "type", usa ele)
                const modalName = data?.type || "popup";
                const component = {};

                dispatch("openModal", {
                    name: modalName,
                    content: data.message || "📩 Nova mensagem recebida!",
                });
            } catch (err) {
                console.error("❌ Erro ao processar mensagem WS:", err);
            }
        },
    },
    getters: {
        //websocket
        getWSBackend: (state) => state.urlWebSocket,
        getAnaliseWS: (state) => state.urlBackend + "/analise-ws",
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
        //fila de links
        getLinks: (state) => state.linksAnalise,
    },
});

store.subscribe((_mutation, state) => {
    localStorage.setItem("vuex-state", JSON.stringify(state));
});

export default store;
