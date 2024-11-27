/* componente geral de video player TIRADO DO MDN: If you don't specify the controls
attribute, the video won't include the browser's default controls; you can create your own
custom controls using JavaScript and the #####HTMLMediaElement###### API. See Creating a
cross-browser video player for more details. To allow precise control over your video (and
audio) content, HTMLMediaElements fire many different events. In addition to providing
controllability, these events let you monitor the progress of both download and playback
of the media, as well as the playback state and position. */

<template>
  <main class="wrapper-player">
    <!-- <div class="video-container"> </div> -->
    <!-- 
    <input
      type="range"
      min="0"
      max="100"
      step="1"
      :value="percentage.toFixed(1)"
      @input="onInput"
    /> -->
    <!-- <div class="video-container">   -->
    <video
      class="video-analise"
      :src="this.videoSource"
      :muted="muted"
      :autoplay="autoplay"
      :controls="controls"
      :loop="loop"
      :poster="poster"
      :preload="preload"
      :currentTime="this.currentTime"
      ref="player"
    />
    <div ref="controles" class="controles">
      <span class="time-display" @timeupdate="this.onPlayerTimeupdate"
        >{{ this.time }} / {{ this.duration }}</span
      >

      <div class="linha-do-tempo">
        <div class="bola-slider"></div>
        <button class="slider"></button>
      </div>

      <button class="bola-play" @click="setIcone()">
        <img class="control-icon" :src="this.icone" :style="this.stylePausa" />
      </button>
    </div>
    <!-- </div>  -->
    <!-- fim controles -->
  </main>
</template>

<style scoped>
* {
  max-width: 100%;
  --tam-slider: clamp(1%, 5px, 10px);
  --alt-controles: clamp(50px, 12vmin, 170px);
  z-index: 1;
  border: none;
  margin: 0;
}

input[type="file"] {
  display: none;
}

.wrapper-player {
  display: grid;
  box-shadow: 0px 0px 0px 0.16rem rgb(0, 0, 0);
  grid-template-rows: repeat(auto-fit, 60vmin);
  grid-template-columns: repeat(auto-fit, minmax(100%, 1fr));
  margin: auto;
  /* aspect-ratio: 16/9; */
  width: clamp(90vmin, 90%, 100%);
  height: min-content;
  gap: 0px;
  margin-top: 5vmin;

  position: relative;
  /* min-height: 474px; */

  color: #fff;
  margin-bottom: 2%;
  align-self: center;
}

.video-container {
  display: flex;
  justify-content: flex-end;
  flex-direction: column;
  margin-top: 5vmin;
  border-radius: 31px;
  position: relative;
  /* min-height: 474px; */
  width: 100%;

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

  object-fit: contain;
  position: relative;
  width: max-content;

  margin: auto;

  height: calc(var(--alt-controles) + 100%);
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

/* FIM CSS DE IA */
/* .div-video{
  max-width: 100%;
  max-height: 100%;
  position: relative;
  /*display: inline-block;

} */
/* 
video {
  max-width: 100%;
  max-height: 100%;
  display: flex;
  /*display: inline-block; */
/* padding: 5px; 
  
} */

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
}

.bola-slider {
  --tam-bolinha: clamp(1.7vmin, 22px, 16px);
  width: var(--tam-bolinha);
  height: var(--tam-bolinha);
  position: absolute;
  border-radius: 100%;
  cursor: pointer;
  background-color: #fff;
  left: -0.1vmin;
  z-index: 4;
}

input[type="range"] {
  position: relative;
  top: -1px;
  overflow: hidden;
  width: 245px;
  -webkit-appearance: none;
  appearance: auto;
  background-color: #ccc;
  border-radius: 5px;
}

input[type="range"]:focus {
  outline: none;
}

input[type="range"]::-webkit-slider-runnable-track {
  height: 8px;
  -webkit-appearance: none;
  color: #333;
  margin-top: -1px;
}

input[type="range"]::-webkit-slider-thumb {
  width: 8px;
  -webkit-appearance: none;
  height: 8px;
  cursor: ew-resize;
  background: #333;
  box-shadow: -245px 0 0 245px #333;
}
</style>

<script>
import db from "../db";
import { ref, onMounted, computed } from "vue";

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
    controls: { type: Boolean, required: false, default: false },
    loop: { type: Boolean, required: false, default: true },
    autoplay: { type: Boolean, required: false, default: true },
    muted: { type: Boolean, required: false, default: true },
    poster: { type: String, required: false },
    preload: { type: String, required: false, default: "true" },
  },
  data() {
    return {
      icone: " ",
      percentage: 0,
      tempoAtual: "00:00",
      playing: true,
      duration: 0,
      time: 0,
      currentTime: 0,
      percentagePlayed: 0,
      videoSource: "  ",
      videoMuted: false,
    };
  },
  async mounted() {
    console.log("MONTADO VIDEOPLAYER:");
    this.icone = this.loadIconePlay();
    this.videoSource = await this.pegarVideo();

    //this.bindEvents();
    if (this.$refs.player.muted) {
      this.setMuted(true);
    }
    /* const video = this.$refs.player;
    const altVideo = window.getComputedStyle(video).getPropertyValue("height");
    const controles = this.$refs.controles;
    const altControles = window.getComputedStyle(controles).getPropertyValue("height");

    let bottom = parseFloat(altControles) / 2;
    this.$refs.controles.style.bottom = `calc(${bottom}px + 5vmin)`; */
  },

  methods: {
    onInput(e) {
      console.log("INPUT no slider");
      this.$emit("seek", e.target.value);
    },

    onPlayerPlay({ event, player }) {
      console.log(event.type);
      player.setPlaying(true);
    },
    onPlayerPause({ event, player }) {
      console.log(event.type);
      player.setPlaying(false);
    },
    onPlayerEnded({ event, player }) {
      console.log(event.type);
      player.setPlaying(false);
    },
    onPlayerLoadeddata({ event }) {
      console.log(event.type);
    },
    onPlayerWaiting({ event }) {
      console.log(event.type);
    },
    onPlayerPlaying({ event }) {
      console.log(event.type);
    },
    onPlayerTimeupdate({ event }) {
      this.time = `${event.target.currentTime}`;
      console.log({ event: event.type, time: event.target.currentTime });
    },
    onPlayerCanplay({ event }) {
      console.log(event.type);
    },
    onPlayerCanplaythrough({ event }) {
      console.log(event.type);
    },
    playerStateChanged({ event }) {
      console.log(event.type);
    },

    onVoltar() {
      this.$router.push("/");
    },
    async pegarVideo() {
      try {
        await db.open();

        const videoData = await db.get(parseInt(this.idVideoAtual));
        const url = URL.createObjectURL(videoData.data);
        return url;
      } catch (error) {
        console.error("ERRO! " + error);
      }
    },
    setIcone() {
      this.togglePlay();
      this.icone = this.loadIconePlay();
    },
    loadIconePlay() {
      if (this.playing) {
        return "src/assets/pause.svg";
      } else {
        return "src/assets/play.svg";
      }
    },
    bindVideoEvent(which) {
      const player = this.$refs.player;

      player.addEventListener(which, (event) => {
        if (which === "loadeddata") {
          this.duration = player.duration;
        }
        if (which === "timeupdate") {
          this.percentagePlayed = (player.currentTime / player.duration) * 100;
        }
        this.$emit(which, { event, player: this });
      });
    },
    bindEvents() {
      console.log("BINDING");

      EVENTS.forEach((event) => {
        this.bindVideoEvent(event);
      });
    },
    setMuted(state) {
      this.videoMuted = state;
    },
    setPlaying(state) {
      this.playing = state;
    },
    seekToPercentage(percentage) {
      this.$refs.player.currentTime = (percentage / 100) * this.duration;
    },
    play() {
      this.$refs.player.play();
      this.setPlaying(true);
    },

    pause() {
      this.$refs.player.pause();
      this.setPlaying(false);
    },

    togglePlay() {
      if (this.playing) {
        this.pause();
      } else {
        this.play();
      }
    },

    convertTimeToDuration(seconds) {
      let decimal = parseInt(Number(seconds / 60) % 60, 10);
      let uni = parseInt(seconds % 60, 10);
      return [decimal, uni].join(":").replace(/\b(\d)\b/g, "0$1");
    },

    toggleMute() {
      if (this.videoMuted) {
        this.$refs.player.muted = false;
        this.setMuted(false);
      } else {
        this.$refs.player.muted = true;
        this.setMuted(true);
      }
    },
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
    styleControles() {
      const video = this.$refs.player;
      if (!video) {
        return { top: "0px" };
      }

      const altVideo = window.getComputedStyle(video).getPropertyValue("height");
      const controles = this.$refs.controles;
      const altControles = window.getComputedStyle(controles).getPropertyValue("height");

      let top = parseFloat(altVideo) + parseFloat(altControles) / 2;
      console.log(top);
      return {
        top: `${top}px`,
      };
    },
  },
};
</script>
