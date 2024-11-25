<template>
  <section class="secao-landing">
    <!-- TODO: AJEITAR HEADER E SECAO INICIAL -->
    <headerHome />
    <div class="conteudo-secao">
      <div id="div-video-home">
        <!-- ADICIONAR AUTOPLAY E LOOP PRA TER O RESULTADO FINAL -->

        <video
          alt="Header background"
          class="video-background"
          preload="auto"
          autoplay
          loop
          src="../assets/video-oftalmo.mp4"
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
      <div class="div-mouse-animado">
        <img
          src="../assets/mouse-animado.png"
          alt="Mouse animado"
          class="mouse-animado"
        />
      </div>
      <div class="div-seta-baixo">
        <img src="../assets/seta-baixo.png" alt="Decorative element" class="seta-baixo" />
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
  z-index: 0;
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
.div-seta-baixo {
  margin: auto;
  align-self: center;
  width: clamp(8vmin, 45px, 70px);
  margin-top: -4vh;
  margin-bottom: clamp(0vh, 0vh, 3vh);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.seta-baixo {
  margin: auto;
  width: 100%;
}
</style>

<script>
import headerHome from "./HeaderHomepage.vue";
import db from "../db";

export default {
  name: "Landing",
  components: {
    headerHome,
  },
  setup() {},
  methods: {
    async handleFileUpload($evt) {
      console.log("UPLOAD FEITO");
      const file = $evt.target.files[0];

      if (file) {
        db.open();
        const videoData = {
          name: file.name,
          size: file.size,
          type: file.type,
          data: file, // The video file as a Blob
        };
        let constId = await db.add(videoData);
        console.log(constId + " " + typeof constId);

        alert(constId);
        this.$router.push({ name: "analiseVideo", query: { idVideoAnalise: constId } });
      }
    },
  },
  props: {},
  data() {
    return {
      _: 0,
    };
  },
  mounted() {
    // listener pra quando fileInput recebe mudança
    document.getElementById("fileInput").onchange = this.handleFileUpload;
  },
};
</script>
