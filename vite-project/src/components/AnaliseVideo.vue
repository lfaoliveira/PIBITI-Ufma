  <!-- PARTE GERADA POR IA -->

<template>
  <main class="analysis-view">
    <HeaderAnalise id="header"></HeaderAnalise>

    <h1 class="page-title">Análise de Paralisia</h1>
    
  <div class="responsive-container">
      <div class="diagnosis-card secao">
        <h2 class="diagnostico texto-diag">Diagnóstico: Paralisia no Olho {X}/ Olhos Saudáveis</h2>
        <p class="dif-velocidade texto-diag">Diferença de Velocidade: XX.dd %</p>
        <p class="velocidade-dir texto-diag">Olho Direito: XX.dd mm/s</p>
        <p class="velocidade-esq texto-diag">Olho Esquerdo: XX.dd mm/s</p>
      </div>
    <div class="div-grafico">
      <!-- Placeholder for your graph (image or canvas) -->
      <img class="grafico" alt="Analysis graph" src="../assets/Video exemplo.png" />
    </div>
  </div>
    <VideoPlayer class="secao"></VideoPlayer>
    
    <Rodape></Rodape>
  </main>
</template>








  <!-- PARTE ORIGINAL -->

  <!-- #PARTE DE UPLOAD DE VIDEO  
  <h1 @click="sendData"> Bem-Vindo!</h1>

  label para estilizar butao upload 
  <div class="wrapper">
    <label for="fileInput" ref="" class="custom-file-upload" :style="estiloUpload">
      Upload
    </label>
    <input type="file" id="fileInput" accept="video/*" @change="handleFileUpload" 
    @focus="addFocusClass" @blur="removeFocusClass">
  </div>    
  
  
  <seta class="setaClasse" @click="onVoltar"></seta>
  <div  class="edicaoVideo">
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
          <button @click="togglePlay()" :style="controlStyle" class="videoplayer-controls-toggleplay">
            {{ playing ? "pause" : "play" }}
          </button>
          <div class="videoplayer-controls-time">
            {{ convertTimeToDuration(time) }} /
            {{ convertTimeToDuration(duration) }}
          </div>
          <videotrack
            :percentage="percentagePlayed"
            @seek="seekToPercentage"
            class="videoplayer-controls-track"
          ></videotrack>
          <button @click="toggleMute()" class="videoplayer-controls-togglemute">
            {{ videoMuted ? "unmute" : "mute" }}
          </button>
        </div>
      </template>
    </videoplayer>
  </div> -->


<style scoped>

*{
  max-width: 100vmax;
  font-family: Montserrat, 'Inter';
}

/* 
.secao {
  margin: 0vmin 2vmin;
  max-width: 100%;

  align-self: center;
  padding: 0vmin 2vmin; 
  flex-wrap: wrap;

} */

.texto-diag{
  --fonte-diag: clamp(10px, 15px, 20px);
  font-size: var(--fonte-diag);
}

.responsive-container {
  height: 50%;
  display: flex;
  flex-wrap: wrap; /* Allows the items to wrap to the next line */
  gap: 20px;
  margin: 0 2%; /* 2% lateral margins */
}

.div-grafico {
  flex: 1; /* Take equal space by default */
  min-width: 300px; /* Minimum width before breaking */
}

.div-grafico img{
  width: 100%; /* Make the image responsive */
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Container Query for screen width greater than 800px */
@media only screen  and (min-width: 800px) {
  .responsive-container {
    flex-direction: row; /* Horizontal layout */
  }
  .grafico{
    object-fit: scale-down;
  }
}

@media only screen  and (max-width: 800px) {
  .responsive-container {
    flex-direction: column; /* Vertical layout */
    justify-content: center;
  }
  .diagnosis-card{
    justify-self: center;
  }
}





.analysis-view {
	width: clamp(100%,100%, 100%);
  background-color: #fff;
  /* box-shadow: 0 0 5px 4px rgba(0, 0, 0, 0.34); */
  display: flex;
  flex-direction: column;
  align-items: center;
}


.navigation {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
  color: #fff;
  font: 500 20px Montserrat, sans-serif;
}

.page-title {
  color: #3a0d75;
  font: 400 48px Montserrat, sans-serif;
  margin: clamp(70px, 15vmin, 120px) auto 0px auto;
}

.analysis-content {
  width: 100%;
  margin-top: 86px;
}


.analysis-grid {
  --tam-grid: clamp(400px, 95%, 100%);
  display: grid;
  grid-template-rows: repeat(auto-fill, minmax(40vmin, 2fr));
  grid-template-columns: 1fr fit-content(20%);
  width: var(--tam-grid);
  margin: auto;
}

.diagnosis-card {
  border-radius: 31px;
  background-color: #fff;
  box-shadow: 0 0 5px 4px rgba(0, 0, 0, 0.34);
  padding: 22px 32px 37px;
  color: #6113c6;
  font-size: clamp(5px, 14px, 20px);
  width: clamp(200px, 100vmin, 100%);
  flex: 0.3;
}

.diagnostico {
  color: #38d200;
  margin-bottom: 44px;
  font-size: calc( var(--fonte-diag) + 25%);
}

.dif-velocidade,
.velocidade-dir,
.velocidade-esq {
  margin-top: 35px;
}

.grafico {
  /* flex: 0 0 72%; */
  width: clamp(300px, 100vmin, 100% - 0.8*var(--tam-grid));
  justify-self: start;
  align-self: center;
  height: 100%;
  object-fit:fill;
}

.video-res{
  margin-bottom: 100px;
}
</style>


<script>
import videotrack from "./VideoControls.vue";
import seta from "./icons/Seta.vue";
import { mapGetters } from 'vuex';
import Rodape from "./Rodape.vue";
import HeaderAnalise from "./HeaderAnalise.vue"
import VideoPlayer from "./VideoPlayer.vue";
export default {
  // COMPONENTE QUE VAI IMPORTAR COMPONENTES DA HOMEPAGE
  name: "HomePage",
  components:{
    VideoPlayer,
    videotrack,
    seta,
    Rodape,
    HeaderAnalise,
  },
  created() {},
  data() {
    return {
      time: 0,
    };
  },
  props: {},
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

    onVoltar(){
      this.$router.push('/');
    },
    addFocusClass() {
      // Manually add the 'focus' class to the label
      const label = document.querySelector('.custom-file-upload');
      label.classList.add('focus');
      
    },
    removeFocusClass() {
      // Manually remove the 'focus' class from the label
      const label = document.querySelector('.custom-file-upload');
      label.classList.remove('focus');
    },
  },
  computed: {
    controlStyle(){
      return {
        height: `${videoplayer.videoHeight/window.innerHeight}%`,
        width: `${videoplayer.videoWidth/window.innerWidth}%`,
      }

    },
    estiloUpload(){
      return {
        // COR E FONTE
        borderRadius: `51px`,
        border: `none`,
        color: `black`,        
        //TAMANHO
        position: `relative`,
        //POSICIONAMENTO
        whiteSpace: `nowrap`,
        letterSpacing: `0`,
        alignItems: `center`,
        display: `flex`,
        justifyContent: `center`,
        textAlign: `center`,
      }
    },

    ...mapGetters(['getSharedData']),
    sharedData() {
      return this.getSharedData;
    },
  
  }
};
</script>

<style scoped>
/* CSS DO UPLOAD */

.custom-file-upload{
  background-color: #43C3DD;
  --butao-height: 6vmin;
  --butao-width: 30vmin;
  height: clamp(4rem, var(--butao-height), 6rem);
  width: clamp(6rem, var(--butao-width), 10rem);
  font-size: clamp(2rem, 4vmin, 6rem );
}

.custom-file-upload:focus{
  background-color: #ffffff;
  height: clamp(4vmin + 1vmin, var(--butao-height) + 2 vmin, var(--butao-height)+ 4vmin);
  width: clamp(6rem, var(--butao-width), 10rem);
  font-size: clamp(2rem, 4vmin, 6rem );
}

.custom-file-upload:hover{
  background-color: #39abc2;
  --butao-height: 8vmin;
  --butao-width: 30vmin;
  height: clamp(2vmin + 4vmin, var(--butao-height) + 4vmin, var(--butao-height)+ 12vmin);
  width: clamp(6rem, var(--butao-width), 10rem);
  font-size: clamp(3vmin, 5vmin, 7vmin);
}


CSS ORIGINAL

.edicaoVideo{
  font-family: 'Roboto Serif', serif !important;
}
.setaClasse{
  position: absolute;
  aspect-ratio: 4/3;
  top: 0.2vmin;
  left: 5vmin;
}
.videoplayer {
  display: grid;
  width: 100%;
  height: 100%;
}
button{
  font-family: 'Roboto Serif', serif !important;
}

.videoplayer-controls {
  display: block flex;
  width: 80%;
  height: 80%;
}


.videoplayer-controls-toggleplay,
.videoplayer-controls-togglemute {
  background-color: #43C3DD;
  border-radius: 51px;
  color: #001B2C;
  position: relative;
  height: 1.5em;
  width: 6em;
  white-space: nowrap;
  line-height: normal;
  display: flex;
  left: 0;
  justify-content: center;

  flex-shrink: 1;
  border: none;
}

.videoplayer-controls-toggleplay {
  margin-right: 20px;
}

.videoplayer-controls-time {
  text-align: left;
  font-weight: 400;
  line-height: 2;
  color: #001B2C;
  margin-right: 1rem;
  width: 20%;
}

.videoplayer-controls-track {
  line-height: 2;
  margin-right: 1rem;
}

</style>