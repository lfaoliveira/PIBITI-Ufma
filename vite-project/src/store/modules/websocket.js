// store/modules/websocket.js

import router from "../../router"


export const websocket = {
    namespaced: true,
    
    state: () => ({
        sockets: {},            // dictionary to store multiple WebSocket instances
        socketStatuses: {},     // track connection status for each socket
    }),
    mutations: {
        SET_SOCKET(state, { uuid, socket }) {
            state.sockets = { ...state.sockets, [uuid]: socket }
        },
        SET_SOCKET_CONNECTED(state, { uuid, isConnected }) {
            state.socketStatuses = { ...state.socketStatuses, [uuid]: isConnected }
        },

        CLEAR_SOCKET(state, uuid) {
            delete state.sockets[uuid]
            delete state.socketStatuses[uuid]
        },
    },
    actions: {
        initWebSocket({ commit, dispatch, state }, { uuid, url }) {
            if (state.sockets[uuid]) {
                return
            }
            const ws = new WebSocket(url)
            commit('SET_SOCKET', { uuid, socket: ws })

            ws.onopen = () => {
                commit('SET_SOCKET_CONNECTED', { uuid, isConnected: true })
                console.log(`WebSocket ${url}/${uuid} opened`)

                console.log(`ENVIANDO TASK: ${uuid}`)
                const payload = { taskId: uuid }
                dispatch('sendMessage', { uuid: uuid, messagePayload: payload })
            }

            ws.onmessage = (event) => {
                let data
                try {
                    data = JSON.parse(event.data)
                } catch (err) {
                    console.error(`Error parsing WS message for ${uuid}`, err)
                    return
                }
                dispatch('handleIncomingMessage', { uuid, data })
            }

            ws.onclose = (event) => {
                commit('SET_SOCKET_CONNECTED', { uuid, isConnected: false })
                commit('CLEAR_SOCKET', uuid)
                dispatch('closeWebSocket', { uuid})
                console.log(`WEBSOCKET FECHADO! Code: ${event.code}, Reason: ${event.reason}`);
            }

            ws.onerror = (error) => {
                console.error(`WebSocket ${String(uuid).substring(0, 5)} error`, error)
            }

        },

        handleIncomingMessage({ state, commit, dispatch}, { uuid, data }) {
            console.log(`DATA: ${JSON.stringify(data)}`)

            if (data && data?.task_id) {
                const analysisLink = router.resolve({
                    name: 'analiseVideo',
                    query: { uuid: data.task_id }
                }).fullPath
                console.log(`LINK GERADO: ${analysisLink}`)

                dispatch('modal/openModal', {
                    name: 'popup',
                    content: {
                        component: 'Popup',
                        props: { link: analysisLink }
                    }
                }, { root: true })
            }
            else{
                console.log("DEU MERDA")
            }
        },

        sendMessage({ state }, { uuid, messagePayload }) {
            const socket = state.sockets[uuid]
            console.log(`PAYLOAD: ${JSON.stringify(messagePayload)}`)
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify(messagePayload))
            } else {
                console.warn(`WebSocket ${uuid} not open: cannot send message`)
            }
        },

        closeWebSocket({ state, commit }, uuid) {
            const socket = state.sockets[uuid]
            
            if (socket) {
                socket.close()
                commit('CLEAR_SOCKET', uuid)
            }
        }
    }
}

export default websocket
