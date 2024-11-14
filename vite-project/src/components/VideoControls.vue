<template>
  <!-- <div class="video-track">
    <input
      type="range"
      min="0"
      max="100"
      step="1"
      :value="percentage.toFixed(1)"
      @input="onInput"
    />
  </div> -->
  <span class="time-display">00:00</span>
  <button class="slider">
    <!-- TODO: AJUSTAR BOLA DO SLIDER DENTRO DO SLIDER -->
    <div class="bola-slider"></div>
  </button>
  <div class="bola-play">
    <object type="image/svg+xml" class="control-icon" :data="urlICone" />
  </div>

</template>

<script>
export default {
  name: "videotrack",
  props: {
    percentage: { type: Number, required: true },
  },
  data() {
    return {
      urlICone: 'src/assets/play.svg',
    }
  },
  methods: {
    onInput(e) {
      console.log("INPUT no slider")
      this.$emit("seek", e.target.value);
    },
  },
  mounted() {
  },
};
</script>

<style>


*{
  z-index: 1;
}
.bola-play{
  display: flex;
  width: clamp(3%, 20px, 40px);
  height: clamp(3%, 20px, 40px);
  background-color: #fff;
  margin: 2vmin 0 2vmin 2vmin;
  justify-content: center;
  border-radius: 100%;
}

.control-icon{
  padding: 1%;
width: clamp(1vmin, 22px, 100%);
}

.slider{
  background-color: red;
}

input[type="range"] {
  position: relative;
  top: -1px;
  overflow: hidden;
  width: 245px;
  -webkit-appearance: none;
  appearance: auto;
  background-color: #ccc;
  border-radius: 5px;
}

input[type="range"]:focus {
  outline: none;
}

input[type="range"]::-webkit-slider-runnable-track {
  height: 8px;
  -webkit-appearance: none;
  color: #333;
  margin-top: -1px;
}

input[type="range"]::-webkit-slider-thumb {
  width: 8px;
  -webkit-appearance: none;
  height: 8px;
  cursor: ew-resize;
  background: #333;
  box-shadow: -245px 0 0 245px #333;
}
</style>
