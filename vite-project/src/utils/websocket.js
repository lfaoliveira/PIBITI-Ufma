// Classe handler de WebSocket que serve para manter estado do webSocket vivo independente de componente no Vue
export class WsHandler {
    constructor(dispatch, wsURL, fnHandleBackend) {
        this.dispatch = dispatch
        this.fnHandleBackend = fnHandleBackend
        const ws = new WebSocket(wsURL);
        console.log(`NOVO SOCKET: ${ws.readyState}`);

        ws.onopen = () => ws.send(funSendWS(taskId));
        ws.onmessage = (evt) => this.fnHandleBackend(this.dispatch, evt);
        ws.onerror = (evt) => funError(evt);
        ws.onclose = (evt) => funClose(evt);
    }
    funSendWS(taskId) {
        console.log(`ENVIANDO TASK: ${taskId}`)
        return JSON.stringify({ taskId: taskId });
    }
    funError(evt) {
        console.error(`WEBSOCKET: ${evt.data}`);
    }
    funClose(evt) {
        console.log(`WEBSOCKET FECHADO!\n`);
    }
}
