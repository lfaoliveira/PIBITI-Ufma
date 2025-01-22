<template>
  <main class="wrapper-player">
    <!-- @loadedmetadata="getLoadedVideo" -->
    <!-- <video
      class="video-js vjs-custom-skin"
      preload="auto"
      :src="videoSource"
      :muted="muted"
      :autoplay="autoplay"
      :controls="controls"
      :loop="loop"
      ref="videoplayer"
    /> -->
    <video ref="videoTeste" width="600" controls>
      <source :src="videoSource" type="video/mp4" />
      Your browser does not support the video tag.
    </video>
    <img ref="imgGraf" />
  </main>
</template>

<style>
* {
  max-width: 100%;
  --tam-slider: clamp(1%, 5px, 10px);
  --alt-controles: clamp(50px, 12vmin, 170px);
  border: none;
  margin: 0;
}

/* OBS: UTILIZAR especificidade ao mudar estilo do CSS do video.js */

/*  */

.vjs-custom-skin {
  /* Custom styles here */
}

.video-js .vjs-control-bar {
  /* height: clamp(5em, 100px, 15em); */
  background: linear-gradient(
    180deg,
    rgba(95, 95, 95, 0.66) 0%,
    rgba(33, 33, 33, 0.85) 39%,
    rgba(17, 0, 0, 1) 97%
  );
}
.video-js .vjs-play-control {
  background-color: #fff;
  color: #6113c6;
  border-radius: 100%;
  --tam-bola: clamp(7vmin, 40px, 50px);
  display: flex;
  aspect-ratio: 21/15;
}

.video-js .vjs-mute-control {
  color: #fff;
  margin-left: 1vmin;
}

.video-js[tabindex="-1"] {
  height: clamp(100%, 100%, 100%);
  width: clamp(100%, 100%, 100%);
}
/* COMEÇAR A MODIFICAR CSS DO VIDEO.JS */

.video-js .vjs-control-bar {
  display: flex;
}

/* .vjs-button > .vjs-icon-placeholder::before{
  font-size: 1.8em;
} */

input[type="file"] {
  display: none;
}

.wrapper-player {
  box-shadow: 0px 0px 0px 0.05rem rgb(0, 0, 0);
  grid-template-rows: repeat(auto-fit, 60vmin);
  grid-template-columns: repeat(auto-fit, minmax(100%, 1fr));
  margin: auto;
  /* aspect-ratio: 16/9; */
  width: clamp(90vmin, 90%, 100%);
  height: clamp(20em, 450px, 91vmin);
  gap: 0px;
  margin-top: 5vmin;
  position: relative;
  /* min-height: 474px; */

  color: #fff;
  margin-bottom: 2%;
  align-self: center;
}

/* .video-thumbnail {
  position: absolute;

  z-index: 0;
  height: 100%;
  width: 100%;
  object-fit: cover;
  object-position: center;
} */

.control-icon {
  aspect-ratio: 0.94;
  object-fit: contain;
  object-position: center;
  border-radius: 0;
  pointer-events: all;
  cursor: pointer;
}

.video-analise {
  inset: 0;
  border: none;
  position: relative;
  object-fit: contain;
  width: auto;
  height: calc(var(--alt-controles) + 100%);
  aspect-ratio: 19/9;

  margin: auto;
}

@media (max-width: 991px) {
  .video-demo {
    white-space: initial;
  }

  .video-container {
    padding-top: 100px;
    white-space: initial;
  }

  .video-controls {
    white-space: initial;
  }
}

.controles {
  display: flex;
  flex-direction: column;
  background: linear-gradient(
    180deg,
    rgba(95, 95, 95, 0.66) 0%,
    rgba(33, 33, 33, 0.85) 39%,
    rgba(17, 0, 0, 1) 97%
  );

  height: var(--alt-controles);
  position: relative;
  margin: 0px;
}

.time-display {
  font-size: clamp(8px, 12px, 15px);
  position: relative;

  /* top: clamp(10px, 15px, 20px);  */
}

.bola-play {
  --tam-bola: clamp(7vmin, 40px, 50px);
  display: flex;
  aspect-ratio: 21/15;
  width: var(--tam-bola);
  /* height: var(--tam-bola); */
  background-color: #fff;
  margin: 2vmin 0px 2vmin 0.4vmin;
  justify-content: center;
  align-items: center;
  border-radius: 100%;
  cursor: pointer;
}

.linha-do-tempo {
  display: flex;
  justify-content: center;
  height: fit-content;
  flex-direction: column;
  margin-top: 1vmin;
}

.slider {
  background-color: rgba(255, 255, 255, 0.72);
  width: 100%;
  height: clamp(3px, 7px, 10px);
  cursor: pointer;
}

.bola-slider {
  --tam-bolinha: clamp(1.7vmin, 22px, 16px);
  width: var(--tam-bolinha);
  height: var(--tam-bolinha);
  position: absolute;
  border-radius: 100%;

  background-color: #fff;
  left: -0.1vmin;
  z-index: 4;
  cursor: pointer;
}
</style>

<script>
import db from "../db.js";
import videojs from "video.js";
import "video.js/dist/video-js.css";
import { Buffer } from "node:buffer";
// eventos pro player checar durante execução
const EVENTS = [
  "play",
  "pause",
  "ended",
  "loadeddata",
  "waiting",
  "playing",
  "timeupdate",
  "canplay",
  "canplaythrough",
  "statechanged",
];

export default {
  name: "Player_de_Video",
  // TODO: INSERIR LOGICA DE ADAPTAR TAMANHO DO WRAPPER COM BASE NO ASPECT-RATIO DO VIDEO
  props: {
    idVideoAtual: { type: String, required: true, default: "" },
    controls: { type: Boolean, default: true },
    loop: { type: Boolean, default: true },
    autoplay: { type: Boolean, default: false },
    muted: { type: Boolean, default: true },
    preload: { type: String, default: "false" },
  },
  components: {},
  data() {
    return {
      videoSource: "",
    };
  },
  async mounted() {
    console.log("MONTADO VIDEOPLAYER:");
    const res = await this.pegarVideo();
    this.videoSource = res.videoURL;

    const mimeVideo = res.mime;
    this.graficoURL = res.graficoURL;
    this.$refs.imgGraf.src = this.graficoURL;
    this.strResult = res.strResult;

    /* const tiposSuport = ["mp4", "ogg", "webm", "mkv", "avi"];
    
    // itera sobre tipos aceitaveis e cria array de fontes
    tiposSuport.forEach((tipo) => {
      console.log(tipo);
      const mimeAtual = mime.lookup(tipo);
      sources.push({ src: videoSource, type: `${mimeAtual}` });
    }); */

    const sources = [{ src: this.videoSource, type: `${mimeVideo}` }];
    this.setupPlayer(sources);
  },

  methods: {
    setupPlayer(sources) {
      //Funcao que faz setup inicial do videoplayer usando dados do VideoPlayer.vue
      this.player = videojs(this.$refs.videoplayer, {
        sources: sources,
      });
    },

    onVoltar() {
      this.$router.push("/");
    },
    async pegarVideo() {
      try {
        await db.open();

        const resultData = await db.get(parseInt(this.idVideoAtual));
        const mime = resultData.mimeVideo;

        const videoURL = this.base64ToURL(resultData.video, mime);
        console.log(`VIDEO URL: ${videoURL}`);
        const graficoURL = this.base64ToURL(resultData.grafico, "image/jpg");
        const strResult = resultData.string;

        return { strResult, graficoURL, mime, videoURL };
      } catch (error) {
        console.error("ERRO! " + error);
      }
    },
    base64ToURL(base64String, mimeType) {
      // Decode the Base64 string
      try {
        const buffer = Buffer.from(base64String, "base64"); // Remove metadata part
        //const url = URL.createObjectURL(blob);
        const url = `data:${mimeType};base64,${buffer.toString("base64")}`;
        return url;
      } catch (error) {
        console.error("Error decoding Base64 string:", error);
        return null;
      }
    },
  },
  beforeDestroy() {
    if (this.player) {
      this.player.dispose();
    }
  },
  computed: {
    stylePausa() {
      /*FUNCAO que estiliza play e pause  */
      // so funiona porque nao acessa DOM diretamente. ver docs
      if (this.playing) {
        return {
          padding: `0%`,
          width: `clamp(1vmin, 22px + 3px, 100%)`,
        };
      } else {
        return {
          padding: `12%`,
          width: `clamp(1vmin, 25px, 100%)`,
        };
      }
    },
  },
};
</script>
