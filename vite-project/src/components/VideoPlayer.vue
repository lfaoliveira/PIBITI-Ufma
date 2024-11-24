
/* componente geral de video player */

<template>
  <main>
    <section class="video-demo">
      <div class="video-container">
        <img class="video-thumbnail" alt="Video thumbnail" src="https://cdn.builder.io/api/v1/image/assets/TEMP/c55bdb6a7ebf3b86f87fc14c7107afda5ac8eb148fe8c57ff3b1ff1f32422e76?placeholderIfAbsent=true&apiKey=8b29090e827e422ea4601ed102c7c8ec"/>
        <videocontrols :percentage="0" class="video-controls"> </videocontrols>
      </div>
    </section>

    <div class="div-video">
      <video
        :src="this.videoSource"
        :muted="muted"
        :autoplay="autoplay"
        :controls="controls"
        :loop="loop"
        :width="width"
        :height="height"
        :poster="poster"
        :preload="preload"
        :style="videoStyle"
        ref="player"
      />

      <slot
        name="controls"
        :play="play"
        :pause="pause"
        :toggle-play="togglePlay"
        :playing="playing"
        :percentage-played="percentagePlayed"
        :seek-to-percentage="seekToPercentage"
        :duration="duration"
        :convert-time-to-duration="convertTimeToDuration"
        :video-muted="videoMuted"
        :toggle-mute="toggleMute"
      ></slot>
    </div>
  </main>
</template>

<style scoped>

*{
  max-width: 100%;
}

.video-demo {
  width: 75%;
  border-radius: 0;
  display: flex;
  flex-direction: column;
  color: #fff;
  margin-bottom: 2%;
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
  width: 31px;
  border-radius: 0;
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

input[type="file"] {
  display: none;
}

.div-video{
  max-width: 100%;
  max-height: 100%;
  position: relative;
  /*display: inline-block; */

}
video {
  max-width: 100%;
  max-height: 100%;
  display: flex;
  /*display: inline-block; */
  /* padding: 5px; */
  border: 0.16rem solid rgba(85, 85, 85, 0.426);
}
</style>


<script>
const VIDEO_RATIO = 0.7

import videocontrols from "./VideoControls.vue";
import { useStore } from "vuex/dist/vuex.cjs.js";

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
  
  name: "Videoplayer",
  components: {
    videocontrols,
  },
  props: {
    controls: { type: Boolean, required: false, default: false },
    loop: { type: Boolean, required: false, default: false },
    width: { type: Number, required: false},
    height: { type: Number, required: false },
    autoplay: { type: Boolean, required: false, default: false },
    muted: { type: Boolean, required: false, default: false },
    poster: { type: String, required: false },
    preload: { type: String, required: false, default: "auto" },
  },
  data() {
    return {
      playing: true,
      duration: 0,
      percentagePlayed: 0,
      source: "",
      videoMuted: false,
      videoWidth: window.innerWidth * VIDEO_RATIO,
      videoHeight: window.innerHeight * VIDEO_RATIO,
    };
  },
  mounted() {
    console.log("BINDING:");
    
    //this.bindEvents();
    if (this.$refs.player.muted) {
      this.setMuted(true);
    }
  },
  methods: {
    loadIconePlay(){
      if (this.playing){
        return "../assets/play.svg"
      }
      else{
        return "../assets/pause.svg"
      }

    },
    resizeVideo() {
      const aspectRatio = 16 / 9; // Assuming a standard aspect ratio of 16:9
      const maxWidth = window.innerWidth * VIDEO_RATIO; // % of the window width
      const maxHeight = window.innerHeight * VIDEO_RATIO; // % of the window height
      if (maxWidth / aspectRatio <= maxHeight) {
        this.videoWidth = maxWidth;
        this.videoHeight = maxWidth / aspectRatio;
      } else {
        this.videoHeight = maxHeight;
        this.videoWidth = maxHeight * aspectRatio;
      }
    },

    bindEvents() {
      console.log("BINDING");

      EVENTS.forEach((event) => {
        this.bindVideoEvent(event);
      });
    },
    bindVideoEvent(which) {
      const player = this.$refs.player;

      player.addEventListener(
        which,
        (event) => {
          if (which === "loadeddata") {
            this.duration = player.duration;
          }
          if (which === "timeupdate") {
            this.percentagePlayed = (player.currentTime / player.duration) * 100;
          }
          this.$emit(which, { event, player: this });
        },
      );
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

    setPlaying(state) {
      this.playing = state;
    },

    seekToPercentage(percentage) {
      this.$refs.player.currentTime = (percentage / 100) * this.duration;
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

    setMuted(state) {
      this.videoMuted = state;
    },
    
  },
  computed: {
    videoSource(){
      const store = useStore(); 
      
      
      return store.getters.getVideoURL;
    },
    videoStyle() {
      return {
        backgroundColor: `#000`,
        width: `${this.videoWidth}px`,
        height: `${this.videoHeight}px`,
      };
    },
    estiloUpload(){
      const height_but = 6 // vmin
      const width_but = 10
      const height_text = height_but
      return {
        // COR E FONTE
        backgroundColor: `#43C3DD`,
        borderRadius: `51px`,
        border: `none`,
        color: `black`,        
        //TAMANHO
        position: `relative`,
        height: `${4}vmin`,
        width: `${12}vmin`,

        //POSICIONAMENTO
        whiteSpace: `nowrap`,
        letterSpacing: `0`,
        alignItems: `center`,
        display: `flex`,
        justifyContent: `center`,
        marginBottom: `1.2vh`,
        marginTop: `1vh`,
        textAlign: `center`,
      }
    },

  },
  mounted() {
    window.addEventListener('resize', this.resizeVideo);
    this.bindEvents();
    
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeVideo);
  },
};
</script>

