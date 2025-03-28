<template>
  <div class="frame-pagina">
    <HeaderSistema :activeIndex="2"></HeaderSistema>

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
        id="logo-nca"
      />
    </div>

    <!-- TODO: BOTAR FOTOS DO POVO E PARTICIPAÇÃO -->

    <section :class="`secao-participacao` + ` ` + `${this.lista_dados[0].tipo}`">
      <div class="div-img">
        <img class="img-pessoa" :src="this.lista_dados[0].img" />
      </div>
      <!-- TODO: TERMINAR DE FAZER LOGICA DE PREEENCHIMENTO DE DADOS-->
      <div class="textos">
        <h1 class="nome">{{ this.lista_dados[0].nome }}</h1>
        <h1 class="participacao">Participação:</h1>
        <p class="desc">{{ this.lista_dados[0].descricao }}</p>
      </div>
    </section>

    <section :class="`secao-participacao` + ` ` + `${this.lista_dados[1].tipo}`">
      <div class="div-img">
        <img class="img-pessoa" :src="this.lista_dados[1].img" />
      </div>
      <!-- TODO: TERMINAR DE FAZER LOGICA DE PREEENCHIMENTO DE DADOS-->
      <div class="textos">
        <h1 class="nome">{{ this.lista_dados[1].nome }}</h1>
        <h1 class="participacao">Participação:</h1>
        <p class="desc">{{ this.lista_dados[1].descricao }}</p>
      </div>
    </section>

    <section :class="`secao-participacao` + ` ` + `${this.lista_dados[2].tipo}`">
      <div class="div-img">
        <img class="img-pessoa" :src="this.lista_dados[2].img" />
      </div>
      <!-- TODO: TERMINAR DE FAZER LOGICA DE PREEENCHIMENTO DE DADOS-->
      <div class="textos">
        <h1 class="nome">{{ this.lista_dados[2].nome }}</h1>
        <h1 class="participacao">Participação:</h1>
        <p class="desc">{{ this.lista_dados[2].descricao }}</p>
      </div>
    </section>

    <section :class="`secao-participacao` + ` ` + `${this.lista_dados[3].tipo}`">
      <div class="div-img">
        <img class="img-pessoa" :src="this.lista_dados[3].img" />
      </div>
      <!-- TODO: TERMINAR DE FAZER LOGICA DE PREEENCHIMENTO DE DADOS-->
      <div class="textos">
        <h1 class="nome">{{ this.lista_dados[3].nome }}</h1>
        <h1 class="participacao">Participação:</h1>
        <p class="desc">{{ this.lista_dados[3].descricao }}</p>
      </div>
    </section>

    <section :class="`secao-participacao` + ` ` + `${this.lista_dados[4].tipo}`">
      <div class="div-img">
        <img class="img-pessoa" :src="this.lista_dados[4].img" />
      </div>
      <!-- TODO: TERMINAR DE FAZER LOGICA DE PREEENCHIMENTO DE DADOS-->
      <div class="textos">
        <h1 class="nome">{{ this.lista_dados[4].nome }}</h1>
        <h1 class="participacao">Participação:</h1>
        <p class="desc">{{ this.lista_dados[4].descricao }}</p>
      </div>
    </section>

    <section class="team secao">
      <h2 class="section-title" id="titulo-equipe">Equipe do NCA</h2>
      <div class="team-content">
        <p class="texto-secoes" id="team-description">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer fringilla mi a
          lorem tincidunt imperdiet. Duis ac nisl pellentesque, posuere dui eu, iaculis
          lectus. Curabitur vehicula nibh urna Morbi vulputate magna id magna tempus
          volutpat. Duis metus elit, egestas id lorem at, dictum sollicitudin nunc. Nunc a
          bibendum leo. Fusce efficitur nibh a pretium feugiat. In at facilisis ante.
          Nullam id velit sed dolor mattis fringilla. Aliquam id interdum lorem
        </p>
        <img
          alt="Imagem Time do VipLab"
          class="team-image"
          src="../../assets/Foto-NCA.png"
        />
      </div>
    </section>

    <Rodape></Rodape>
  </div>
  <!-- fim frame-pagina -->
</template>

<script>
import Rodape from "../auxiliares/Rodape.vue";
import HeaderSistema from "../auxiliares/HeaderSistema.vue";

export default {
  name: "autores",
  components: {
    HeaderSistema,
    Rodape,
  },
  created() {},
  data() {
    return {
      lista_dados: [
        {
          nome: "Luis Felipe Araujo de Oliveira",
          descricao: "Ut at ante quis urna euismod aliquam ut sit amet tellus. ",
          tipo: "tipo2",
          img: "src/assets/dummy.png",
        },
        {
          nome: "Prof. João Dalysson",
          descricao: "Ut at ante quis urna euismod aliquam ut sit amet tellus. ",
          tipo: "tipo1",
          img: "src/assets/dummy.png",
        },
        {
          nome: "Prof. Luis Rivero",
          descricao: "Ut at ante quis urna euismod aliquam ut sit amet tellus. ",
          tipo: "tipo2",
          img: "src/assets/dummy.png",
        },
        {
          nome: "Polyana Bezerra",
          descricao: "Ut at ante quis urna euismod aliquam ut sit amet tellus. ",
          tipo: "tipo1",
          img: "src/assets/dummy.png",
        },
        {
          nome: "Dr. Jorge",
          descricao: "Ut at ante quis urna euismod aliquam ut sit amet tellus. ",
          tipo: "tipo2",
          img: "src/assets/dummy.png",
        },
      ],
    };
  },
  props: {},
  methods: {},
  mounted() {},
};
</script>

<style lang="scss" scoped>
.frame-pagina {
  display: flex;
  align-items: center;
  flex-direction: column;
  gap: clamp(20px, 4vmin, 40px);
}

#divisor {
  display: flex;
  justify-content: center;
  flex-direction: row;
  align-items: center;
  gap: clamp(15vmin, 120px, 20vmin);
  align-self: stretch;
  width: 100%;
  height: clamp(80px, 15vmin, 140px);
}
@media (max-width: 575px) {
  #divisor {
    height: clamp(50px, 14vmin, 80px);
  }
}

#logo-ufma {
  height: 100%;
  align-self: stretch;
  aspect-ratio: 146.33/146.33;
}

#logo-vip {
  height: 100%;
  aspect-ratio: 150.11/105.92;
}

#logo-nca {
  height: 100%;
  align-self: stretch;
  aspect-ratio: 188.08/146.33;
}

.tipo1 {
  background-color: white;
  color: black;
}

.tipo2 {
  background: #6113c6;
  color: white;
}

.secao-participacao {
  display: flex;
  padding: 4vmin 0px;
  align-items: flex-start;
  gap: 0.5%;
  align-self: stretch;

  .div-img {
    display: flex;
    padding: 0px 1vmin;
    align-items: center;

    .img-pessoa {
      width: clamp(83px, 23vmin, 160px);
      aspect-ratio: 3/4;
    }
  }
  .textos {
    display: flex;
    height: fit-content;
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5vmin;
    flex: 1 0 0;

    .desc {
      font-size: 24px;
      width: 75%;
    }
  }
}
</style>
