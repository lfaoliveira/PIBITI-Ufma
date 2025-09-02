<template>
    <div
        class="flex items-start justify-between w-[490px] p-4 gap-3 bg-white border border-black/10 rounded-2xl shadow-[0_20px_20px_rgba(0,0,0,0.08)]"
    >
        <!-- Left Section -->
        <div class="flex gap-3">
            <!-- Icon -->
            <div class="flex items-center justify-center w-8 h-8 bg-[#2C006F] rounded-lg">
                <!-- Star Icon -->
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="w-5 h-5 text-white"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        d="M12 .587l3.668 7.431 8.2 1.193-5.934 5.782 1.402 8.174L12 18.896l-7.336 3.856 1.402-8.174L.132 9.211l8.2-1.193z"
                    />
                </svg>
            </div>

            <!-- Text Content -->
            <div class="flex flex-col gap-2">
                <h2 class="font-montserrat font-semibold text-xl leading-6 text-black">
                    Vídeo Analisado com Sucesso!
                </h2>
                <p class="font-montserrat text-sm leading-[140%] text-[#792359]">
                    Clique no link abaixo para visualizar seu vídeo
                </p>
                <a
                    href="#"
                    class="font-inter font-bold text-sm leading-6 underline text-black"
                >
                    Clique Aqui
                </a>
            </div>
        </div>

        <!-- Close Button -->
        <button class="flex items-center justify-center w-6 h-6 bg-gray-300 rounded-full">
            <img src="../../assets/x.png" class="w-10 h-10 bg-black img" />
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
    props: {},
    computed: {},

    methods: {},
};
</script>

<style lang="scss" scoped>
/* No scoped styles needed as Tailwind handles most of it */
/* You might keep this section for any custom utility classes or base styles not covered by Tailwind */
</style>
