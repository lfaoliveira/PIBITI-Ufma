<template>
    <HeaderSistema :activeIndex="3" />

    <div class="frame-pagina">
        <section class="secao-conteudo">
            <h2>Como obter o vídeo que será processado?</h2>
            <p>
                Praesent nec justo turpis. Maecenas tortor est, posuere in orci quis,
                tempus sagittis nisl. Proin ullamcorper faucibus odio eget fermentum. Ut
                vitae dapibus enim, quis tincidunt neque. Suspendisse vitae condimentum
                ipsum. Praesent faucibus nunc eu odio aliquet congue.
            </p>
            <p>
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
            <img src="../../assets/dummy.png" alt="Pessoa segurando um mouse" />
        </section>

        <section class="secao-conteudo">
            <h2>Como fazer a análise do sistema?</h2>
            <p>
                Praesent nec justo turpis. Maecenas tortor est, posuere in orci quis,
                tempus sagittis nisl. Proin ullamcorper faucibus odio eget fermentum. Ut
                vitae dapibus enim, quis tincidunt neque. Suspendisse vitae condimentum
                ipsum. Praesent faucibus nunc eu odio aliquet congue.
            </p>
            <img src="../../assets/dummy.png" alt="Pessoa utilizando um mouse" />
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
.frame-pagina {
    display: flex;
    align-items: center;
    flex-direction: column;
    gap: clamp(20px, 4vmin, 40px);
}

.secao-conteudo {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 60%;
    gap: clamp(20px, 4vmin, 40px);
}

@media (max-width: 500px) {
    .secao-conteudo {
        width: 95%;
    }
}

h2 {
    font-size: 1.5em;
    font-weight: bold;
    text-align: center;
}

p {
    text-align: justify;
}

img {
    width: 70%;
    aspect-ratio: 62/40;
    height: auto;
}
</style>
