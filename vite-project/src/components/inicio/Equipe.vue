<template>
  <div class="frame-pagina">
    <HeaderInicio :activeIndex="2"></HeaderInicio>
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
        <h1 class="nome">Luis Felipe Araujo de Oliveira</h1>
        <h1 class="participacao">Participação:</h1>
        <div class="desc">
          Ut at ante quis urna euismod aliquam ut sit amet tellus. Nunc molestie et lectus
          et interdum. Cras tempus varius massa convallis vulputate
        </div>
      </div>
    </section>

    <section class="secao-participacao tipo1">
      <div class="div-img">
        <img class="img-pessoa" src="..\..\assets\dummy.png" />
      </div>
      <div class="textos">
        <h1 class="nome">Prof. João Dalysson</h1>
        <h1 class="participacao">Participação:</h1>
        <div class="desc">
          Ut at ante quis urna euismod aliquam ut sit amet tellus. Nunc molestie et lectus
          et interdum. Cras tempus varius massa convallis vulputate
        </div>
      </div>
    </section>

    <section class="secao-participacao tipo2">
      <div class="div-img">
        <img class="img-pessoa" src="..\..\assets\dummy.png" />
      </div>
      <div class="textos">
        <h1 class="nome">Prof. Luis Rivero</h1>
        <h1 class="participacao">Participação:</h1>
        <div class="desc">
          Ut at ante quis urna euismod aliquam ut sit amet tellus. Nunc molestie et lectus
          et interdum. Cras tempus varius massa convallis vulputate
        </div>
      </div>
    </section>

    <section class="secao-participacao tipo1">
      <div class="div-img">
        <img class="img-pessoa" src="..\..\assets\dummy.png" />
      </div>
      <div class="textos">
        <h1 class="nome">Polyana Bezerra</h1>
        <h1 class="participacao">Participação:</h1>
        <div class="desc">
          Ut at ante quis urna euismod aliquam ut sit amet tellus. Nunc molestie et lectus
          et interdum. Cras tempus varius massa convallis vulputate
        </div>
      </div>
    </section>

    <section class="secao-participacao tipo2">
      <div class="div-img">
        <img class="img-pessoa" src="..\..\assets\dummy.png" />
      </div>
      <div class="textos">
        <h1 class="nome">Dr. Jorge</h1>
        <h1 class="participacao">Participação:</h1>
        <div class="desc">
          Ut at ante quis urna euismod aliquam ut sit amet tellus. Nunc molestie et lectus
          et interdum. Cras tempus varius massa convallis vulputate
        </div>
      </div>
    </section>

    <section class="secao-participacao tipo1">
      <div class="div-img">
        <img class="img-pessoa" src="..\..\assets\dummy.png" />
      </div>
      <div class="textos">
        <h1 class="nome">ADAddwdawdadw awd adawd</h1>
        <h1 class="participacao">Participação:</h1>
        <div class="desc">
          Ut at ante quis urna euismod aliquam ut sit amet tellus. Nunc molestie et lectus
          et interdum. Cras tempus varius massa convallis vulputate
        </div>
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
import HeaderInicio from "./HeaderInicio.vue";
import Rodape from "../auxiliares/Rodape.vue";

export default {
  name: "autores",
  components: {
    HeaderInicio,
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
          img: null,
        },
        {
          nome: "Prof. João Dalysson",
          descricao: "Ut at ante quis urna euismod aliquam ut sit amet tellus. ",
          tipo: "tipo1",
          img: null,
        },
        {
          nome: "Prof. Luis Rivero",
          descricao: "Ut at ante quis urna euismod aliquam ut sit amet tellus. ",
          tipo: "tipo2",
          img: null,
        },
        {
          nome: "Polyana Bezerra",
          descricao: "Ut at ante quis urna euismod aliquam ut sit amet tellus. ",
          tipo: "tipo1",
          img: null,
        },
        {
          nome: "Dr. Jorge",
          descricao: "Ut at ante quis urna euismod aliquam ut sit amet tellus. ",
          tipo: "tipo2",
          img: null,
        },
      ],
    };
  },
  props: {},
  methods: {
    insertParticipationSection() {
      nomeParticip.forEach((obj) => {
        const tempDiv = document.createElement("section");
        tempDiv.innerHTML = `
          <section class="secao-participacao ${obj.tipo || "tipo1"}">
            <div class="div-img">
              <img class="img-pessoa" src="${obj.img || "../../assets/dummy.png"}" />
            </div>
            <div class="textos">
              <h1 class="nome">${obj.name}</h1>
              <h1 class="participacao">Participação:</h1>
              <div class="desc">${obj.desc}</div>
            </div>
          </section>
        `;
        const newSection = tempDiv.firstElementChild;

        document.querySelector(".frame-pagina").appendChild(newSection);
      });
    },
  },
  mounted() {
    this.insertParticipationSection();
  },
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
  height: clamp(100px, 20vmin, 140px);
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
      width: 75%;
    }
  }
}
</style>
