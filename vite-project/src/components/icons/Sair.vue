<template>
  <div class="frame" @click="deslogar">
    <p class="texto">Sair</p>
    <img class="img" src="../../assets/Log_out.png" />
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
.frame {
  gap: 2vmin;
  @include botao-header;
  display: flex;
  flex-direction: row;
  align-items: center;
}
p {
  color: white;
  @include botao-header;
  font-weight: 600;
  &:hover {
    background: hsl(0, 0%, 100%);
    font-weight: 600;
    transform: scale(0.9);
  }
}
img {
  aspect-ratio: 1/1;
  width: 3.5vmin;
}
</style>
