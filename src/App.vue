<template>
  <header>
    <img
      alt="Vue logo"
      class="logo"
      src="./assets/logo.svg"
      width="125"
      height="125"
    />

    <div class="wrapper">
      <HelloWorld msg="Bem-vindo!"></HelloWorld>
    </div>
  </header>

  <menuInicial/>

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
import HelloWorld from "./components/HelloWorld.vue";
import videoplayer from "./components/VideoPlayer.vue";
import videoplayerTrack from "./components/VideoPlayerTracker.vue";
import menuInicial from "./components/MenuInicial.vue";

export default {
  components: {
    HelloWorld,
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
header {
  line-height: 1;
  display: flex;
  position: absolute;
  top: 1rem;
  /* Stick to the top */
  left: 0em;
  /* Align to the left */
  justify-content: center;
  /* Horizontal center */
  /*  width: 50rem; Full width to cover the entire page width     */
  height: 100px;
  width: 100%;
  padding-right: 20%;
  padding-left: 20%;
  flex: 0;
  border-color: aqua;
  /* border: 1ch; */
  background-color: rgb(0, 0, 0);
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 800px) {
  header {
    display: flex;
    place-items: center;
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    color: aliceblue;
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}

.app {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 25%;
  left: 50%;
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
