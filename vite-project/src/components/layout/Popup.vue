<template>
    <div
        class="bg-[#fff] rounded-xl p-6 text-white shadow-lg w-11/12 max-w-sm font-sans text-center"
    >
        <div class="flex items-center justify-center mb-4 relative">
            <div
                class="w-8 h-8 mr-3 bg-white rounded-full flex items-center justify-center"
            >
                <Estrela></Estrela>
            </div>
            <h2 class="text-xl text-black font-extrabold m-0">
                Vídeo Analisado com Sucesso!
            </h2>
            <button
                class="absolute -top-3 -right-3 bg-transparent border-none text-gray-400 text-1xl cursor-pointer p-1"
                @click="$emit('close')"
            >
                &times;
            </button>
        </div>
        <p class="text-[#c080c0] text-sm underline mb-6">
            Clique no link abaixo para visualizar seu vídeo
        </p>
        <a
            href="#"
            class="text-white text-base font-medium underline cursor-pointer"
            @click.prevent="$emit('view-video')"
        >
            Clique Aqui
        </a>
    </div>
</template>

<script>
import { mapActions, mapState } from "vuex";

import Estrela from "../icons/Estrela.vue";

export default {
    name: "Popup",
    components: {
        Estrela,
    },
    props: {
        name: "popup",
    },
    computed: {
        ...mapState("modal", ["modals"]),
        modalState() {
            console.log(
                "LOAD MODAL STATE POPUP.vue: " + JSON.stringify(this.modals[this.name])
            );
            return this.modals[this.name] || {};
        },
        isOpen() {
            console.log("Popup.vue ABERTO: " + String(this.modalState.isOpen));
            return this.modalState.isOpen;
        },
        content() {
            return this.modalState.content || {};
        },
    },
    // mounted() {
    //     console.log(this.modals.isOpen);
    // },
    methods: {},
};
</script>

<style lang="scss" scoped>
/* No scoped styles needed as Tailwind handles most of it */
/* You might keep this section for any custom utility classes or base styles not covered by Tailwind */
</style>
