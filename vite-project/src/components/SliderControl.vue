<template>
  <div class="linha-do-tempo">
    <button
      class="bola-slider"
      ref="bolaSlider"
      @mousedown="startDrag($event)"
      @mousemove="drag($event)"
      @mouseup="stopDrag($event)"
      @updateprogress="(porcento, $event) => moverSlide(porcento, $event)"
      :style="{ left: this.posBola + 'px' }"
    ></button>
    <!-- <div class="slider" ref="slider"></div> -->
    <div class="slider" ref="slider" @click="updateSlider"></div>
  </div>
</template>

<script>
export default {
  name: "Controle do Slider",
  props: {},
  data() {
    return {
      // OBS: nao usar duracao em tempo de montagem, apenas no click
      videoDuration: null,
      sliderPercentage: 0,
      posBola: 0,
      posInicial: 0,
      tamSlider: null,
    };
  },
  mounted() {
    // const rect = this.$refs.bolaSlider.getBoundingClientRect();
    console.log("MOTNADO SLIDER");
    this.$nextTick(() => {
      const esq = this.$refs.bolaSlider.style.left;
      this.posBola = parseFloat(esq);
      this.posInicial = this.posBola;
      this.startX = this.posBola;

      this.tamSlider = parseFloat(this.$refs.slider.style.width);
      console.log(this.$refs.slider.style.width);
    });
  },
  methods: {
    moverSlide(percent, $evt) {
      alert("ERA RPA MOVER");
      // Update the video time
      const bola = this.$refs.bolaSlider;

      bola.style.left = percent * this.tamSlider - this.posInicial;

      // Update the slider position visually
      this.sliderPercentage = percent;
    },
    seekUser($evt) {
      // Seek the video based on where the user clicks on the slider
      const sliderContainer = this.$refs.slider;
      const video = this.$refs.videoplayer;

      // Get bounding box and calculate clicked position
      const rect = sliderContainer.getBoundingClientRect();
      const clickPosition = $evt.clientX - rect.left;
      const percentageClicked = clickPosition / rect.width;

      // Update the video time
      video.currentTime = percentageClicked * video.duration;

      // Update the slider position visually
      this.sliderPercentage = percentageClicked * 100;
    },

    startDrag(event) {
      this.isDragging = true;
      this.startX = event.clientX - this.posBola;
      console.log("START:" + this.posBola);
    },
    drag(event) {
      this.posBola = event.clientX - this.posBola;
      console.log("DRAG:" + this.posBola);
    },
    stopDrag() {
      this.isDragging = false;
      console.log("STOP:" + this.posBola);
    },
    seekToPercentage(percentage) {
      this.$refs.videoplayer.currentTime = (percentage / 100) * this.duration;
    },
  },
};
</script>

<style scoped>
* {
  max-width: 100%;
  --tam-slider: clamp(1%, 5px, 10px);
  --alt-controles: clamp(50px, 12vmin, 170px);
  z-index: 1;
  border: none;
  margin: 0;
}

.linha-do-tempo {
  display: flex;
  justify-content: center;
  height: fit-content;
  flex-direction: column;
  margin-top: 1vmin;
}

.slider {
  background-color: rgba(255, 255, 255, 0.72);
  width: 100%;
  height: clamp(3px, 7px, 10px);
  cursor: pointer;
}

.bola-slider {
  --tam-bolinha: clamp(1.7vmin, 22px, 16px);
  width: var(--tam-bolinha);
  height: var(--tam-bolinha);
  position: absolute;
  border-radius: 100%;

  background-color: #fff;
  left: -0.1vmin;
  z-index: 4;
  cursor: pointer;
}
</style>
