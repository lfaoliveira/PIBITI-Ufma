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
  <div class="controles">
    <span class="time-display">00:00</span>
    <button class="slider"></button>
    <div class="bola-slider"></div>
    <button class="bola-play">
      <object type="image/svg+xml" class="control-icon" :data="urlICone" />
    </button>
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
  --tam-slider: clamp(1%, 5px, 10px); 
  z-index: 1;
  border: none;
  margin: 0;
}

.controles{
  background: linear-gradient(180deg, rgba(95,95,95,0.66) 0%, rgba(33,33,33,0.85) 39%, rgba(17,0,0,1) 97%);
  height: clamp(2vmin, 101px, 150px);
}

.time-display{
  font-size: clamp(8px, 12px, 15px);
  position: relative;
  top: clamp(10px, 15px, 20px);
}

.bola-play{
  --tam-bola: clamp(3%, 38px, 40px);
  display: flex;
  width: var(--tam-bola);
  height: var(--tam-bola);
  background-color: #fff;
  margin: -1vmin 0 0vmin 0.7vmin;
  justify-content: center;
  border-radius: 100%;
  cursor: pointer;
}

.control-icon{
  padding: 12%;
  width: clamp(1vmin, 22px, 100%);
  cursor: pointer;
}

.slider{
  background-color: rgba(255, 255, 255, 0.72);
  width: 100%;
  height: var(--tam-slider);
  
}

.bola-slider{
  --tam-bolinha: clamp(1.6vmin, 12px, 16px);
  width: var(--tam-bolinha);
  height: var(--tam-bolinha);
  background-color: #ccc;
  position: relative;
  top: clamp(-11px - var(--tam-slider)/2, -20px - var(--tam-slider)/2, -30px - var(--tam-slider)/2);
  border-radius: 100%;
  cursor: pointer;
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
