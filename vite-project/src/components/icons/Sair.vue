<template>
  <div class="flex flex-row items-center gap-[2vmin] cursor-pointer text-white w-fit font-medium no-underline transition-all duration-300 p-[1vmin] text-center text-[clamp(13px,1.8vmin,20px)] hover:bg-[hsla(267,81%,37%,0.63)] hover:font-semibold hover:scale-110" @click="deslogar">
    <p class="text-white font-semibold m-0">Sair</p>
    <img class="aspect-square w-[3.5vmin]" src="../../assets/Log_out.png" />
  </div>
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
