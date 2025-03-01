#CODIGO GERADO POR IA:
<template>
  <Landing></Landing>

  <section class="features secao">
    <div class="sobre-titulo">
      <img class="img-medicos" src="../../assets/medicos.png" />
      <div class="estrelas">
        <img class="estrela-img" src="../../assets/estrela.png" />
        <img class="estrela-img" src="../../assets/estrela.png" />
        <img class="estrela-img" src="../../assets/estrela.png" />
        <img class="estrela-img" src="../../assets/estrela.png" />
        <img class="estrela-img" src="../../assets/estrela.png" />
      </div>
    </div>
    <h2 class="section-title" id="titulo-conv">
      Analisado e aprovado por oftalmologistas!
    </h2>
    <div class="feature-list">
      <div class="feature-item">
        <img
          src="../../assets/aprovado.png"
          alt="Análise de vídeos"
          class="feature-icon"
        />
        <p class="feature-description">
          Analise vídeos de paralisia do sexto nervo óptico
        </p>
      </div>
      <div class="feature-item">
        <img
          src="../../assets/aprovado.png"
          alt="Gráficos resultantes"
          class="feature-icon"
        />
        <p class="feature-description">Observe os gráficos resultantes</p>
      </div>
      <div class="feature-item">
        <img src="../../assets/aprovado.png" alt="Salvar gráficos" class="feature-icon" />
        <p class="feature-description">Salve os gráficos a qualquer momento!</p>
      </div>
      <div class="feature-item">
        <img
          src="../../assets/aprovado.png"
          alt="Análise em velocidades diferentes"
          class="feature-icon"
        />
        <p class="feature-description">Analise os vídeos em velocidades diferentes</p>
      </div>
    </div>
  </section>
  <div id="divisor" class="secao">
    <img
      src="../../assets/logo_VIP_Lab.png"
      alt="Logo VIpLab"
      class="img-logos"
      id="logo-vip"
    />
    <img
      src="../../assets/logo ufma.png"
      alt="Logo UFMA"
      class="img-logos"
      id="logo-ufma"
    />
    <img
      src="../../assets/LogoNCAFundBranco2000_2021.png"
      alt="Logo VIpLab"
      class="img-logos"
      :id="this.idNCA"
    />
  </div>

  <section class="about secao">
    <h2 class="section-title" id="titulo-about">Sobre o Software</h2>
    <p class="texto-secoes" id="about-description">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer fringilla mi a
      lorem tincidunt imperdiet. Duis ac nisl pellentesque, posuere dui eu, iaculis
      lectus. Curabitur vehicula nibh urna
    </p>
  </section>

  <section class="optic-nerve secao">
    <div class="optic-nerve-text">
      <h2 class="section-title" id="titulo-nervo">Sexto Nervo Óptico</h2>
      <p class="texto-secoes" id="optic-nerve-description">
        O músculo reto lateral é inervado pelo sexto nervo óptico, também chamado de nervo
        abducente, como ilustra a figura. Este nervo é diretamente responsável pela
        contração do músculo reto lateral. O reto lateral permite que o olho faça o
        movimento de abdução, ou seja, que se mova em direção ao seu canto externo. Uma
        lesão no sexto nervo causa a paralisia parcial ou total do músculo reto lateral,
        impossibilitando ou limitando a abdução
      </p>
    </div>
    <div class="div-nervo">
      <img
        alt="Ilustração do sexto nervo óptico"
        class="optic-nerve-image"
        src="../../assets/sexto-nervo.png"
      />
    </div>
  </section>

  <section class="faq secao">
    <h2 class="section-title" id="faq-titulo">Perguntas Frequentes</h2>
    <div class="faq-grid">
      <div class="faq-item">
        <h3 class="faq-question">Pergunta 1</h3>
        <p class="faq-answer">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer fringilla mi a
          lorem
        </p>
      </div>
      <div class="faq-item">
        <h3 class="faq-question">Pergunta 2</h3>
        <p class="faq-answer">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer fringilla mi a
          lorem
        </p>
      </div>
      <div class="faq-item">
        <h3 class="faq-question">Pergunta 3</h3>
        <p class="faq-answer">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer fringilla mi a
          lorem
        </p>
      </div>
      <div class="faq-item">
        <h3 class="faq-question">Pergunta 4</h3>
        <p class="faq-answer">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer fringilla mi a
          lorem
        </p>
      </div>
      <div class="faq-item">
        <h3 class="faq-question">Pergunta 5</h3>
        <p class="faq-answer">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer fringilla mi a
          lorem
        </p>
      </div>
      <div class="faq-item">
        <h3 class="faq-question">Pergunta 6</h3>
        <p class="faq-answer">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer fringilla mi a
          lorem
        </p>
      </div>
    </div>
  </section>

  <section class="acquisition-protocol secao">
    <h2 class="section-title" id="titulo-protocolo">Protocolo de Aquisição</h2>
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

  <section class="detection-method secao">
    <h2 class="section-title" id="titulo-deteccao">Método de Detecção</h2>
    <p class="texto-secoes" id="method-description">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer fringilla mi a
      lorem tincidunt imperdiet. Duis ac nisl pellentesque, posuere dui eu, iaculis
      lectus. Curabitur vehicula nibh urna
    </p>
  </section>

  <section class="velocity-calculation secao">
    <h2 class="section-title" id="metodo">Método de Cálculo da Velocidade</h2>
    <p class="texto-secoes" id="calculation-description">
      Praesent in lobortis purus, id blandit leo. Vestibulum posuere urna vitae
      scelerisque lacinia. Donec nec elit efficitur, sollicitudin est nec, sodales mauris.
      Maecenas et purus vel massa varius sodales. mi a lorem tincidunt imperdiet. Duis ac
      nisl pellentesque, posuere dui eu, iaculis lectus. Curabitur vehicula nibh urna
    </p>
  </section>

  <section class="team secao">
    <h2 class="section-title" id="titulo-equipe">Equipe</h2>
    <div class="team-content">
      <p class="texto-secoes" id="team-description">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer fringilla mi a
        lorem tincidunt imperdiet. Duis ac nisl pellentesque, posuere dui eu, iaculis
        lectus. Curabitur vehicula nibh urna Morbi vulputate magna id magna tempus
        volutpat. Duis metus elit, egestas id lorem at, dictum sollicitudin nunc. Nunc a
        bibendum leo. Fusce efficitur nibh a pretium feugiat. In at facilisis ante. Nullam
        id velit sed dolor mattis fringilla. Aliquam id interdum lorem
      </p>
      <img
        alt="Imagem Time do VipLab"
        class="team-image"
        src="../../assets/foto time.png"
      />
    </div>
  </section>

  <rodape class="secao" />
</template>

<style scoped>
/* classes principais */
.secao {
  margin: 5vmin 0vmin 0vmin 0vmin;
  max-width: 100%;

  align-self: center;
  /* padding: 0vmin 2vmin; */
  flex-wrap: wrap;
}
.section-title {
  font-size: clamp(0.6em, 2em, 3em);
  margin: 2vmin 0vmin 2vmin 2vmin;
  font-weight: 700;
}

.texto-secoes {
  margin: 2vmin;
  font-size: clamp(0.5em, 1em, 1.5em);
}

/* classes específicas */

/* convencimento */

.features {
  display: flex;
  flex-direction: column;
}
.sobre-titulo {
  flex: 2;
  display: flex;
  justify-content: center;
  align-content: center;
  width: 75%;
}
.estrelas {
  display: flex;
  align-content: center;
  flex: 1.5;
}

.img-medicos {
  width: auto;
  height: 50%;
  margin: 0vmin 2vmin;
}

.estrela-img {
  width: clamp(20px, 5.4vmin, 59px);
  height: clamp(20px, 5vmin, 60px);
  align-self: center;
}

#titulo-conv {
  margin: 0px;
  margin-bottom: 2vmin;
  left: 0px;
  flex: 1;
  font-size: 32px;
  font-weight: 800;
}
.feature-list {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  flex-wrap: wrap;
}

.feature-item {
  margin-bottom: 5px;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.feature-icon {
  margin: 0px;
  margin-right: 9px;
  width: clamp(2vmin, 25px, 30px);
  height: auto;
}

.feature-description {
  margin: 0px;
  text-align: center;
  width: auto;
  font-size: clamp(15px, 3vmin, 25px);
  color: #792359;
}

/* divisor e logos*/
#divisor {
  max-width: 100%;
  display: grid;
  width: 100%;
  height: auto;
  box-shadow: 0px 3px 12px 0px rgba(0, 0, 0, 0.3);
  grid-template-rows: repeat(auto-fit, minmax(6em, 1fr));
  grid-template-columns: repeat(auto-fit, minmax(22em, 2fr));
  justify-content: center;
}

.img-logos {
  /* aspect-ratio: 57/64; */
  margin: 5% auto;
  width: 30%;
  height: auto;
  justify-self: center;
  align-self: center;
}

#logo-ufma {
  margin: 5% auto;
  height: auto;
}

#logo-nca-shift {
  position: relative;
  left: 50%;
}
#logo-nca-normal {
  align-self: center;
}

/*  Sobre o software*/

.about {
  background-color: #6113c6;
  width: 100%;
  color: white;
}
#titulo-about {
  color: white;
  font-weight: 700;
}
.about-description {
  color: white;
  font-weight: 900;
  font-size: 25px;
  margin: 0px 0px 2vmin 2vmin;
}

/*  Nervo Optico*/
.optic-nerve {
  display: grid;
  grid-template-rows: repeat(auto-fit, minmax(40vmin, 2fr));
  grid-template-columns: repeat(auto-fit, minmax(23em, 2fr));
}
.optic-nerve-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
#titulo-nervo {
  font-weight: 900;
  font-size: 25px;
  margin-left: 0vmin;
}
#optic-nerve-description {
  margin-left: 0vmin;
}
.optic-nerve-text {
  flex: 1;
  flex-shrink: 1;
  margin: 0vmin 2vmin;
}

.div-nervo {
  display: flex;
  align-content: center;
  justify-content: center;
  flex: 1;
}

.optic-nerve-image {
  aspect-ratio: 88/64;
  width: clamp(10vmin, 430px, 96%);
  height: auto;
  box-shadow: 0px 3px 12px 0px rgba(0, 0, 0, 0.3);
  margin: 5px 2vmin 5px 2vmin;
  flex: 0.7;
}
@media only screen and (max-width: 799px) {
  .optic-nerve-image {
    aspect-ratio: 110/64;
    width: clamp(5vmin, 200px, 96%);
    flex: 0.95;
  }
}

/* FAQ */

.faq {
  background-color: #260b4a;
  width: 100%;
  height: auto;
  padding: 0vmin 0vmin 4vmin 0vmin;
  display: flex;
  flex-direction: column;
  box-shadow: 0px 0.2vmin 37px 0px rgba(66, 0, 255, 1);
  align-content: center;
  justify-content: center;
}

#faq-titulo {
  color: white;
  font-weight: 700;
  font-size: clamp(25px, 32px, 45px);
  margin: 1vmin auto;
  width: auto;
}

.faq-grid {
  min-width: 200px;
  width: 75%;
  color: white;
  display: grid;
  grid-template-rows: repeat(auto-fit, minmax(10em, 1fr));
  grid-template-columns: repeat(auto-fit, minmax(31ch, 1fr));
  grid-auto-columns: 20%;
  gap: 2em;
  margin: auto;
}

.faq-item {
  background-color: #0e0021;
  border-radius: 35px;
  color: #fff;
  display: flex;
  padding: clamp(1em, 2em, 3em) 2em;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.faq-question {
  font: 700 24px Montserrat, sans-serif;
  margin-bottom: 10px;
  color: #fff;
}

.faq-answer {
  font-size: clamp(12px, 1.1em, 30px);
  font-weight: 500;
  color: #fff;
  width: 200px;
}

/* PROTOCOLO */

#titulo-protocolo {
  color: black;
}

/* DETECCAO */

#titulo-deteccao {
  color: white;
}
#method-description {
  color: white;
}
.detection-method {
  background-color: #6113c6;
  width: 100%;
}

/* calculo de velocidade */

.velocity-calculation {
  width: 100%;
}
#metodo {
  color: black;
}

/* TIME */

/* TODO: TRANSFORMAR secao da equipe em display: grid e ajustar */
.team {
  background-color: #6113c6;
}

.team-content {
  display: grid;
  grid-template-rows: repeat(auto-fit, minmax(6em, 1fr));
  grid-template-columns: repeat(auto-fit, minmax(100vmin, 2fr));
  justify-content: space-between;
  align-items: center;
}

#team-description {
  padding-right: 20px;
  align-self: start;
  color: white;
  width: 79%;
  font-size: clamp(0.5em, 1em + 4px, 1.5em + 4px);
}
#titulo-equipe {
  color: white;
  margin-bottom: 0vmin;
}

.team-image {
  aspect-ratio: 2/1;
  width: clamp(90%, 95%, 95%);
  height: auto;
  padding: calc(exp(2%)) 2%;
}
</style>

#FIM CODIGO GERADO POR IA

<script>
import rodape from "../Rodape.vue";
import Landing from "./Landing.vue";
import anime from "animejs/lib/anime.es.js";

export default {
  name: "Homepage",
  components: {
    rodape,
    Landing,
  },
  created() {},
  methods: {
    /* ...mapActions(["updateSharedData"]),
    sendData() {
      this.updateSharedData({ message: "Hello from HomePage" });
      this.$router.push("/teste");
    }, */
    idNCA() {
      const divisor = document.getElementById("divisor");
      if (divisor == null) {
        return "logo-nca-normal";
      }
      this.linhasDivisor = window
        .getComputedStyle(divisor)
        .gridTemplateRows.split(" ").length;
      if (this.linhasDivisor == 2) {
        return "logo-nca-shift";
      } else {
        return "logo-nca-normal";
      }
    },
  },
  data() {
    return {
      videoURL: "",
      objAnimacao: { animar: true, y: 0, frame: {} },
      linhasDivisor: 0,
    };
  },
  mounted() {
    const animateMouse = () => {
      anime({
        targets: ".mouse-animado",
        duration: 950,
        translateY: "-7vmin",
        direction: "alternate",
        loop: true,
        easing: "cubicBezier(0.230, 1.000, 0.065, 1.005)",
        autoplay: true,
      });
    };

    // Start the animation immediately after mounting
    animateMouse();
  },
  computed: {},
  props: {},
};
</script>
