<template>
  <button class="inline-flex flex-row items-center cursor-pointer text-white w-fit font-medium no-underline transition-all duration-300 p-[1vmin] text-center text-[clamp(13px,1.8vmin,20px)] hover:bg-[hsla(267,81%,37%,0.63)] hover:font-semibold hover:scale-110" @click="fnVoltar">
    <img src="../../assets/seta.png" alt="Seta" class="aspect-[4/3] w-[clamp(25px,32px,5vmin)] h-auto mr-[clamp(10px,2vmin,50px)]" />
    <div class="text-white font-normal">Voltar</div>
  </button>
</template>

<script>
export default {
  name: "seta",
  created() {},
  data() {
    return {};
  },
  methods: {
    fnVoltar() {
      // retorna 1 página
      this.$router.go(-1);
    },
  },
};
</script>

<style lang="scss" scoped>
/* Estilos substituídos por Tailwind */
</style>
