<template>
    <nav class="flex w-full z-40 bg-[#0E0021]">
        <ul class="flex items-center gap-[2vmin] p-[1vmin] flex-1">
            <img
                class="rounded-lg border-2 border-initial aspect-[320/200] h-full max-h-[8vmin]"
                src="../../../public/logo_app2.png"
            />
            <li v-for="(item, index) in itensEsquerdo" :key="index">
                <a
                    class="cursor-pointer text-white text-xs sm:text-sm bg-transparent w-fit font-medium no-underline transition-all duration-300 p-1 inline-block text-center hover:bg-[hsla(267,81%,37%,0.63)] hover:font-semibold hover:scale-110 max-[940px]:p-0"
                    :class="{ 'font-extrabold underline': activeIndex === index }"
                    @click="setActive(item)"
                >
                    {{ item }}
                </a>
            </li>
        </ul>
        <ul ref="ladoDireito" class="relative flex items-center gap-[2vmin] sm:pr-[1rem]">
            <li class="sm:hidden">
                <button class="bg-transparent cursor-pointer p-1" @click="clickMenu">
                    <img
                        class="w-[5vmin] aspect-[219/200]"
                        :src="
                            isOpen
                                ? 'src/assets/close.png'
                                : 'src/assets/menu-sanduiche.png'
                        "
                    />
                </button>
            </li>
            <template v-if="this.logado">
                <li class="hidden sm:block">
                    <button class="bg-transparent cursor-pointer p-1" @click="clickMenu">
                        <img
                            class="w-[5vmin] aspect-[219/200]"
                            :src="
                                isOpen
                                    ? 'src/assets/close.png'
                                    : 'src/assets/menu-sanduiche.png'
                            "
                        />
                    </button>
                </li>
            </template>
            <transition name="slide">
                <div
                    v-show="this.isOpen"
                    class="absolute top-full right-0 mt-2 bg-[#1a1a2e] border border-white/10 rounded-2xl shadow-2xl py-3 px-4 min-w-[12rem] z-50"
                >
                    <button
                        @click="clickMenu"
                        class="absolute top-3 right-3 text-white/60 hover:text-white transition-colors"
                    >
                        ✕
                    </button>
                    <ul class="flex flex-col items-end gap-1 pt-2">
                        <li v-if="!this.logado" class="w-full">
                            <a
                                class="flex items-center justify-end gap-3 w-full text-white text-xs sm:text-sm font-medium py-2 px-3 rounded-lg hover:bg-white/10 transition-colors cursor-pointer"
                                :class="{
                                    'font-extrabold underline':
                                        activeIndex === itensEsquerdo.length,
                                }"
                                @click="setActive('Acessar Sistema')"
                            >
                                Acessar Sistema
                            </a>
                        </li>
                        <li v-if="this.logado" class="w-full">
                            <a
                                class="flex items-center justify-end gap-3 w-full text-white text-xs sm:text-sm font-medium py-2 px-3 rounded-lg hover:bg-white/10 transition-colors cursor-pointer"
                                :class="{ 'font-extrabold underline': activeIndex === 6 }"
                                @click="setActive('Perfil')"
                            >
                                Perfil
                            </a>
                        </li>
                        <li v-if="this.logado" class="w-full">
                            <Sair></Sair>
                        </li>
                        <li v-if="this.logado" class="w-full">
                            <Salvar :modo="this.modoSalvar" :urlPDF="urlPDF"></Salvar>
                        </li>
                    </ul>
                </div>
            </transition>
            <li v-show="!this.logado && !this.isOpen" class="hidden sm:block">
                <a
                    class="cursor-pointer text-white text-xs sm:text-sm bg-transparent w-fit font-medium no-underline transition-all duration-300 p-1 inline-block text-center hover:bg-[hsla(267,81%,37%,0.63)] hover:font-semibold hover:scale-110 max-[940px]:p-0"
                    :class="{
                        'font-extrabold underline': activeIndex === itensEsquerdo.length,
                    }"
                    @click="setActive('Acessar Sistema')"
                    >Acessar Sistema</a
                >
            </li>
        </ul>
    </nav>
</template>

<script>
import Salvar from "../icons/Salvar.vue"
import Voltar from "../icons/Voltar.vue"
import Sair from "../icons/Sair.vue"

import axios from "axios"

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
        }
    },
    props: {
        activeIndex: 0,
        urlPDF: null,
    },
    created() {
        this.$store.subscribe((mutation, state) => {
            if (mutation.type === "setLogado") {
                this.logado = state.logado
            }
        })
    },
    mounted() {
        //executar checagem se esta logado

        this.emAnalise = this.$route.path === "/analise"
        this.logado = this.$store.getters.getLogado
        console.log("ANALISe")
    },
    methods: {
        setActive(nome) {
            this.$emit("update:activeIndex", nome)

            const mapa = {
                Início: "/",
                Método: "/metodo",
                Sobre: "/equipe",
                "Como Funciona?": "/duvidas",
                "Fazer Análise": "/ficha",
                "Acessar Sistema": "/acesso",
                Perfil: "/perfil",
            }
            const rota = mapa[nome]
            this.$router.push(rota)
        },

        async fnBaixar() {
            // lógica para salvar resultado
            console.log("Baixando...")
            if (this.urlPDF != null) {
                const res = await axios.get(this.urlPDF)
                console.log("HEADER: ")
            } else {
                alert("Nao foi possível encontrar relatório!")
            }
        },
        clickMenu() {
            if (this.isOpen) {
                this.isOpen = false
            } else {
                this.isOpen = true
                this.$refs.ladoDireito.style.alignItems = "flex-end"
            }
        },
    },
    computed: {
        modoSalvar() {
            if (this.emAnalise == true) {
                return "on"
            } else return "off"
        },
    },
}
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
    transition: opacity 0.2s ease, transform 0.2s ease;
}

.slide-enter-from,
.slide-leave-to {
    opacity: 0;
    transform: translateY(-8px);
}

.slide-enter-to,
.slide-leave-from {
    opacity: 1;
    transform: translateY(0);
}
</style>
