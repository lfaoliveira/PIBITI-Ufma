import { createRouter, createWebHistory } from 'vue-router';
import Homepage from './components/HomePage.vue';
import AnaliseVideo from './components/AnaliseVideo.vue';

const routes = [
  { path: '/', component: Homepage },       // Root path (Home page)
  { path: '/teste', component: AnaliseVideo }, // pagina de testes
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;