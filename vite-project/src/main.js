import './assets/main.css'

import { createApp } from 'vue'
import { createStore } from 'vuex';
import router from './router.js'; // Import the router config
import store from './store/index'; // Import your Vuex store



import App from './App.vue'

const app = createApp(App);
app.use(router).use(store); // Use the router in the app
app.mount('#app');

