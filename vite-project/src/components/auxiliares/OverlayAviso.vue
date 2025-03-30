<template
  @abreAviso="
    () => {
      this.aberto = true;
      console.log('RECEBEU ABRE AVISO');
    }
  "
>
  <section v-if="this.aberto" class="overlay">
    <div class="alerta">
      <img :src="srcImg" />
      <ul class="textos">
        <h1>{{ titulo }}</h1>
        <h1>{{ subtexto }}</h1>
        <h1 v-if="opcional !== ''">{{ opcional }}</h1>
      </ul>
    </div>
    <div class="div-but">
      <Button @click="this.fnClose" :texto="'OK'" :ativo="true"></Button>
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
  mounted() {},
  data() {
    return {
      aberto: false,
    };
  },

  props: {
    titulo: "",
    subtexto: "",
    opcional: "",
    srcImg: { type: String, default: "", required: true },
  },
  methods: {
    fnClose() {
      this.$emit("fechaAviso");
    },
  },
};
</script>

<style lang="scss" scoped>
.overlay {
  @include overlay;

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
