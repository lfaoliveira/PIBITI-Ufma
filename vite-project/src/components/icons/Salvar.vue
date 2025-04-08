<template>
  <button class="salvar" @click="fnSalvar" :disabled="butDisabled">
    <img class="icone-download" alt="Save icon" src="../../assets/download.png" />
    <p class="texto-salvar">Baixar Resultado</p>
  </button>
</template>

<script>
export default {
  name: "salvar",
  created() {},
  data() {
    return {};
  },
  mounted() {},
  props: {
    modo: "off",
  },
  methods: {
    fnSalvar() {
      //logica para baixar o pdf dos resultados para a maquina do usuario
    },
  },
  computed: {
    butDisabled() {
      return this.modo == "off";
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
  margin: 0.5vmin auto;
  width: fit-content;
  cursor: pointer;
  @include botao-header;
  padding: 0px;
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
  font-weight: 700;
  margin: auto;
  width: fit-content;
}
</style>
