import { createRouter, createWebHistory } from 'vue-router';
import Homepage from './components/inicio/HomePage.vue';
import AnaliseVideo from './components/analise/AnaliseVideo.vue';
import Loading from "./components/analise/Loading.vue";
import Termos from './components/inicio/Termos.vue';
import Metodo from './components/inicio/Metodo.vue';
import Duvidas from './components/inicio/Duvidas.vue';
import Equipe from './components/inicio/Equipe.vue';
import Acesso from './components/Acesso.vue';
import FichaDiag from './components/analise/FichaDiag.vue';
import Perfil from './components/nav/Perfil.vue';
import EsqueciSenha from './components/auxiliares/EsqueciSenha.vue';
import MudarSenha from './components/auxiliares/MudarSenha.vue';



const routes = [
    { name: 'home', path: '/', component: Homepage }, // Root path (Home page)
    {
        path: '/analise', // pagina de analise
        name: 'analiseVideo',
        component: AnaliseVideo,
        props: (route) => ({ id_diag: route.query.id_diag, responseStringJson: route.query.responseStringJson }),
    },
    {
        name: 'PaginaCarregando', path: '/loading', component: Loading,
    },
    {
        name: 'PaginaAcesso', path: '/acesso', component: Acesso,
    },
    {
        name: 'PaginaTermos', path:'/termos', component: Termos,
    },
    {
        name: 'PaginaMetodo', path: '/metodo' , component: Metodo
    },
    {
        name: 'PaginaDuvidas', path: '/duvidas',  component: Duvidas
    },
    {
        name: 'PaginaEquipe', path: '/equipe',  component: Equipe
    },
    {
        name: 'FichaDiag', path: '/ficha',  component: FichaDiag
    },
    {
        name: 'Perfil', path: '/perfil',  component: Perfil
    },
    {
        name: 'EsqueciSenha', path: '/esqueceuSenha',  component: EsqueciSenha
    },
    {
        name: 'MudarSenha', path: '/mudarSenha',  component: MudarSenha
    },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;