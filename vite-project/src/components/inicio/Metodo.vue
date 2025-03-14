<template>
  <section class="secao-texto tipo1">
    <h2 class="titulo-secao">Sobre o Software</h2>
    <p class="texto-secoes" id="about-description">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer fringilla mi a
      lorem tincidunt imperdiet. Duis ac nisl pellentesque, posuere dui eu, iaculis
      lectus. Curabitur vehicula nibh urna
    </p>
  </section>

  <section class="secao-com-imagem tipo2">
    <h2 class="titulo-secao">Sexto Nervo Óptico</h2>
    <div class="texto-imagem">
      <p class="texto-grande" id="optic-nerve-description">
        O músculo reto lateral é inervado pelo sexto nervo óptico, também chamado de nervo
        abducente, como ilustra a figura. Este nervo é diretamente responsável pela
        contração do músculo reto lateral. O reto lateral permite que o olho faça o
        movimento de abdução, ou seja, que se mova em direção ao seu canto externo. Uma
        lesão no sexto nervo causa a paralisia parcial ou total do músculo reto lateral,
        impossibilitando ou limitando a abdução
      </p>
      <div class="div-nervo">
        <img
          alt="Ilustração do sexto nervo óptico"
          class="optic-nerve-image"
          src="../../assets/sexto-nervo.png"
        />
      </div>
    </div>
  </section>

  <section class="secao-texto tipo1">
    <h2 class="titulo-secao" id="titulo-protocolo">Protocolo de Aquisição</h2>
    <p class="texto-secoes" id="protocol-description">
      Os vídeos podem ser gravados com câmeras comuns ou com smartphones, mas para isso,
      usa-se um tripé para garantir a estabilidade da câmera. Além disso, a fim de evitar
      ruídos no resultado final causados pelo balançar da cabeça do paciente, pede-se que
      este apoie os cotovelos em uma mesa, cerre os punhos, juntando-os e apoiando o
      queixo em ambos os punhos. O vídeo começa a ser gravado com o paciente olhando para
      a frente, com os olhos na posição primária (PPO). Ambos os olhos do paciente
      precisam estar visíveis no vídeo, e alinhados horizontalmente; não é preciso que o
      rosto inteiro do paciente esteja visível, mas não há problema se estiver. Em
      seguida, pede-se que o paciente olhe para a esquerda, depois que olhe para a
      direita. Esse movimento é repetido algumas vezes, com o objetivo de analisar a
      movimentação horizontal dos olhos
    </p>
  </section>

  <section class="secao-texto tipo2">
    <h2 class="titulo-secao" id="titulo-deteccao">Método de Detecção</h2>
    <p class="texto-secoes" id="method-description">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer fringilla mi a
      lorem tincidunt imperdiet. Duis ac nisl pellentesque, posuere dui eu, iaculis
      lectus. Curabitur vehicula nibh urna
    </p>
  </section>

  <section class="secao-texto tipo1">
    <h2 class="titulo-secao" id="metodo">Método de Cálculo da Velocidade</h2>
    <p class="texto-secoes" id="calculation-description">
      Praesent in lobortis purus, id blandit leo. Vestibulum posuere urna vitae
      scelerisque lacinia. Donec nec elit efficitur, sollicitudin est nec, sodales mauris.
      Maecenas et purus vel massa varius sodales. mi a lorem tincidunt imperdiet. Duis ac
      nisl pellentesque, posuere dui eu, iaculis lectus. Curabitur vehicula nibh urna
    </p>
  </section>
  <Rodape></Rodape>
</template>

<script>
import Rodape from "../auxiliares/Rodape.vue";

export default {
  name: "compMetodo",
  components: {
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
$Fonte-Titulo-Secao: 32px;

* {
  display: flex;
  flex-direction: column;

  justify-content: center;
  gap: 20px;
}

.frame-pagina {
  width: 95%;
}

.secao-texto {
  display: flex;
  width: 100%;
  padding: 0px 20px;
  flex-direction: column;
  align-items: flex-start;
  gap: 40px;
}

.titulo-secao {
  text-align: center;
  font-size: $Fonte-Titulo-Secao;
  font-style: normal;
  font-weight: 700;
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
  box-shadow: 0px 0px 31.9px 4px rgba(0, 0, 0, 0.25);
}

.optic-nerve-image {
  width: 50vmin;
  height: 43vmin;
}

.tipo1 {
  color: white;
  background-color: #6113c6;
}

.tipo2 {
  color: black;
  background-color: white;
}
</style>
