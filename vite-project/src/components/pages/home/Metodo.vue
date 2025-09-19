<template>
    <HeaderSistema :activeIndex="1"></HeaderSistema>
    <div class="frame-pagina">
        <section class="secao-texto tipo1">
            <h2 class="titulo-secao">Sobre o Software</h2>
            <p class="texto-secoes" id="about-description">
                Nosso sistema é uma solução não invasiva para auxiliar no
                diagnóstico da paralisia do sexto nervo craniano (SONP). A tecnologia
                analisa vídeos simples dos movimentos oculares e calcula a velocidade
                média de cada olho, permitindo identificar diferenças que podem indicar a
                presença da paralisia. O método foi desenvolvido em ambiente clínico e
                demonstrou alta precisão e confiabilidade para apoiar médicos no processo
                de avaliação.
            </p>
        </section>

        <section class="secao-com-imagem tipo2">
            <h2 class="titulo-secao">Sexto Nervo Óptico</h2>
            <div class="texto-imagem">
                <p class="texto-grande" id="optic-nerve-description">
                    O músculo reto lateral é controlado pelo sexto nervo craniano, também
                    chamado de nervo abducente. Esse nervo é responsável por mover os olhos
                    para fora, em direção ao canto externo. Quando há uma lesão nesse nervo,
                    o olho perde parcial ou totalmente a capacidade de realizar esse
                    movimento, caracterizando a paralisia do sexto nervo.
                </p>
                <div class="div-nervo">
                    <img
                        alt="Ilustração do sexto nervo óptico"
                        class="optic-nerve-image"
                        src="../../../assets/sexto-nervo.png"
                    />
                </div>
            </div>
        </section>

        <section class="secao-texto tipo1">
            <h2 class="titulo-secao" id="titulo-protocolo">Protocolo de Aquisição</h2>
            <p class="texto-secoes" id="protocol-description">
                Os vídeos podem ser gravados com câmeras de smartphones comuns apoiadas em
                um tripé. Para evitar movimentação da cabeça, o paciente deve apoiar os
                cotovelos sobre uma mesa, cerrar os punhos e descansar o queixo sobre eles.
                A gravação começa com o paciente olhando para frente (posição primária).
                Em seguida, ele é orientado a mover os olhos para a esquerda e depois para
                a direita, repetindo esse movimento algumas vezes. É importante que ambos
                os olhos estejam visíveis e alinhados horizontalmente no vídeo. Esse
                protocolo garante estabilidade e qualidade adequadas para análise do
                movimento ocular.
            </p>
        </section>

        <section class="secao-texto tipo2">
            <h2 class="titulo-secao" id="titulo-deteccao">Método de Detecção</h2>
            <p class="texto-secoes" id="method-description">
                O sistema identifica automaticamente a região dos olhos em cada quadro do
                vídeo por meio de redes neurais de detecção de objetos. Em seguida, registra
                a trajetória do movimento ocular e aplica filtros matemáticos para corrigir
                eventuais imprecisões. Com base nessa trajetória, calcula a velocidade de
                cada olho e compara os resultados. Diferenças significativas de velocidade entre os olhos
                podem indicar a presença de paralisia.
            </p>
        </section>

        <section class="secao-texto tipo1">
            <h2 class="titulo-secao" id="metodo">Método de Cálculo da Velocidade</h2>
            <p class="texto-secoes" id="calculation-description">
                A velocidade média do olho é calculada a partir do deslocamento horizontal
                entre quadros sucessivos do vídeo. Como o sexto nervo óptico controla
                exclusivamente os movimentos laterais, o cálculo considera apenas esse
                eixo. Se um dos olhos se movimentar pelo menos 19,65% mais devagar que o
                outro, o sistema classifica o paciente como portador de paralisia do sexto
                nervo no olho mais lento. Estudos clínicos demonstraram que esse método
                alcança mais de 92% de precisão, tornando-se um forte aliado na prática
                médica. 
            </p>
        </section>
        <Rodape></Rodape>
    </div>
</template>


<script>
import Rodape from "../../layout/Rodape.vue";
import HeaderSistema from "../../layout/HeaderSistema.vue";

export default {
    name: "compMetodo",
    components: {
        Rodape,
        HeaderSistema,
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
$Fonte-Titulo-Secao: clamp(22px, 5vmin, 30px);

.frame-pagina {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 20px;
}

.secao-texto {
    display: flex;
    width: 100%;
    padding: 20px 20px;
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
}

.titulo-secao {
    text-align: center;
    font-size: $Fonte-Titulo-Secao;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
}

.secao-com-imagem {
    display: flex;
    padding: 0px 20px;
    flex-direction: column;
    align-items: flex-start;
    align-self: stretch;
}

.texto-imagem {
    display: flex;
    flex-direction: row;
    padding: 13px 0px;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 81px;
    width: 100%;
}

.texto-grande {
    flex: 0.9;
}

.div-nervo {
    display: flex;
    padding-bottom: 20px;
    align-items: center;
    padding: 1px;
    border: 1px solid #61616198;
}

.optic-nerve-image {
    width: auto;
    height: clamp(24vmin, 236px, 50vmin);
    aspect-ratio: 379/336;
}

.tipo1 {
    color: white;
    background-color: #6113c6;
}

.tipo2 {
    color: black;
    background-color: white;
}

@media (max-width: 700px) {
    .texto-imagem {
        flex-direction: column;
    }
    .div-nervo {
        width: 100%;
        height: max-content;
        justify-content: center;
        align-items: center;
    }
    .optic-nerve-image {
        width: clamp(20vmin, 286px, 376px);
        // height: clamp(30vmin, 246px, 40vmin);
        height: auto;
        aspect-ratio: 379/336;
    }
}
</style>
