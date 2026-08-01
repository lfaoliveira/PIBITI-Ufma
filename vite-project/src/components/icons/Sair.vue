<template>
  <a class="flex items-center justify-end gap-3 w-full text-white text-xs sm:text-sm font-medium py-2 px-3 rounded-lg hover:bg-white/10 transition-colors cursor-pointer" @click="deslogar">
    <span>Sair</span>
    <img class="w-5 h-5" src="../../assets/Log_out.png" />
  </a>
</template>

<script>
import axios from "axios";

export default {
  name: "Deslogar",
  created() {},
  data() {
    return {};
  },
  props: {},
  methods: {
    async deslogar() {
      try {
        let res = await axios.get(this.$store.getters.getUrlDeslogar);

        while (res.status == 200) {
          await new Promise((resolve) => setTimeout(resolve, 5000));

          res = await axios.post(this.$store.getters.getUrlDeslogar);
          if (res.status === 200) {
            this.$store.commit("setLogado", false);
            break;
          }
        }
      } catch (e) {
        console.log("STATUS DESLOGAR: ", e.status);
        if (e.status !== 200) {
          this.$store.commit("setLogado", false);
          console.log("DESLOGADO!!!!!");
        }
      }
    },
  },
};
</script>

<style lang="scss" scoped>
/* Estilos substituídos por Tailwind */
</style>
