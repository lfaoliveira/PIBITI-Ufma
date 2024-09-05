<script>
import HelloWorld from "./components/HelloWorld.vue"
import videoplayer from "./components/VideoPlayer.vue";
import videoplayerTrack from "./components/VideoPlayerTracker.vue";
export default {
  components: {
    HelloWorld,
    videoplayer,
    videoplayerTrack,
  },
  data() {
    return {
      time: 0,
    }
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
    appStyle(){
      return {
        height: `${videoplayer.videoHeight + 10}`,
        width: `${videoplayer.videoWidth + 10}`,
      };
    }
  },
}
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="OLA MUNDO"></HelloWorld>
    </div>    
  </header>

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




<style scoped>
header {
  color:aliceblue;
  line-height: 1.5;
  display: flex;
  position: absolute;
  top: 3%;  /* Stick to the top */
  left: 0; /* Align to the left */
  justify-content: center; /* Horizontal center */
  align-items: center;
  width: 100%; /* Full width to cover the entire page width */
  height: 120px;
  border-color: aqua;
  background-color: rgba(0, 0, 0, 0.5);
  
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    color:aliceblue;
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}

.app{
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10%;
  height: 50ch;
}

.videoplayer {
  width: 500px;
}

.videoplayer-controls {
  display: flex;
  font: 0.8em sans-serif;
  width: 100%;
}

.videoplayer-controls-toggleplay,
.videoplayer-controls-togglemute {
  background-color: #d9d9d9;
  border-radius: 51px;
  color: black;
  position: relative;
  height: 10%;
  width: 20%;
  font-family: "Inter-Regular", Helvetica;
  white-space: nowrap;
  letter-spacing: 0;
  line-height: normal;
  display: block;
  padding: 0.25lh;
  margin-bottom: 10px;
  text-align: center;
  flex: 1;
  border: none;
}

.videoplayer-controls-time {
  flex: 2;
  text-align: center;
  line-height: 2;
}

.videoplayer-controls-track {
  flex: 5;
  line-height: 2;
}
</style>



