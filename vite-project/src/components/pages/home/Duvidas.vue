<template>
    <HeaderSistema :activeIndex="3" />

    <div class="flex flex-col items-center gap-[clamp(20px,4vmin,40px)]">
        <section
            class="flex flex-col justify-center items-center w-[60%] max-[500px]:w-[95%] gap-[clamp(20px,4vmin,40px)]"
        >
            <h2 class="text-2xl font-bold text-center">
                Como obter o vídeo que será processado?
            </h2>
            <p class="text-justify">
                Os vídeos podem ser gravados com câmeras de smartphones comuns apoiadas em
                um tripé. Para evitar movimentação da cabeça, o paciente deve apoiar os
                cotovelos sobre uma mesa, cerrar os punhos e descansar o queixo sobre
                eles. A gravação começa com o paciente olhando para frente (posição
                primária). Em seguida, ele é orientado a mover os olhos para a esquerda e
                depois para a direita, repetindo esse movimento algumas vezes. É
                importante que ambos os olhos estejam visíveis e alinhados horizontalmente
                no vídeo. Esse protocolo garante estabilidade e qualidade adequadas para
                análise do movimento ocular.
            </p>
            <p class="text-justify">
                Após a aplicação do protocolo, clique em "Fazer Análise" e então preencha
                os respectivos dados do paciente, fazendo envio do vídeo para análise no
                sistema.
            </p>
            <img
                src="../../../assets/duvidas/tela_ficha.png"
                alt="Pessoa segurando um mouse"
                class="w-[30%] h-auto border"
            />
        </section>

        <section
            class="flex flex-col justify-center items-center w-[60%] max-[500px]:w-[95%] gap-[clamp(20px,4vmin,40px)]"
        >
            <h2 class="text-2xl font-bold text-center">
                Como fazer a análise no sistema?
            </h2>
            <p class="text-justify">
                Após o envio do vídeo, o processamento é realizado automaticamente pelos
                servidores da plataforma. Quando a análise é concluída, uma notificação
                aparace na tela e quando clicada o médico é redirecionado para a tela de
                resultados, onde pode visualizar o diagnóstico indicando se há indícios de
                paralisia do sexto nervo em um ou ambos os olhos, a diferença percentual
                de velocidade entre os olhos e as velocidades médias de cada olho em mm/s.
                A tela também exibe um gráfico da evolução temporal da velocidade
                sacádica, o vídeo processado com as marcações da rede neural e a opção de
                exportar um relatório completo em PDF para prontuário ou compartilhamento.
            </p>
            <img
                src="../../../assets/duvidas/tela_ficha_diag_sucesso.png"
                alt="Pessoa utilizando um mouse"
                class="w-[30%] h-auto border"
            />
        </section>

        <Rodape></Rodape>
    </div>
</template>

<script>
import HeaderSistema from "../../layout/HeaderSistema.vue"
import Rodape from "../../layout/Rodape.vue"

export default {
    name: "duvidas",
    components: {
        HeaderSistema,
        Rodape,
    },
    created() {},
    data() {
        return {}
    },
    props: {},
    methods: {},
}
</script>

<style lang="scss" scoped>
/* Estilos substituídos por Tailwind */
</style>
