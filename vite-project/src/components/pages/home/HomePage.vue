<template>
    <main class="flex items-center flex-col gap-[clamp(30px,13vmin,100px)] shrink-0 self-stretch w-full h-full justify-center mx-0 max-w-full flex-wrap">
        <HeaderSistema :activeIndex="0"></HeaderSistema>

        <div id="div-video-home" class="w-[clamp(92%,100%,100%)] flex self-center h-full absolute bottom-0 flex-wrap justify-start">
            <video
                alt="Header background"
                class="w-full h-full absolute object-cover z-0 self-center"
                preload="auto"
                autoplay
                loop
                src="../../../assets/video-oftalmo.mp4"
            />
            <figure class="w-full h-full absolute pointer-events-none bg-[rgba(18,18,18.1,0.41)]" />
        </div>
        <div class="mx-auto flex justify-center items-center relative h-auto w-[clamp(290px,64ch,100%)] my-0">
            <h1 id="titulo" class="text-white font-semibold text-[clamp(14px,5.33vmin,41px)] text-start max-[500px]:text-center w-auto mx-auto">
                6NerveTrack: Análise de Vídeos de Paralisia do Sexto Nervo Óptico
            </h1>
        </div>
        <div class="flex w-[30vmin] items-start flex-col items-center gap-[5vmin] shrink-0 z-[1]">
            <Button @click="fnDuvidas" texto="Como Funciona?" :ativo="true"> </Button>
            <Button @click="fnFicha" texto="Fazer Análise" :ativo="true"> </Button>
        </div>
    </main>
</template>

<style lang="scss" scoped>
input {
    display: none;
}
</style>

<script>
import HeaderSistema from "../../layout/HeaderSistema.vue";
import Button from "../../navigation/Button.vue";

export default {
    name: "HomePage",
    components: {
        HeaderSistema,
        Button,
    },
    setup() {},
    methods: {
        fnDuvidas() {
            this.$router.push("/duvidas");
        },
        fnFicha() {
            this.$router.push("/ficha");
        },
    },
    props: {},
    data() {
        return {};
    },
    mounted() {
        console.log("MONTADO HOMEPAGE");
    },
};
</script>
