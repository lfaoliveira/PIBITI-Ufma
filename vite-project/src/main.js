import './assets/main.css'

import { createApp } from 'vue'
import { createStore } from 'vuex';
import router from './router.js'; // Import the router config
import store from './store/index'; // Import your Vuex store
import 'video.js/dist/video-js.css';
import axios from 'axios';

import './style.css'

import Popup from "./components/layout/Popup.vue";
import TesteOverlay from './components/layout/TesteOverlay.vue';

axios.defaults.withCredentials = true;


import App from './App.vue'

const app = createApp(App);


/*@@@@@@@@@@@@@@@@@@    NOME REGISTRADO DEVE SER DIFERENTE DO NOME REAL DO COMPONETE    @@@@@@@@@@@@@@@@@@ */
app.component("Popup", Popup); // <-- make "Popup" resolvable globally
app.component("Teste", TesteOverlay); 


router.beforeEach(async (_to, _from, next) => {
  try {
    const response = await axios.get(store.getters.getUrlChecklogin, {
      withCredentials: true,
    });
    
    if (response.status === 200) {
        store.commit('setLogado', true);
        console.log("LOGADO: ", true)
    } else {
        console.log("LOGADO: ", false)
        store.commit('setLogado', false);
    }
} catch (error) {
    console.log("LOGADO: ", false)
    store.commit('setLogado', false);
  }
  next();
});


app.use(router)
app.use(store)
// Use  router, vue-store and vue-cookies in the app
app.mount('#app');

