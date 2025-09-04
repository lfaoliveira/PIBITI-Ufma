<template>
    <section
        v-if="aberto"
        :class="[
            posCSS,
            // overlay styles (converted from @mixin overlay)
            'z-20 flex flex-col items-center absolute m-auto bg-white border border-black h-[90vmin] w-1/2 transition-all duration-500 ease-in',
            // responsive adjustment (media query)
            'max-[870px]:w-full max-[870px]:h-[90%]',
            // inner styles (from your SCSS)
            'flex items-start justify-between w-auto p-4 gap-3 bg-white border border-black/10 rounded-2xl shadow-[0_20px_20px_rgba(0,0,0,0.08)]'
        ]"
    >
        <div class="flex justify-center items-start gap-[2vmin]">
            <img :src="srcImg" class="ml-[5vmin] w-[10vmin] h-[10vmin]" />
            <ul class="flex flex-col items-start self-stretch gap-[5vmin] w-fit">
                <h1>{{ titulo }}</h1>
                <h1>{{ subtexto }}</h1>
                <h1 v-if="opcional !== ''" id="opcional" class="text-[#792359]">
                    {{ opcional }}
                </h1>
            </ul>
        </div>
        <div class="w-[22vmin]">
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
            aberto: true,
        };
    },
    props: {
        eventoAviso: "", //
        titulo: "",
        subtexto: "",
        opcional: "",
        srcImg: { type: String, default: "", required: true },
        rota: null,
        posCSS: "absolute top-22 right-0 w-28 h-auto",
    },

    methods: {
        ...mapActions("modal", ["closeModal", "openModal", "closeAllModals"]),
        close() {
            this.$emit("close");
            this.closeModal("overlay");
            this.aberto = false;
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
