<template>
  <button class="salvar" @click="fnSalvar" :enabled="butEnabled" :disabled="!butEnabled">
    <img class="icone-download" alt="Save icon" src="../../assets/download.png" />
    <p class="texto-salvar">Baixar Resultado</p>
  </button>
</template>

<script>
export default {
  name: "salvar",
  created() {},
  data() {
    return {
      modo: "off",
    };
  },
  mounted() {
    const but = document.querySelector(".salvar");
    console.log("BUT DISABLED: ", but.disabled);
  },
  props: {},
  methods: {
    fnSalvar() {
      //logica para baixar o pdf dos resultados para a maquina do usuario
    },
  },
  computed: {
    butEnabled() {
      if (this.modo == "on") {
        return "true";
      } else {
        return null;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.salvar {
  background: none;

  justify-content: center;
  gap: 1vmin;
  align-items: center;
  margin: auto;
  width: fit-content;
  cursor: pointer;
  @include botao-header;
  flex-direction: row;
  display: inline-flex;
}

.icone-download {
  width: 5.5vmin;
  aspect-ratio: 1;
  padding: 0.5vmin;
}

.texto-salvar {
  display: flex;
  text-decoration: underline;
  color: #fff;
  font-weight: 800;
  margin: auto;
  width: fit-content;
  font-size: $fonte-header;
}
</style>
