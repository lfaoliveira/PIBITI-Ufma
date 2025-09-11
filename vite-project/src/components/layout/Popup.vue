<template>
    <div
        :class="[
            String(posCSS) ,
            'flex items-start justify-between h-3.5lh w-min sm:w-60 sm:mr-0 md:w-100 md:h-[6.5lh] z-3  p-2 sm:p-4 gap-3',
            'bg-white border border-black/10 rounded-2xl shadow-lg']"
    >
        <!-- Left Section -->
        <div class="flex gap-3">
            <!-- Icon -->
            <div class="flex items-center justify-center w-1/8 h-min rounded-lg">
                <!-- Star Icon -->
                <img src="../../assets/estrela_roxa.png" class=" w-6 min-w-6 sm:w-8 sm:h-8 text-white" />
            </div>

            <!-- Text Content -->
            <div class="flex flex-col gap-2">
                <h2 class="font-montserrat !font-bold text-xl leading-6 text-black">
                    Vídeo Analisado com Sucesso!
                </h2>
                <p class="font-montserrat text-sm leading-[140%] text-[#792359]">
                    Clique no link abaixo para visualizar seu vídeo
                </p>
                <a
                    :href="link"
                    class="!font-inter !font-bold !text-sm !underline !text-black w-"
                >
                    Clique Aqui
                </a>
            </div>
        </div>

        <!-- Close Button -->
        <button
            @click="this.close()"
            class="flex items-center justify-center aspect-square w-6 min-w-6 bg-gray-300 !border-0 hover:border-4 hover:bg-gray-200 hover:border-black hover:brightness-100 transition-all duration-200 rounded-full"
        >
            <img src="../../assets/x.png" class="relative aspect-square w-1/2" />
        </button>
    </div>
</template>

<script>
import { mapActions, mapState } from "vuex";

import Estrela from "../icons/Estrela.vue";
import X from "../icons/X.vue";

export default {
    name: "Popup",
    components: {
        Estrela,
        X,
    },
    props: {
        link: { type: String, default: "#", required: true },
        posCSS: {
            type: String,
            default: "absolute top-22 right-5 w-28 h-auto"
        },
    },
    computed: {},

    methods: {
        ...mapActions("modal", ["closeModal", "openModal", "closeAllModals"]),
        close() {
            this.$emit("close");
            this.closeModal("popup");
        },
    },
};
</script>

<style lang="scss" scoped>
/* No scoped styles needed as Tailwind handles most of it */
/* You might keep this section for any custom utility classes or base styles not covered by Tailwind */
</style>
