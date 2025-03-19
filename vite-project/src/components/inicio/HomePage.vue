<template>
  <main class="secao-landing">
    <headerHome :activeIndex="0" />

    <div id="div-video-home">
      <video
        alt="Header background"
        class="video-background"
        preload="auto"
        autoplay
        loop
        src="../../assets/video-oftalmo.mp4"
      />
      <figure class="overlay" />
    </div>
    <div class="div-titulo">
      <h1 class="section-title" id="titulo">
        Software de Análise de Vídeos de Paralisia do Sexto Nervo Óptico
      </h1>
    </div>
    <div class="botoes">
      <ButMedio @click="fnDuvidas" texto="Como Funciona?" :ativo="true"> </ButMedio>
      <ButMedio @click="fnAcesso" texto="Fazer Análise" :ativo="true"> </ButMedio>
    </div>
  </main>
</template>

<style lang="scss" scoped>
$fonte-titulo: clamp(14px, 5.33vmin, 41px);
$height-video: 100%;

.secao-landing {
  display: flex;
  align-items: center;
  flex-direction: column;
  gap: clamp(30px, 13vmin, 100px);
  flex-shrink: 0;
  align-self: stretch;
  width: 100%;
  height: clamp(100%, 100%, 100%);
  justify-content: center;
  margin-top: 0px;
  align-self: center;
  flex-wrap: wrap;
  margin: 0px;
  max-width: 100%;
}

#div-video-home {
  width: clamp(92%, 100%, 100%);
  display: flex;
  align-self: center;
  height: 100%;
  /* margin: 5vmin 0vmin 0vmin 0vmin; */
  position: absolute;

  bottom: 0px;
  flex-wrap: wrap;
  justify-content: start;
}

.overlay {
  width: 100%;
  height: 100%;
  position: absolute;
  pointer-events: none;
  background-color: rgba(18, 18, 18.1, 0.41);
}

.video-background {
  width: 100%;
  height: $height-video;
  position: absolute;
  object-fit: cover;
  z-index: 0;
  align-self: center;
}

/* MUDAR CONTAINER PRA GRID */

.div-titulo {
  margin: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  height: auto;
  width: clamp(290px, 64ch, 100%);
  margin: 0vmin auto;
}

#titulo {
  color: #fff;
  font-weight: 600;
  font-size: $fonte-titulo;
  text-align: start;
  @media (max-width: 500px) {
    text-align: center;
  }
  width: auto;
  margin: 0vmin auto;
}

.botoes {
  display: flex;
  width: 30vmin;
  align-items: flex-start;
  flex-direction: column;
  align-items: center;
  gap: 2vmin;
  flex-shrink: 0;
  z-index: 1;
}

input {
  display: none;
}
</style>

<script>
import headerHome from "./HeaderInicio.vue";
import ButMedio from "../auxiliares/ButtonMedio.vue";

export default {
  name: "HomePage",
  components: {
    headerHome,
    ButMedio,
  },
  setup() {},
  methods: {
    fnDuvidas() {
      this.$router.push("/duvidas");
    },
    fnAcesso() {
      this.$router.push("/acesso");
    },
  },
  props: {},
  data() {
    return {};
  },
  mounted() {},
};
</script>
