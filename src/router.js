import { createRouter, createWebHistory } from 'vue-router';
import Homepage from './components/HomePage.vue';
import EdicaoVideo from './components/EdicaoVideo.vue';

const routes = [
  { path: '/', component: Homepage },       // Root path (Home page)
  { path: '/teste', component: EdicaoVideo }, // pagina de testes
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;