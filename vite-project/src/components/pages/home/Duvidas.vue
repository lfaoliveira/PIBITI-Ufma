<template>
    <HeaderSistema :activeIndex="3" />

    <div class="flex flex-col items-center gap-[clamp(20px,4vmin,40px)]">
        <section class="flex flex-col justify-center items-center w-[60%] max-[500px]:w-[95%] gap-[clamp(20px,4vmin,40px)]">
            <h2 class="text-2xl font-bold text-center">Como obter o vídeo que será processado?</h2>
            <p class="text-justify">
                Praesent nec justo turpis. Maecenas tortor est, posuere in orci quis,
                tempus sagittis nisl. Proin ullamcorper faucibus odio eget fermentum. Ut
                vitae dapibus enim, quis tincidunt neque. Suspendisse vitae condimentum
                ipsum. Praesent faucibus nunc eu odio aliquet congue.
            </p>
            <p class="text-justify">
                Praesent nec justo turpis. Maecenas tortor est, posuere in orci quis,
                tempus sagittis nisl. Proin ullamcorper faucibus odio eget fermentum. Ut
                vitae dapibus enim, quis tincidunt neque. Suspendisse vitae condimentum
                ipsum. Praesent faucibus nunc eu odio aliquet congue. Donec congue feugiat
                ligula, in porta tortor eleifend quis. Nulla vel felis eu sapien pharetra
                facilisis. Curabitur vel est pharetra, viverra ante id, sodales arcu.
                Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere
                cubilia curae; Ut sit amet condimentum lectus, dapibus eleifend dolor.
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            </p>
            <img src="../../../assets/dummy.png" alt="Pessoa segurando um mouse" class="w-[70%] aspect-[62/40] h-auto" />
        </section>

        <section class="flex flex-col justify-center items-center w-[60%] max-[500px]:w-[95%] gap-[clamp(20px,4vmin,40px)]">
            <h2 class="text-2xl font-bold text-center">Como fazer a análise do sistema?</h2>
            <p class="text-justify">
                Praesent nec justo turpis. Maecenas tortor est, posuere in orci quis,
                tempus sagittis nisl. Proin ullamcorper faucibus odio eget fermentum. Ut
                vitae dapibus enim, quis tincidunt neque. Suspendisse vitae condimentum
                ipsum. Praesent faucibus nunc eu odio aliquet congue.
            </p>
            <img src="../../../assets/dummy.png" alt="Pessoa utilizando um mouse" class="w-[70%] aspect-[62/40] h-auto" />
        </section>

        <Rodape></Rodape>
    </div>
</template>

<script>
import HeaderSistema from "../../layout/HeaderSistema.vue";
import Rodape from "../../layout/Rodape.vue";

export default {
    name: "duvidas",
    components: {
        HeaderSistema,
        Rodape,
    },
    created() {},
    data() {
        return {};
    },
    props: {},
    methods: {},
};
</script>

<style lang="scss" scoped>
/* Estilos substituídos por Tailwind */
</style>
