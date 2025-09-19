<template>
    <nav class="nav-bar">
        <ul class="header lado-esquerdo">
            <img class="img-logo" src="../../../public/logo_app2.png" />
            <!-- Para cada item dentro de menuItens, so ativa quem tiver indice igual a activeIndex -->
            <li class="nav-item" v-for="(item, index) in itensEsquerdo" :key="index">
                <a :class="{ active: activeIndex === index }" @click="setActive(item)">
                    {{ item }}
                </a>
            </li>
        </ul>
        <ul ref="ladoDireito" class="lado-direito">
            <template v-if="this.logado">
                <li class="div-hamburguer">
                    <button class="button-hamburguer" @click="clickMenu">
                        <img
                            class="img-hamburguer"
                            :src="
                                this.isOpen
                                    ? 'src/assets/close.png'
                                    : 'src/assets/menu-sanduiche.png'
                            "
                        />
                    </button>
                </li>
            </template>
            <transition name="slide">
                <li
                    ref="opcoes"
                    class="lista-opcoes"
                    v-show="this.isOpen || this.logado == false"
                >
                    <div v-if="this.logado == false" class="nav-item">
                        <a
                            class="acesso"
                            :class="{ active: activeIndex === itensEsquerdo.length }"
                            @click="setActive('Acessar Sistema')"
                            >Acessar Sistema</a
                        >
                    </div>
                    <div class="nav-item" v-if="this.logado">
                        <a
                            :class="{ active: activeIndex === 6 }"
                            @click="setActive('Perfil')"
                            >Perfil</a
                        >
                    </div>

                    <div class="nav-item" v-if="this.logado">
                        <Sair></Sair>
                    </div>

                    <div class="nav-item" v-if="this.logado">
                        <Salvar :modo="this.modoSalvar" :urlPDF="urlPDF"></Salvar>
                    </div>
                </li>
            </transition>
        </ul>
    </nav>
</template>

<script>
import Salvar from "../icons/Salvar.vue";
import Voltar from "../icons/Voltar.vue";
import Sair from "../icons/Sair.vue";

import axios from "axios";

export default {
    name: "HeaderSistema",
    components: {
        Salvar,
        Voltar,
        Sair,
    },
    data() {
        return {
            itensEsquerdo: [
                "Início",
                "Método",
                "Sobre",
                "Como Funciona?",
                "Fazer Análise",
            ],
            emAnalise: false,
            logado: false,
            telaPequena: false,
            isOpen: false,
        };
    },
    props: {
        activeIndex: 0,
        urlPDF: null,
    },
    created() {
        this.$store.subscribe((mutation, state) => {
            if (mutation.type === "setLogado") {
                this.logado = state.logado;
            }
        });
    },
    mounted() {
        //executar checagem se esta logado

        this.emAnalise = this.$route.path === "/analise";
        this.logado = this.$store.getters.getLogado;
        console.log("ANALISe");
    },
    methods: {
        setActive(nome) {
            this.$emit("update:activeIndex", nome);

            const mapa = {
                Início: "/",
                Método: "/metodo",
                Sobre: "/equipe",
                "Como Funciona?": "/duvidas",
                "Fazer Análise": "/ficha",
                "Acessar Sistema": "/acesso",
                Perfil: "/perfil",
            };
            const rota = mapa[nome];
            this.$router.push(rota);
        },

        async fnBaixar() {
            // lógica para salvar resultado
            console.log("Baixando...");
            if (this.urlPDF != null) {
                const res = await axios.get(this.urlPDF);
                console.log("HEADER: ");
            } else {
                alert("Nao foi possível encontrar relatório!");
            }
        },
        clickMenu() {
            if (this.isOpen) {
                this.isOpen = false;
            } else {
                this.isOpen = true;
                this.$refs.ladoDireito.style.alignItems = "flex-end";
            }
        },
    },
    computed: {
        modoSalvar() {
            if (this.emAnalise == true) {
                return "on";
            } else return "off";
        },
    },
};
</script>

<style lang="scss" scoped>
.nav-bar {
    display: flex;
    width: clamp(100%, 100%, 100%);
    z-index: 1;
    background: #0e0021;
    .img-logo {
        border-style:initial;
        border-radius: 0.5rem;
        border-width: 2px;
        aspect-ratio: 320/200;
        height: 100%;
    }
    &:has(.div-hamburguer) {
        max-height: 8vmin;
        padding-right: 10vmin;

        .button-hamburguer {
            background: none;
            cursor: pointer;
        }

        .div-hamburguer {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            background: none;
            .img-hamburguer {
                width: 5vmin;
                aspect-ratio: 219/200;
            }
        }
    }
}

.slide-enter-active,
.slide-leave-active {
    transition: transform 0.3s ease-out 0s;
}

.slide-enter-from {
    transform: translateX(-100%);
}
.slide-enter-to {
    transform: translateX(0);
}
.slide-leave-from {
    transform: translateX(0);
}
.slide-leave-to {
    transform: translateX(-200%);
}

/* .slide-enter-from,
  .slide-leave-to {
  transition: all 0.2s ease-in-out 0s;
} */

.lista-opcoes {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    transition: transform 0.3s, opacity 0.1s;
    padding-right: 1vmin;
}

.header {
    list-style: none;
    display: flex;
    height: $alt-headers;
    padding: clamp(0.2%, 10px, 1%) 0px;
    margin: 0px 2% 0% 1%;
    align-items: center;
    gap: 3vmin;
    flex: 1 0 0;
    align-self: stretch;
}

.lado-direito {
    list-style: none;
    margin: 0vmin 0vmin 0vmin 1vmin;
    background: #0e0021;
    height: max-content;
    padding: 0px;
    //   width: clamp(200px, 36vmin, 320px);
    display: flex;
    align-items: flex-end;
    flex-direction: column;
    width: fit-content;
    gap: 3vmin;
}

.nav-item a {
    @include botao-header($escala: 1.1);
}

.nav-item a.active {
    cursor: pointer;
    font-weight: 800;
    text-decoration: underline;
}
@media (max-width: 940px), (max-height: 940px) {
    .nav-item a {
        padding: 0px;
    }
    .lado-direito:has(.acesso) {
        height: clamp(5vmin, 70px, 10vmin);
        padding: clamp(0.2%, 10px, 1%) 0px;

        .lista-opcoes {
            height: 100%;
            align-items: center;
            justify-content: center;
        }
        .acesso {
            margin-right: clamp(2vmin, 20px, 2%);
            padding: 0px;
        }
    }
}
</style>
