<template>
  <router-view></router-view>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  props: {},
  data() {
    return {
      _: 0,
    };
  },
  async mounted() {
    console.log("LOGADO: ", this.$store.getters.getLogado);
  },
};
</script>

<style lang="scss">
$fonte-maior: 48px;
$fonte-secao: 32px;
$fonte-paragrafo-info: 20px;
$fonte-but-grande: 24px;
</style>
