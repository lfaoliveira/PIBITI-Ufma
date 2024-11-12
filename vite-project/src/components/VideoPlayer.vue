
/* componente geral de video player */

<template>
  
  <section class="video-demo">
    <div class="video-container">
      <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/c55bdb6a7ebf3b86f87fc14c7107afda5ac8eb148fe8c57ff3b1ff1f32422e76?placeholderIfAbsent=true&apiKey=8b29090e827e422ea4601ed102c7c8ec" alt="Video thumbnail" class="video-thumbnail" />
      <div class="video-controls">
        <span class="time-display">00:00</span>
        <div class="progress-indicator"></div>
        <img alt="ICONE PLAY" class="control-icon" src="https://cdn.builder.io/api/v1/image/assets/TEMP/fc26523d69cd2e893ce066b39edd92af909bf86c844b1ccb3bb4e63e02f6869f?placeholderIfAbsent=true&apiKey=8b29090e827e422ea4601ed102c7c8ec"/>
      </div>
    </div>
  </section>
<!--   
  <div class="div-video">
    <video
      :src="videoURL"
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
  </div> -->

</template>

<script>

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
const VIDEO_RATIO = 0.7

export default {
  
  name: "Videoplayer",
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
      videoMuted: false,
      videoURL: '',
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
    handleFileUpload($evt){
      console.log("UPLOAD FEITO")
      const file = $evt.target.files[0];
      if (file) {
        this.videoFile = file;
        this.videoURL =  URL.createObjectURL(this.videoFile) // filename = path relativo
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
      console.log("BINDING")

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

<style scoped>

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
  flex-direction: column;
  border-radius: 31px;
  position: relative;
  min-height: 474px;
  width: 100%;
  padding-top: 132px;
}

.video-thumbnail {
  position: absolute;
  inset: 0;
  height: 100%;
  width: 100%;
  object-fit: cover;
  object-position: center;
}

.play-button {
  position: relative;
  align-self: center;
  width: 136px;
  height: 93px;
  border: 5px solid #ed1818;
}

.video-controls {
  position: relative;
  display: flex;
  margin-top: 186px;
  width: 100%;
  flex-direction: column;
  align-items: flex-start;
  padding: 4px 80px 4px 0;
}

.progress-indicator {
  background-color: #d9d9d9;
  border-radius: 50%;
  width: 10px;
  height: 11px;
  margin-top: 5px;
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
    max-width: 100%;
    padding-top: 100px;
    white-space: initial;
  }

  .video-controls {
    max-width: 100%;
    padding-right: 20px;
    margin-top: 40px;
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
