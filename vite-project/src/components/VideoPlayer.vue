/* componente geral de video player */

<template>
  <main class="wrapper-player">
    <section class="video-demo">
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
      <div class="video-container">
        <video
          class="video-analise"
          :src="this.videoSource"
          :muted="muted"
          :autoplay="autoplay"
          :controls="controls"
          :loop="loop"
          :poster="poster"
          :preload="preload"
          ref="player"
        />
        <div class="controles">
          <span class="time-display" @timeupdate="this.onPlayerTimeupdate">{{
            this.time
          }}</span>
          <button class="slider"></button>
          <div class="bola-slider"></div>
          <button class="bola-play" @click="setIcone()">
            <img class="control-icon" :src="this.icone" :style="this.stylePausa" />
          </button>
        </div>
      </div>
      <!-- fim controles -->
    </section>
  </main>
</template>

<style scoped>
* {
  max-width: 100%;
  --tam-slider: clamp(1%, 5px, 10px);
  z-index: 1;
  border: none;
  margin: 0;
}

input[type="file"] {
  display: none;
}

.wrapper-player {
  display: flex;
  justify-content: center;
  align-content: center;
  margin: auto;
  width: 90%;
}

.video-demo {
  width: 100%;
  border-radius: 0;
  display: flex;
  flex-direction: column;
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
  min-height: 474px;
  width: 100%;
}

.video-thumbnail {
  position: absolute;
  inset: 0;
  z-index: 0;
  height: 100%;
  width: 100%;
  object-fit: cover;
  object-position: center;
}

.control-icon {
  aspect-ratio: 0.94;
  object-fit: contain;
  object-position: center;
  border-radius: 0;

  pointer-events: all;
  cursor: pointer;
}

.video-analise {
  border: none;
  width: 100%;
  height: 100%;
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

video {
  max-width: 100%;
  max-height: 100%;
  display: flex;
  /*display: inline-block; */
  /* padding: 5px; */
  border: 0.16rem solid rgba(85, 85, 85, 0.426);
}

.controles {
  background: linear-gradient(
    180deg,
    rgba(95, 95, 95, 0.66) 0%,
    rgba(33, 33, 33, 0.85) 39%,
    rgba(17, 0, 0, 1) 97%
  );
  height: clamp(2vmin, 101px, 150px);
  position: relative;
}

.time-display {
  font-size: clamp(8px, 12px, 15px);
  position: relative;
  top: clamp(10px, 15px, 20px);
}

.bola-play {
  --tam-bola: clamp(3%, 38px, 40px);
  display: flex;
  width: var(--tam-bola);
  height: var(--tam-bola);
  background-color: #fff;
  margin: -1vmin 0 0vmin 0.7vmin;
  justify-content: center;
  border-radius: 100%;
  cursor: pointer;
}

.slider {
  background-color: rgba(255, 255, 255, 0.72);
  width: 100%;
  height: var(--tam-slider);
}

.bola-slider {
  --tam-bolinha: clamp(1.6vmin, 12px, 16px);
  width: var(--tam-bolinha);
  height: var(--tam-bolinha);
  background-color: #ccc;
  position: relative;
  top: clamp(
    -11px - var(--tam-slider) / 2,
    -20px - var(--tam-slider) / 2,
    -30px - var(--tam-slider) / 2
  );
  border-radius: 100%;
  cursor: pointer;
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
      this.time = event.target.currentTime;
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
