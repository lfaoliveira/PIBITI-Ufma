
/* componente geral de video player */

<template>
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
    <!--label para estilizar butao upload -->
    <label for="fileInput" class="custom-file-upload" :style="estiloUpload">
      Upload
    </label>
    <input type="file" id="fileInput" accept="video/*" @change="handleFileUpload">
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

</template>

<script lang="js">
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
  name: "videoplayer",
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
        //true
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
        width: `${this.videoWidth}px`,
        height: `${this.videoHeight}px`,
      };
    },
    estiloUpload(){
      const height_but = 6
      const width_but = 25
      const height_text = height_but
      return {
        // COR E FONTE
        backgroundColor: `#d9d9d9`,
        borderRadius: `51px`,
        border: `none`,
        color: `black`,
        fontFamily: `"Inter-Regular", Helvetica`,
        
        //TAMANHO
        position: `relative`,
        height: `${height_but}%`,
        width: `${width_but}%`,
        //lineHeight: `${height_text*10}%`,
        
        //POSICIONAMENTO
        whiteSpace: `nowrap`,
        letterSpacing: `0`,
        border: `none`,
        alignItems: `center`,
        
        display: `flex`,
        justifyContent: `center`,
        padding: `0.15lh`,
        //marginTop: `-25px`,
        marginBottom: `10px`,
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
input[type="file"] {
  display: none;
}

.div-video{
  position: relative;
  /*display: inline-block; */

}
video {
  margin-top: 20px;
  max-width: 100%;
  max-height: 100%;
  display: flex;
  /*display: inline-block; */
  padding: 5px;
  border: 0.16rem solid rgba(85, 85, 85, 0.426);
}
</style>
