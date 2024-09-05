import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import Teste from './components/Teste.vue';

const routes = [
  { path: '/', component: App },       // Root path (Home page)
  { path: '/teste', component: Teste }, // funciona
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;