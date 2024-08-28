<script>
import HelloWorld from './components/HelloWorld.vue'
import videoplayer from "./components/videoplayer.vue";
import videoplayerTrack from "./components/VideoPlayerTracker.vue";

export default {
  components: {
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
}
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div>    
  </header>

  <div class="app">
    <videoplayer
      class="videoplayer"
      src=".\\src\\assets\\exemplo.mp4"
      :muted="false"
      :autoplay="false"
      :controls="true"
      :loop="false"
      poster=".\\src\\assets\\01.jpg"
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
          />
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
  line-height: 1.5;
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
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
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
  flex: 1;
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



