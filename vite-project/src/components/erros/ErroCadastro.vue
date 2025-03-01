<script>
import { ref } from "vue";

export default {
  name: "CadComp",
  created() {
    /* document.addEventListener("cadastroCerto", () => {
      console.log(this.tipo + " OK");
    }); */
  },
  data() {
    return {
      cont: 0,
      texto: "",
      tipo: null,
    };
  },
  mounted() {
    console.log("MOUNTED ERROS");
  },
  props: {},
  methods: {
    handleErro(tipo) {
      console.log("ERRO AQUI");
      this.tipo = tipo;
      if (this.tipo === "checks") {
        this.texto = "Aceite os Termos e Condições!";
      } else {
        this.texto = this.tipo + " Incorreto!";
      }
      const caixa = this.$refs.caixaErro;
      caixa.style.display = "unset";
      console.log("TIPO ERRO: ");
    },
    handleSucess() {
      const caixa = this.$refs.caixaErro;
      caixa.style.display = "none";
      this.texto = "adadaw";
    },
  },
};
</script>

<style lang="scss" scoped>
* {
  box-sizing: content-box;
}

.erro {
  width: 100%;
  height: 50px;
  background-color: white;
  color: red;
  display: none;
}
</style>

<template>
  <div
    class="erro"
    ref="caixaErro"
    @erroCadastro="handleErro"
    @cadastroCerto="handleSucess"
  >
    {{ this.texto }}
  </div>
</template>
