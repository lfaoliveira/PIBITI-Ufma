<template>
    <section
        :class="[
            posCSS,
            // overlay container
            'z-3 relative top-5/100 flex flex-col justify-between items-center transition-all duration-500 ease-in',
            // recommended responsive breakpoints
            'h-80 w-[100%] sm:h-fit sm:top-15/100 sm:w-auto',
            // content styles
            'p-4 gap-3 bg-white border border-black/10 rounded-2xl shadow-lg'
        ]"
    >
        <div class="flex justify-center items-start gap-[2vmin] text-black">
            <img :src="srcImg" class="ml-[5vmin] w-4/20 h-4/20 sm:w-15 sm:h-15" />
            <ul class="flex flex-col items-start self-stretch gap-[5vmin] w-fit">
                <h1>{{ titulo }}</h1>
                <h1 class="w-20 max-w-[10ch]">{{ subtexto }}</h1>
                <h1 v-if="opcional !== ''" id="opcional" class="text-[#792359]">
                    {{ opcional }}
                </h1>
            </ul>
        </div>
        <div class="w-30">
            <Button @click="close()" :texto="'OK'" :ativo="true" />
        </div>
    </section>
</template>

<script>
import Button from "../navigation/Button.vue";
import { mapActions, mapState } from "vuex";

export default {
    name: "overlay",
    components: {
        Button,
    },

    data() {
        return {
            aberto: null,
        };
    },
    props: {
        eventoAviso: "", //
        titulo: "",
        subtexto: "",
        opcional: "",
        srcImg: { type: String, default: "", required: true },
        rota: null,
        posCSS: "",
    },
    computed:{

    },
    methods: {
        ...mapActions("modal", ["closeModal", "openModal", "closeAllModals"]),
        close() {
            this.closeModal("overlay");
            console.log("fechando OVERLAY")
        },
    },

};
</script>

<style lang="scss" scoped>
.overlay {
    @include overlay;
    background: white;

    gap: 5vmin;

    img {
        margin-left: 5vmin;
        width: 10vmin;
        height: 10vmin;
    }

    .alerta {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        gap: 2vmin;

        .textos {
            display: flex;
            width: fit-content;
            flex-direction: column;
            align-items: flex-start;
            gap: 5vmin;
            align-self: stretch;
        }
        #opcional {
            color: #792359;
        }
    }
    .div-but {
        width: 22vmin;
    }
}
</style>
