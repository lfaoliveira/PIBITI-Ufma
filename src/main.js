import './assets/main.css'

import { createApp } from 'vue'
import router from './router.js'; // Import the router config

import App from './App.vue'

const app = createApp(App)
app.use(router); // Use the router in the app
app.mount('#app')

