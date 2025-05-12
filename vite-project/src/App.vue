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
    try {
      const resp = await axios.get(this.$store.getters.getUrlChecklogin, {
        withCredentials: true,
      });
      if (resp.status === 200) {
        this.$store.commit("setLogado", true);
        console.log("LOGADO: ", this.$store.getters.getLogado);
      }
    } catch {
      this.$store.commit("setLogado", false);
      console.log("LOGADO: ", false);
    }
  },
};
</script>

<style lang="scss">
$fonte-maior: 48px;
$fonte-secao: 32px;
$fonte-paragrafo-info: 20px;
$fonte-but-grande: 24px;
</style>
