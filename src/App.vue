<template>

  <h1> Bem-vindo!</h1>

  <menuInicial />

  <div class="app" :style="appStyle">
    <videoplayer
      class="videoplayer"
      :muted="false"
      :autoplay="true"
      :controls="false"
      :loop="false"
      @play="onPlayerPlay"
      @pause="onPlayerPause"
      @ended="onPlayerEnded"
      @loadeddata="onPlayerLoadeddata"
      @waiting="onPlayerWaiting"
      @playing="onPlayerPlaying"
      @timeupdate="onPlayerTimeupdate"
      @canplay="onPlayerCanplay"
      @canplaythrough="onPlayerCanplaythrough"
      @statechanged="playerStateChanged"
    >
      <template
        v-slot:controls="{
          togglePlay,
          playing,
          percentagePlayed,
          seekToPercentage,
          duration,
          convertTimeToDuration,
          videoMuted,
          toggleMute,
        }"
      >
        <div class="videoplayer-controls">
          <button @click="togglePlay()" class="videoplayer-controls-toggleplay">
            {{ playing ? "pause" : "play" }}
          </button>
          <div class="videoplayer-controls-time">
            {{ convertTimeToDuration(time) }} /
            {{ convertTimeToDuration(duration) }}
          </div>
          <videoplayer-track
            :percentage="percentagePlayed"
            @seek="seekToPercentage"
            class="videoplayer-controls-track"
          ></videoplayer-track>
          <button @click="toggleMute()" class="videoplayer-controls-togglemute">
            {{ videoMuted ? "unmute" : "mute" }}
          </button>
        </div>
      </template>
    </videoplayer>
  </div>
</template>

<script>
import videoplayer from "./components/VideoPlayer.vue";
import videoplayerTrack from "./components/VideoPlayerTracker.vue";
import menuInicial from "./components/MenuInicial.vue";

export default {
  components: {
    videoplayer,
    videoplayerTrack,
    menuInicial,
  },
  data() {
    return {
      time: 0,
    };
  },
  methods: {
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
  },
  computed: {
    appStyle() {
      return {
        height: `${videoplayer.videoHeight + 1000}px`,
        width: `${videoplayer.videoWidth + 1000}px`,
      };
    },
  },
};
</script>

<style scoped>
h1 {
  font-family: "Inter-Regular", Helvetica;
  font-size: 3rem;
  color: #004abc;
  line-height: 1;
  display: flex;
  position: absolute;
  top: 0rem;
  /* Stick to the top */
  left: 0em;
  /* Align to the left */
  justify-content: center;
  align-items: center;
  /* Horizontal center */
  /*  width: 50rem; Full width to cover the entire page width     */
  height: 4rem;
  width: 100%;
  flex: 1;
  margin-top: 1.5vh;
  background-color: rgb(0, 0, 0);
}

.app {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2vh;
  left: 0%;
  text-align: center;
  align-items: center;
  align-content: center;
  position: relative;
  border-width: 10px;
}

.videoplayer {
  width: 500px;
}

.videoplayer-controls {
  display: flex;
  font: 0.8em sans-serif;
  width: 150%;
  height: 20%;
}


.videoplayer-controls-toggleplay,
.videoplayer-controls-togglemute {
  background-color: #d9d9d9;
  border-radius: 51px;
  color: black;
  position: relative;
  height: 1.5em;
  width: 6em;
  font-family: "Inter-Regular", Helvetica;
  white-space: nowrap;
  line-height: normal;
  display: flex;
  margin-bottom: 10px;
  justify-content: center;

  flex-shrink: 1;
  border: none;
}

.videoplayer-controls-toggleplay {
  margin-right: 20px;
  width: 5em;
}

.videoplayer-controls-time {
  flex: 0.4;
  text-align: left;
  line-height: 2;
}

.videoplayer-controls-track {
  flex: 0.2;
  line-height: 2;
  margin-right: 1rem;
}

</style>
