import { createRouter, createWebHistory } from 'vue-router';
import Homepage from './components/inicio/HomePage.vue';
import AnaliseVideo from './components/analise/AnaliseVideo.vue';
import Salvar from './components/icons/Salvar.vue'
import Loading from "./components/analise/Loading.vue";
import CadastroVue from './components/Cadastro.vue';
import Termos from './components/inicio/Termos.vue';
import Metodo from './components/inicio/Metodo.vue';
import Duvidas from './components/inicio/Duvidas.vue';
import Equipe from './components/inicio/Equipe.vue';



const routes = [
    { name: 'home', path: '/', component: Homepage }, // Root path (Home page)
    {
        path: '/analise', // pagina de analise
        name: 'analiseVideo',
        component: AnaliseVideo,
        props: (route) => ({ idVideoAnalise: route.query.idVideoAnalise }),
    },
    {
        path: '/demo', component: AnaliseVideo,
        props: (route) => ({ idVideoAnalise: route.query.idVideoAnalise }),
    }, // pagina de exibição da demonstração
    {
        name: 'loading', path: '/loading', component: Loading,
    },
    {
        name: 'cad', path: '/cad', component: CadastroVue,
    },
    {
        name: 'termos', path:'/termos', component: Termos,
    },
    {
        path: '/metodo', name: 'PaginaMetodo', component: Metodo
    },
    {
        path: '/duvidas', name: 'PaginaDuvidas', component: Duvidas
    },
    {
        path: '/equipe', name: 'PaginaEquipe', component: Equipe
    },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;