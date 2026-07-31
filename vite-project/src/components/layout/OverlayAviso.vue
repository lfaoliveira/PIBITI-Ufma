<template>
    <section v-if="aberto" class="z-20 flex flex-col items-center absolute mx-auto bg-white border border-black h-[90vmin] transition-all duration-500 ease-in w-1/2 max-[870px]:w-full max-[870px]:h-[90%] gap-[5vmin]">
        <div class="flex justify-center items-start gap-[2vmin]">
            <img :src="srcImg" class="ml-[5vmin] w-[10vmin] h-[10vmin]" />
            <ul class="flex w-fit flex-col items-start gap-[5vmin] self-stretch">
                <h1>{{ titulo }}</h1>
                <h1>{{ subtexto }}</h1>
                <h1 v-if="opcional !== ''" id="opcional" class="text-[#792359]">{{ opcional }}</h1>
            </ul>
        </div>
        <div class="w-[22vmin]">
            <Button @click="closeOverlay" :texto="'OK'" :ativo="true"></Button>
        </div>
    </section>
</template>

<script>
import Button from "../navigation/Button.vue";
import emitter from "../../eventBus.js";

export default {
    name: "overlay",
    components: {
        Button,
    },
    created() {
        // Listen for the 'cadastroRepetido' event
        emitter.on(this.eventoAviso, this.openOverlay);
    },
    mounted() {
        console.log("MONTADO AVISo");
    },
    beforeUnmount() {
        // Clean up the event listener
        emitter.off(this.eventoAviso, this.openOverlay);
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
    },
    methods: {
        openOverlay() {
            this.aberto = true;
        },
        closeOverlay() {
            this.aberto = false;
            if (this.rota != null) {
                console.log("ROTA: ", this.rota);
                this.$router.push(this.rota);
            }
        },
    },
};
</script>

<style lang="scss" scoped>
/* Estilos substituídos por Tailwind */
</style>
