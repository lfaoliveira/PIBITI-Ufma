<template>
    <nav class="flex w-full z-10 bg-[#0E0021]">
        <ul class="flex items-center gap-[2vmin] p-[1vmin] flex-1">
            <img class="rounded-lg border-2 border-initial aspect-[320/200] h-full max-h-[8vmin]" src="../../../public/logo_app2.png" />
            <li class="nav-item" v-for="(item, index) in itensEsquerdo" :key="index">
                <a :class="{ active: activeIndex === index }" @click="setActive(item)">
                    {{ item }}
                </a>
            </li>
        </ul>
        <ul ref="ladoDireito" class="flex items-center gap-[2vmin] pr-[10vmin]">
            <template v-if="this.logado">
                <li class="flex flex-col items-start bg-none">
                    <button class="bg-none cursor-pointer" @click="clickMenu">
                        <img
                            class="w-[5vmin] aspect-[219/200]"
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
                    <div class="" v-if="this.logado">
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
.nav-item a {
    cursor: pointer;
    color: white;
    font-size: clamp(13px, 1.8vmin, 20px);
    background: none;
    width: fit-content;
    font-weight: 500;
    text-decoration: none;
    transition: all 0.3s;
    padding: 1vmin;
    display: inline-block;
    text-align: center;
}

.nav-item a:not(:disabled):hover {
    background: hsla(267, 81%, 37%, 0.63);
    font-weight: 600;
    transform: scale(1.1);
}

.nav-item a:disabled {
    cursor: default;
    opacity: 0.5;
}

.nav-item a.active {
    cursor: pointer;
    font-weight: 800;
    text-decoration: underline;
}

.lista-opcoes {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    transition: transform 0.3s, opacity 0.1s;
    padding-right: 1vmin;
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

@media (max-width: 940px), (max-height: 940px) {
    .nav-item a {
        padding: 0px;
    }
}
</style>
