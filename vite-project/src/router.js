import { createRouter, createWebHistory } from 'vue-router';
import Homepage from './components/HomePage.vue';
import AnaliseVideo from './components/AnaliseVideo.vue';
import Demo from './components/Demo.vue'

const routes = [
  { path: '/', component: Homepage },       // Root path (Home page)
  { path: '/analise:urlVideo', component: AnaliseVideo, props: true }, // pagina de analise
  { path: '/demo', component: Demo, props: true }, // pagina de exibição da demonstração
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;