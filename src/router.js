import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import EdicaoVideo from './components/EdicaoVideo.vue';

const routes = [
  { path: '/', component: App },       // Root path (Home page)
  { path: '/teste', component: EdicaoVideo }, // pagina de testes
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;