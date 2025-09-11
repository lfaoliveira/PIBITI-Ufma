// store/index.js
import { createStore } from 'vuex'


export class WsFactory {
    // Add resolve and reject to the constructor parameters
    constructor(dispatch, wsURL, fnHandleBackend, taskId, resolve, reject) {
        try {
            this.ws = new WebSocket(wsURL);
            console.log(`NOVO SOCKET: ${this.ws}`);

            // When the connection opens successfully, resolve the promise
            this.ws.onopen = (event) => {
                console.log('✅ Conexão WebSocket aberta.');
                this.ws.send(this.funSendWS(taskId));
                resolve(event); // Signal success!
            };

            // When an error occurs, reject the promise
            this.ws.onerror = (event) => {
                this.funError(event);
                reject(event); // Signal failure!
            };

            // These handlers remain the same
            this.ws.onmessage = (evt) => fnHandleBackend(dispatch, evt);
            this.ws.onclose = (evt) => this.funClose(evt);

        } catch (err) {
            console.log("ERRO WsHandler");
            reject(err); // Reject if the constructor itself fails
        }
    }

    // ... other methods (funSendWS, funError, funClose)
    funSendWS(taskId) {
        console.log(`ENVIANDO TASK: ${taskId}`);
        return JSON.stringify({ taskId: taskId });
    }
    funError(evt) {
        console.error(`WEBSOCKET ERROR:`, evt);
    }
    funClose(evt) {
        console.log(`WEBSOCKET FECHADO! Code: ${evt.code}, Reason: ${evt.reason}`);
    }
}



const storeWS = createStore({
  state: {
    socket: null,            // store the WebSocket instance
    socketConnected: false,
    messages: []             // example: accumulate incoming data
  },
  mutations: {
    SET_SOCKET(state, socket) {
      state.socket = socket
    },
    SET_SOCKET_CONNECTED(state, isConnected) {
      state.socketConnected = isConnected
    },
    ADD_MESSAGE(state, message) {
      state.messages.push(message)
    },
    CLEAR_SOCKET(state) {
      state.socket = null
      state.socketConnected = false
    }
  },
  actions: {
    initWebSocket({ commit, dispatch, state }) {
      if (state.socket) {
        // already connected; maybe close then reconnect?
        return
      }
      const ws = new WebSocket('ws://your.websocket.server/endpoint')

      ws.onopen = () => {
        commit('SET_SOCKET_CONNECTED', true)
        console.log('WebSocket opened')
      }

      ws.onmessage = (event) => {
        // parse data if needed
        let data
        try {
          data = JSON.parse(event.data)
        } catch (err) {
          console.error('Error parsing WS message', err)
          return
        }
        // Dispatch another action or commit mutation
        dispatch('handleIncomingMessage', data)
      }

      ws.onclose = (event) => {
        commit('SET_SOCKET_CONNECTED', false)
        console.log('WebSocket closed', event)
        // Optionally clear socket in state
        commit('CLEAR_SOCKET')
        // Maybe try reconnect, depending on application
      }

      ws.onerror = (error) => {
        console.error('WebSocket error', error)
        // you may want to do error handling, close socket, etc.
      }

      // store the socket instance
      commit('SET_SOCKET', ws)
    },

    handleIncomingMessage({ commit }, messageData) {
      // e.g. you want to mutate state, or perform other logic
      commit('ADD_MESSAGE', messageData)
      // maybe also do other dispatches etc.
    },

    sendMessage({ state }, messagePayload) {
      if (state.socket && state.socket.readyState === WebSocket.OPEN) {
        // send string or JSON as needed
        state.socket.send(JSON.stringify(messagePayload))
      } else {
        console.warn('WebSocket not open: cannot send message')
      }
    },

    closeWebSocket({ state, commit }) {
      if (state.socket) {
        state.socket.close()
        commit('CLEAR_SOCKET')
      }
    }
  }
})

export default storeWS
