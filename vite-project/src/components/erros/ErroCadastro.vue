<template>
  <div class="erro" v-if="errado">{{ this.texto }}</div>
</template>

<script>
import { ref } from "vue";
const errado = ref(false);

export default {
  name: "CadComp",
  created() {
    /*   this.$watch("texto", (newVal) => {
      if (newVal !== "") {
        this.errado = true;
      } else {
        this.errado = false;
      }
    }); */
  },
  data() {
    return {
      texto: "",
      tipo: "",
    };
  },
  mounted() {
    console.log(this.errado);

    if (this.tipo === "checks") {
      this.texto = "Aceite os Termos e Condições!";
    } else {
      this.texto = this.tipo + " Incorreto!";
    }
  },
  props: {},
  methods: {},
};
</script>

<style lang="scss" scoped>
.erro {
  width: 100%;
  height: 50px;
  background-color: white;
  color: black;
}
</style>
