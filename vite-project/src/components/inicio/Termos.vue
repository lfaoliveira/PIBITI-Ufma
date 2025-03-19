<template>
  <HeaderSistema tipo="outro" />
  <h1>Termos e Condições</h1>
  <main>
    <h1>Título dos Termos e Condições</h1>
    <!-- TODO: BOTAR REATIVIDADE DO VUE COM STRINGS PRA PREENCHER ESSA PORRA -->
  </main>
</template>

<script>
import Voltar from "../icons/Voltar.vue";
import HeaderSistema from "../analise/HeaderSistema.vue";

export default {
  name: "termosComp",
  components: {
    Voltar,
    HeaderSistema,
  },
  created() {},
  data() {
    return {};
  },
  props: {},
  methods: {
    fnVoltar() {
      this.$router.push({ name: "cad" });
    },
  },
};
</script>

<style lang="scss" scoped>
* {
  --alt-butao: clamp(40px, 5vmin, 77px);
  --raio-butao: clamp(10px, 40%, 20px);
  font-family: "Montserrat", "Inter";
  border: 0px;
}

.div-header {
  max-width: 95%;
  position: absolute;
  margin: 1vmin 0px 0px 0px;
  height: auto;
  width: clamp(90vmin, 85%, 95%);
  z-index: 1;
  display: flex;
  align-items: center;
}
</style>
