import './assets/main.css'

import { createApp } from 'vue'
import { createStore } from 'vuex';
import router from './router.js'; // Import the router config
import store from './store/index'; // Import your Vuex store
import 'video.js/dist/video-js.css';



import App from './App.vue'

const app = createApp(App);

// Global navigation guard
router.beforeEach(async (to, from, next) => {
  try {
    const response = await axios.get(store.getters.getUrlChecklogin, {
      withCredentials: true,
    });
    if (response.status === 200) {
      store.commit('setLogado', true);
      console.log("200")
    } else {
      store.commit('setLogado', false);
    }
  } catch (error) {
    store.commit('setLogado', false);
  }
  next();
});


app.use(router)
app.use(store)
// Use  router, vue-store and vue-cookies in the app
app.mount('#app');

