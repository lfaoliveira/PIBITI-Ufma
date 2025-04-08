<!-- PARTE GERADA POR IA -->

<template>
  <HeaderSistema :activeIndex="5" />
  <main class="analysis-view">
    <h1 class="page-title">Análise de Paralisia</h1>

    <div class="analysis-grid">
      <div class="diagnosis-card">
        <h2 class="diagnostico texto-diag">Diagnóstico: {{ this.olho_doente }}</h2>
        <p class="dif-velocidade texto-diag">
          Diferença de Velocidade: {{ this.percentDif }} %
        </p>
        <p class="velocidade-dir texto-diag">Olho Direito: {{ this.velD }} mm/s</p>
        <p class="velocidade-esq texto-diag">Olho Esquerdo: {{ this.velE }} mm/s</p>
      </div>
      <div class="div-grafico">
        <!-- Placeholder for your graph (image or canvas) -->
        <img ref="imgGraf" class="grafico" alt="Analysis graph" />
      </div>
    </div>
    <VideoPlayer
      v-if="resPronto"
      :videoSource="this.videoSource"
      :mimeVideo="this.mimeVideo"
    ></VideoPlayer>
    <Rodape class="rodape"></Rodape>
  </main>
</template>

<script>
import seta from "../icons/Voltar.vue";
import Rodape from "../auxiliares/Rodape.vue";
import VideoPlayer from "./VideoPlayer.vue";
import HeaderSistema from "../auxiliares/HeaderSistema.vue";

export default {
  // COMPONENTE QUE VAI IMPORTAR COMPONENTES DE ANALISE
  name: "Analise de Video",
  components: {
    VideoPlayer,
    Rodape,
    HeaderSistema,
  },
  created() {},
  data() {
    return {
      videoSource: "",
      graficoURL: "",
      mimeVideo: "",
      resPronto: false,
      olho_doente: "",
      percentDif: "",
      velD: "",
      velE: "",
    };
  },
  props: {
    idVideoAnalise: "",
  },
  methods: {
    addFocusClass() {
      // Manually add the 'focus' class to the label
      const label = document.querySelector(".custom-file-upload");
      label.classList.add("focus");
    },
    removeFocusClass() {
      // Manually remove the 'focus' class from the label
      const label = document.querySelector(".custom-file-upload");
      label.classList.remove("focus");
    },

    // pegar resultados da análise
    async getAnalysisResults() {
      try {
        alert(this.idVideoAnalise);
        // caso seja video de demonstracao
        if (parseInt(this.idVideoAnalise) === -1) {
          const mime = "video/mp4";
          const videoURL = VIDEO_DEMO_URL;
          const graficoURL = GRAF_DEMO_url;
          const strResult = STR_RESULT_DEMO;
          return { strResult, graficoURL, mime, videoURL };
        }
        await db.open();
        const resultData = await db.get(parseInt(this.idVideoAnalise));
        const mime = resultData.mimeVideo;
        const videoURL = resultData.video;
        const graficoURL = resultData.grafico;
        const strResult = resultData.string;

        return { strResult, graficoURL, mime, videoURL };
      } catch (error) {
        console.error("ERRO! " + error);
      }
    },
    parseResult(string) {
      const split = String(string).split(",");
      this.velE = parseFloat(split[0]).toFixed(2);
      this.velD = parseFloat(split[1]).toFixed(2);
      this.percentDif = parseFloat(split[2]).toFixed(2);
      const diag = split[3];
      let texto = "";
      if (diag === "None") {
        texto = "Olhos Saudáveis";
      } else {
        texto = "Olho " + diag + " Possivelmente Doente";
      }
      this.olho_doente = texto;
    },
  },
  computed: {
    controlStyle() {
      return {
        height: `${videoplayer.videoHeight / window.innerHeight}%`,
        width: `${videoplayer.videoWidth / window.innerWidth}%`,
      };
    },
    estiloUpload() {
      return {
        // COR E FONTE
        borderRadius: `51px`,
        border: `none`,
        color: `black`,
        //TAMANHO
        position: `relative`,
        //POSICIONAMENTO
        whiteSpace: `nowrap`,
        letterSpacing: `0`,
        alignItems: `center`,
        display: `flex`,
        justifyContent: `center`,
        textAlign: `center`,
      };
    },
  },
  async mounted() {
    console.log("MONTADO ANALISE:");
    const res = await this.getAnalysisResults();
    this.resPronto = true;
    this.videoSource = res.videoURL;
    this.mimeVideo = res.mime;
    console.log("MIME: ANALI", this.mimeVideo);
    this.graficoURL = res.graficoURL;
    this.$refs.imgGraf.src = this.graficoURL;
    const strResult = res.strResult;
    this.parseResult(strResult);
  },
};
</script>

<style scoped>
* {
  max-width: 100vmax;
  font-family: Montserrat, "Inter";
}

.texto-diag {
  --fonte-diag: clamp(10px, 15px, 20px);
  font-size: var(--fonte-diag);
  margin: clamp(3%, 20px, 50px) 4%;
}

.responsive-container {
  width: 97%;
  display: flex;
  flex-wrap: wrap; /* Allows the items to wrap to the next line */
  gap: 20px;
}

.div-grafico {
  display: flex;
  /* Minimum width before breaking */
  width: clamp(100%, 100%, 100%); /* Make the image responsive */
  border-radius: 10px;
  box-shadow: 0 0px 7px rgba(0, 0, 0, 0.5);
}

.grafico {
  object-fit: contain;
  width: clamp(100%, 100%, 100%);
}
.video-exemplo {
  width: 100%;
  height: 50%;
}

.analysis-view {
  width: clamp(100%, 100%, 100%);
  background-color: #fff;
  /* box-shadow: 0 0 5px 4px rgba(0, 0, 0, 0.34); */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-title {
  color: #3a0d75;
  font-size: clamp(35px, 52px, 70px);
  margin: clamp(30px, 6vmin, 120px) auto 0px auto;
}

.analysis-grid {
  --tam-grid: 97%;
  display: grid;
  grid-template-rows: repeat(auto-fill, minmax(40vmin, 2fr));
  grid-template-columns: repeat(auto-fit, minmax(85vmin, 2fr));
  gap: clamp(2%, 20px, 4vmin);
  width: var(--tam-grid);
  margin-top: 2%;
}

.diagnosis-card {
  border-radius: 13px;
  background-color: #fff;
  box-shadow: 0 0 5px 4px rgba(0, 0, 0, 0.21);
  padding: 22px 32px 37px;
  color: #6113c6;
  font-size: clamp(5px, 14px, 20px);
  width: clamp(200px, 100vmin, 100%);
  flex: 0.3;
  display: flex;
  flex-direction: column;
  justify-self: center;
}

.diagnostico {
  color: #38d200;
  font-size: calc(var(--fonte-diag) + 15%);
}

.custom-file-upload {
  background-color: #43c3dd;
  --butao-height: 6vmin;
  --butao-width: 30vmin;
  height: clamp(4rem, var(--butao-height), 6rem);
  width: clamp(6rem, var(--butao-width), 10rem);
  font-size: clamp(2rem, 4vmin, 6rem);
}

.custom-file-upload:focus {
  background-color: #ffffff;
  height: clamp(4vmin + 1vmin, var(--butao-height) + 2 vmin, var(--butao-height) + 4vmin);
  width: clamp(6rem, var(--butao-width), 10rem);
  font-size: clamp(2rem, 4vmin, 6rem);
}

.custom-file-upload:hover {
  background-color: #39abc2;
  --butao-height: 8vmin;
  --butao-width: 30vmin;
  height: clamp(2vmin + 4vmin, var(--butao-height) + 4vmin, var(--butao-height) + 12vmin);
  width: clamp(6rem, var(--butao-width), 10rem);
  font-size: clamp(3vmin, 5vmin, 7vmin);
}

CSS ORIGINAL .edicaoVideo {
  font-family: "Roboto Serif", serif !important;
}
.setaClasse {
  position: absolute;
  aspect-ratio: 4/3;
  top: 0.2vmin;
  left: 5vmin;
}
.videoplayer {
  display: grid;
  width: 100%;
  height: 100%;
}
button {
  font-family: "Roboto Serif", serif !important;
}

.videoplayer-controls {
  display: block flex;
  width: 80%;
  height: 80%;
}

.videoplayer-controls-toggleplay,
.videoplayer-controls-togglemute {
  background-color: #43c3dd;
  border-radius: 51px;
  color: #001b2c;
  position: relative;
  height: 1.5em;
  width: 6em;
  white-space: nowrap;
  line-height: normal;
  display: flex;
  left: 0;
  justify-content: center;

  flex-shrink: 1;
  border: none;
}

.videoplayer-controls-toggleplay {
  margin-right: 20px;
}

.videoplayer-controls-time {
  text-align: left;
  font-weight: 400;
  line-height: 2;
  color: #001b2c;
  margin-right: 1rem;
  width: 20%;
}

.videoplayer-controls-track {
  line-height: 2;
  margin-right: 1rem;
}

.rodape {
  margin-top: clamp(20px, 6vmin, 5rem);
}
</style>
