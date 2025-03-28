<template>
  <button class="salvar" @click="fnSalvar" :enabled="butEnabled" :disabled="!butEnabled">
    <img class="icone-download" alt="Save icon" src="../../assets/download.png" />
    <p class="texto-salvar">Salvar Resultado</p>
  </button>
</template>

<script>
export default {
  name: "salvar",
  created() {},
  data() {
    return {};
  },
  props: {
    modo: { type: String, default: "off" },
  },
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

.salvar:disabled {
  cursor: default;
  opacity: 0.5;
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
