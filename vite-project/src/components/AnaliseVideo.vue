  <!-- PARTE GERADA POR IA -->

  <template>
  <main class="analysis-view">
    <header class="header">
      <nav class="navigation">
        <button class="back-button">
          <img src="https://cdn.builder.io/api/v1/image/assets%2F8b29090e827e422ea4601ed102c7c8ec%2F8073b5ee0f8d4d1f9ccf2dd8deaf2852" alt="Back arrow" class="back-icon" />
          <span>Voltar</span>
        </button>
        <button class="save-button">
          <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/bcdb4d424162515c6065f11e425d579318bf22d447dbea27d81b9649e4b2dc8e?placeholderIfAbsent=true&apiKey=8b29090e827e422ea4601ed102c7c8ec" alt="Save icon" class="save-icon" />
          <span>Salvar Resultado</span>
        </button>
      </nav>
    </header>
    <h1 class="page-title">Análise de Paralisia</h1>
    <section class="analysis-content">
      <div class="analysis-grid">
        <div class="diagnosis-card">
          <h2 class="diagnosis-title">Diagnóstico: Paralisia no Olho {X}/ Olho Saudável</h2>
          <p class="speed-difference">Diferença de Velocidade: XX.dd %</p>
          <p class="right-eye-speed">Olho Direito: XX.dd mm/s</p>
          <p class="left-eye-speed">Olho Esquerdo: XX.dd mm/s</p>
        </div>
        <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/6fc3fc6b7a4ffe40c62e0b7ba344a361d1040c5d2b60098c23ae6d95ca1836d0?placeholderIfAbsent=true&apiKey=8b29090e827e422ea4601ed102c7c8ec" alt="Analysis graph" class="analysis-graph" />
      </div>
    </section>
    <section class="additional-graphs">
      <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/ebe87e1942af688064c5388f00dd308ff4d20bf4833f49fdfcbee8164828034c?placeholderIfAbsent=true&apiKey=8b29090e827e422ea4601ed102c7c8ec" alt="Additional analysis graph" class="additional-graph" />
      <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/31716a680375eeece1f52072bad79d6e8ff3886573af8e13c0d04e7a3e0c662a?placeholderIfAbsent=true&apiKey=8b29090e827e422ea4601ed102c7c8ec" alt="Analysis icon" class="analysis-icon" />
    </section>
    <footer class="footer">
      <nav class="footer-nav">
        <a href="#" class="footer-link">Avisos Legais</a>
        <a href="mailto:contato@email.ufma.br" class="footer-link">Contato: contato@email.ufma.br</a>
        <a href="#" class="footer-link">Sobre</a>
      </nav>
    </footer>
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
.analysis-view {
  background-color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 80px;
  overflow: hidden;
}

.header {
  width: 100%;
  max-width: 1280px;
  padding: 12px 16px 0 8px;
  border: 1px solid #f00;
}

.navigation {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
  color: #fff;
  font: 500 20px Montserrat, sans-serif;
}

.back-button,
.save-button {
  display: flex;
  align-items: center;
  border-radius: 16px;
  background-color: #6113c6;
  box-shadow: 0 0 5px 3px rgba(0, 0, 0, 0.33);
  padding: 8px 16px;
  border: none;
  color: inherit;
  font: inherit;
  cursor: pointer;
}

.save-button {
  box-shadow: 0 0 8px 3px rgba(0, 0, 0, 0.93);
}

.back-icon,
.save-icon {
  width: 20px;
  height: 20px;
  margin-right: 5px;
}

.page-title {
  color: #3a0d75;
  font: 400 48px Montserrat, sans-serif;
  margin-top: 20px;
}

.analysis-content {
  width: 100%;
  margin-top: 86px;
}

.analysis-grid {
  display: flex;
  gap: 20px;
}

.diagnosis-card {
  flex: 0 0 28%;
  border-radius: 31px;
  background-color: #fff;
  box-shadow: 0 0 5px 4px rgba(0, 0, 0, 0.34);
  padding: 22px 32px 37px;
  color: #6113c6;
  font: 600 16px Montserrat, sans-serif;
}

.diagnosis-title {
  color: #38d200;
  font-size: 16px;
  margin-bottom: 44px;
}

.speed-difference,
.right-eye-speed,
.left-eye-speed {
  margin-top: 35px;
}

.analysis-graph {
  flex: 0 0 72%;
  width: 100%;
  object-fit: contain;
}

.additional-graphs {
  width: 100%;
  margin-top: 43px;
}

.additional-graph {
  width: 100%;
  object-fit: contain;
}

.analysis-icon {
  width: 108px;
  margin-top: 14px;
}

.footer {
  width: 100%;
  margin-top: 20px;
}

.footer-nav {
  display: flex;
  justify-content: space-between;
  max-width: 452px;
  margin: 0 auto;
  color: #000;
  font: 700 14px Montserrat, sans-serif;
}

.footer-link {
  color: inherit;
  text-decoration: none;
}

@media (max-width: 991px) {
  .analysis-view {
    padding: 0 20px;
  }

  .page-title {
    font-size: 40px;
  }

  .analysis-content {
    margin-top: 40px;
  }

  .analysis-grid {
    flex-direction: column;
  }

  .diagnosis-card {
    padding: 20px;
  }

  .diagnosis-title {
    margin-bottom: 40px;
  }

  .analysis-graph,
  .additional-graph {
    margin-top: 14px;
  }
}
</style>


<script>
import Seta from "./icons/Seta.vue";
import videoplayer from "./VideoPlayer.vue";
import videotrack from "./VideoPlayerTracker.vue";
import seta from "./icons/Seta.vue";
import { mapGetters } from 'vuex';

export default {
  // COMPONENTE QUE VAI IMPORTAR COMPONENTES DA HOMEPAGE
  name: "HomePage",
  components:{
    videoplayer,
    videotrack,
    seta,
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
CSS DO UPLOAD

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