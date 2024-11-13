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
  <div class="progress-indicator">
    <!-- TODO: AJUSTAR BOLA DO SLIDER DENTRO DO SLIDER -->
    <div class="bola-slider"></div>
  </div>
  <div class="bola-play">
    <img alt="ICONE PLAY" class="control-icon" src=""/>
  </div>

</template>

<script lang="js">
export default {
  name: "videotrack",
  props: {
    percentage: { type: Number, required: true },
  },
  methods: {
    onInput(e) {
      console.log("INPUT no slider")
      this.$emit("seek", e.target.value);
    },
  },
};
</script>

<style>


.play-button {
  position: relative;
  align-self: center;
  width: 136px;
  height: 93px;
  border: 5px solid #ed1818;
}

.video-controls {
  position: relative;
  display: flex;
  z-index: 1;
  margin-top: 186px;
  width: 100%;
  background: linear-gradient(180deg, rgba(95,95,95,0.66) 0%, rgba(33,33,33,0.85) 52%, rgba(17,0,0,1) 97%);
  flex-direction: column;
  align-items: flex-start;
  padding: 4px 0px 4px 0;
}

.progress-indicator {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  background-color: rgba(255, 255, 255, 0.62);
  width: 100%;
  height: clamp(5px, 1vmin,12px );
  margin-top: 5px;
}
.bola-slider{
  --tam: clamp(5px, 2vmin, 20px);
  width: var(--tam);
  height: var(--tam);
  background-color: #D9D9D9;
  border-radius: 100%;
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
