<template>
  <section class="secao-landing">
    <headerHome />
    <div class="conteudo-secao">
      <div id="div-video-home">
        <video
          alt="Header background"
          class="video-background"
          preload="auto"
          autoplay
          loop
          src="../../assets/video-oftalmo.mp4"
        />
        <div class="overlay"></div>
      </div>
      <div class="div-titulo">
        <h1 class="section-title" id="titulo">
          Software de Análise de Vídeos de Paralisia do Sexto Nervo Óptico
        </h1>
      </div>
      <div class="cntr-cta">
        <input type="file" id="fileInput" accept="video/*" />
        <label for="fileInput" ref="" class="label-cta"> Analisar Vídeo </label>
      </div>
    </div>
  </section>
</template>

<style scoped>
* {
  --height-video: 100%;
}

.secao-landing {
  display: flex;
  align-items: center;
  width: 100%;
  height: var(--height-video);
  justify-content: center;
  margin-top: 0px;
  align-self: center;
  flex-wrap: wrap;
  margin: 0px;
  max-width: 100%;
}

#div-video-home {
  position: absolute;
  width: clamp(92%, 95%, 98%);
  display: flex;
  align-self: center;
  height: 100%;
  /* margin: 5vmin 0vmin 0vmin 0vmin; */
  top: 0px;
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
  height: var(--height-video);
  object-fit: cover;
  z-index: 0;
  align-self: center;
}

/* MUDAR CONTAINER PRA GRID */
.conteudo-secao {
  align-self: center;
  display: flex;
  flex-wrap: wrap;
  flex-flow: column wrap;
  width: 100%;
  height: 100vh;
  justify-content: space-between;
  align-content: center;
}

.div-titulo {
  margin: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  height: auto;
  width: clamp(290px, 59ch, 100%);
  margin: 0vmin auto;
  margin-top: clamp(10vmin, 13vmin, 17vmin);
  --fonte-titulo: clamp(14px, 5.33vmin, 41px);
}

#titulo {
  color: #fff;
  font-weight: 600;
  font-size: var(--fonte-titulo);
  text-align: start;
  width: auto;
  margin: 0vmin auto;
}

.cntr-cta {
  margin: clamp(30px, 27vmin, 165px) auto 0vmin auto;
  background-color: #6113c6;
  position: relative;
  display: flex;
  border-radius: 59px;
  align-items: center;
  justify-content: center;
  box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.59);
  padding: clamp(1px, 4px, 10px) clamp(6px, 19px, 22px);
}

.label-cta {
  border: none;
  font-size: clamp(1.5vmin, 5vmin, 22px);
  font-family: MontSerrat, Bold;
  color: #fff;
  cursor: pointer;
  width: auto;
}

input {
  display: none;
}

.div-mouse-animado {
  display: flex;
  align-items: center;
  justify-items: center;
  margin: 10vmin auto 0vmin auto;
  align-self: flex-start;
  width: clamp(2em, 7vmin, 120px);
  height: auto;
  position: relative;
}

.mouse-animado {
  width: 100%;
  height: auto;
  position: relative;
}
</style>

<script>
import headerHome from "./HeaderInicio.vue";
import db from "../../db.js";
import axios from "axios";
import mime from "mime-types";

export default {
  name: "HomePage",
  components: {
    headerHome,
  },
  setup() {},
  methods: {},
  props: {},
  data() {
    return {};
  },
  mounted() {
    // listener pra quando fileInput recebe mudança
    document.getElementById("fileInput").onchange = this.handleFileUpload;
  },
};
</script>
