<template>
  <div class="div-header">
    <Voltar class="botao-voltar" :onclick="fnVoltar"></Voltar>
    <Salvar @click="salvarRes"></Salvar>
  </div>
</template>

<style scoped>
* {
  --alt-butao: clamp(40px, 5vmin, 77px);
  --raio-butao: clamp(10px, 40%, 20px);
  font-family: "Montserrat", "Inter";
  border: 0px;
}
input {
  display: none;
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
  /* grid-template-rows: 1fr;
  grid-template-columns: 1fr 1fr; */
}
</style>

<script>
import Voltar from "../icons/Voltar.vue";
import Salvar from "../icons/Salvar.vue";
export default {
  name: "headerAnalise",
  methods: {
    fnVoltar() {
      this.$router.push({ name: "home" });
    },
    salvarRes() {
      this.$router.push({ name: "salvar" });
    },
  },
  components: {
    Voltar,
    Salvar,
  },
  created() {},
  data() {
    return {
      //id para recuperar dados do banco de dados
      idDados: "",
    };
  },
  props: {},
};
</script>
