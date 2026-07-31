<template>
  <div class="flex flex-col items-center gap-[clamp(20px,4vmin,40px)]">
    <HeaderSistema :activeIndex="2"></HeaderSistema>

    <div id="divisor" class="flex justify-center flex-row items-center gap-[clamp(15vmin,120px,20vmin)] self-stretch w-full h-[clamp(80px,15vmin,140px)] max-[575px]:h-[clamp(50px,14vmin,80px)]">
      <img
        src="../../../assets/logo_VIP_Lab.png"
        alt="Logo VIpLab"
        class="h-full self-stretch aspect-[150.11/105.92]"
        id="logo-vip"
      />
      <img
        src="../../../assets/logo ufma.png"
        alt="Logo UFMA"
        class="h-full self-stretch aspect-square"
        id="logo-ufma"
      />
      <img
        src="../../../assets/LogoNCAFundBranco2000_2021.png"
        alt="Logo VIpLab"
        class="h-full self-stretch aspect-[189.36/105.92]"
        id="logo-nca"
      />
    </div>

    <!-- TODO: BOTAR FOTOS DO POVO E PARTICIPAÇÃO -->

    <section :class="`flex gap-[clamp(10px,2vmin,20px)] justify-center items-start w-[min(85%,1000px)]` + ` ` + `${this.lista_dados[0].tipo}`">
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

    <section :class="`flex gap-[clamp(10px,2vmin,20px)] justify-center items-start w-[min(85%,1000px)]` + ` ` + `${this.lista_dados[1].tipo}`">
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

    <section :class="`flex gap-[clamp(10px,2vmin,20px)] justify-center items-start w-[min(85%,1000px)]` + ` ` + `${this.lista_dados[2].tipo}`">
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

    <section :class="`flex gap-[clamp(10px,2vmin,20px)] justify-center items-start w-[min(85%,1000px)]` + ` ` + `${this.lista_dados[3].tipo}`">
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

    <section :class="`flex gap-[clamp(10px,2vmin,20px)] justify-center items-start w-[min(85%,1000px)]` + ` ` + `${this.lista_dados[4].tipo}`">
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

    <section class="flex flex-col items-center gap-5 w-full px-5">
      <h2 class="section-title" id="titulo-equipe">Equipe do NCA</h2>
      <div class="flex flex-col md:flex-row items-center gap-5 w-full">
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
          src="../../../assets/Foto-NCA.png"
        />
      </div>
    </section>

    <Rodape></Rodape>
  </div>
  <!-- fim frame-pagina -->
</template>

<script>
import Rodape from "../../layout/Rodape.vue";
import HeaderSistema from "../../layout/HeaderSistema.vue";

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
          descricao: "Desenvolvedor Frontend e Backend da Aplicação",
          tipo: "tipo2",
          img: "src/assets/dummy.png",
        },
        {
          nome: "Prof. João Dalysson",
          descricao: "Professor e Orientador do projeto de ppesquisa",
          tipo: "tipo1",
          img: "src/assets/dummy.png",
        },
        {
          nome: "Prof. Luis Rivero",
          descricao: "Professor e UX Designer",
          tipo: "tipo2",
          img: "src/assets/dummy.png",
        },
        {
          nome: "Polyana Bezerra",
          descricao: "Pesquisadora principal na criação do método de diagnóstico automático da Paralisia",
          tipo: "tipo1",
          img: "src/assets/dummy.png",
        },
        {
          nome: "Dr. Jorge",
          descricao: "Médico pesquisador e Co-autor no projeto de pesquisa",
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
.tipo1 {
  background-color: white;
  color: black;
}

.tipo2 {
  background: #6113c6;
  color: white;
}
</style>
