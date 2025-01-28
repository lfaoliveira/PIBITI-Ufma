import { createRouter, createWebHistory } from 'vue-router';
import Homepage from './components/HomePage.vue';
import AnaliseVideo from './components/AnaliseVideo.vue';
import Salvar from './components/icons/Salvar.vue'
import Loading from "./components/Loading.vue";

const routes = [
    { name: 'home', path: '/', component: Homepage }, // Root path (Home page)
    {
        path: '/analise', // pagina de analise
        name: 'analiseVideo',
        component: AnaliseVideo,
        props: (route) => ({ idVideoAnalise: route.query.idVideoAnalise }),
    },
    { path: '/salvar', name: 'salvar', component: Salvar },
    {
        path: '/demo', component: AnaliseVideo,
        props: (route) => ({ idVideoAnalise: route.query.idVideoAnalise }),
    }, // pagina de exibição da demonstração
    {
        name: 'loading', path: '/loading', component: Loading,
    },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;