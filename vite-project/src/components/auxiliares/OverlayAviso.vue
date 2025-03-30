<template>
  <section class="overlay">
    <div class="alerta">
      <img :src="srcImg" />
      <ul class="textos">
        <h1>{{ titulo }}</h1>
        <h1>{{ subtexto }}</h1>
        <h1 v-if="opcional !== ''">{{ opcional }}</h1>
      </ul>
    </div>
    <div class="div-but">
      <Button @click="fnClose()" :texto="'OK'" :ativo="true"></Button>
    </div>
  </section>
</template>

<script>
import Button from "./Button.vue";

export default {
  name: "overlay",
  components: {
    Button,
  },
  created() {},
  data() {
    return {};
  },
  props: {
    titulo: "",
    subtexto: "",
    opcional: "",
    srcImg: { type: String, default: "", required: true },
  },
  methods: {
    fnClose() {
      //fechar overlay;
    },
  },
};
</script>

<style lang="scss" scoped>
.overlay {
  z-index: 20;
  display: flex;
  width: clamp(50%, 50%, 50%);
  position: absolute;
  margin: auto;
  background: white;
  border: 1px solid black;
  height: 90vmin;
  flex-direction: column;
  align-items: center;
  gap: 5vmin;

  img {
    margin-left: 5vmin;
    width: 10vmin;
    height: 10vmin;
  }

  .alerta {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 2vmin;

    .textos {
      display: flex;
      width: fit-content;
      flex-direction: column;
      align-items: flex-start;
      gap: 5vmin;
      align-self: stretch;
    }
  }
  .div-but {
    width: 22vmin;
  }
}
</style>
