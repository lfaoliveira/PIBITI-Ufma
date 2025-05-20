<template>
  <a class="salvar" :href="urlPDF" :disabled="butDisabled">
    <img class="icone-download" alt="Save icon" src="../../assets/download.png" />
    <div class="texto-salvar">Baixar Resultado</div>
  </a>
</template>

<script>
export default {
  name: "salvar",
  created() {},
  data() {
    return {};
  },
  mounted() {
    this.$el.addEventListener("click", (event) => {
      if (event.target.closest(".salvar")) {
        console.log("Salvar element clicked");
      }
    });
  },
  props: {
    modo: "off",
    urlPDF: null,
  },
  methods: {},
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
  display: flex !important;
}

.icone-download {
  width: 3em;
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
