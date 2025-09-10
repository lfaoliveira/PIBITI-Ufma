// src/store/index.js
import { createStore } from "vuex";
import { useCookies } from "vue3-cookies";
import { modal } from "./modules/modal";

import { WsHandler } from "../utils/websocket";

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
        wsDict: [],
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
        handleWebSocket({ dispatch }, { wsURL, taskId }) {
            try {
                if (!taskId) {
                    throw new Error("taskId é obrigatório!");
                }
                if (popupMessageObject instanceof Object === false) {
                    throw new Error("MENSAGEM DEVE TER CAMPOS VALIDOS!");
                }
                // 2. Define a função de callback que será chamada ao receber uma mensagem do backend
                const handleBackendMessage = (dispatch, event) => {
                    // A mensagem do WebSocket geralmente é um JSON em formato de string.
                    const data = JSON.parse(event.data);

                    // Verifica se a mensagem contém os dados que você precisa, como o taskId
                    if (data && data?.task_id) {
                        // 3. Cria o link do frontend com base no uuid recebido do backend
                        const analysisLink = `/analise?uuid=${data.task_id}`;
                        console.log(`LINK GERADO: ${analysisLink}`);

                        // 4. Dispara a ação para abrir o modal, passando o link como conteúdo
                        dispatch(
                            "modal/openModal",
                            {
                                name: "popup", 
                                content: { link: analysisLink },
                            },
                            { root: true } // { root: true } é necessário se 'modal' for um módulo raiz e 'analise' um sub-módulo
                        );
                    }
                };
                const wsHand = new WsHandler(dispatch, wsURL, handleBackendMessage);
                wsDict[taskId] = wsHand
                return true
            } catch (err) {
                console.error("❌ Erro ao processar mensagem WS:", err);
                throw err
            }
        },
    },
    getters: {
        //websocket
        getWSBackend: (state) => state.urlWebSocket,
        getAnaliseWS: (state) => state.urlBackend + "/analise-ws",
        getWSUuid: (state, taskId) => state.wsDict[taskId],
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
