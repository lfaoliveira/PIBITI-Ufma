<template>
  <button class="containerSeta" @click="fnVoltar">
    <img src="../../assets/seta.png" alt="Seta" id="imagemSeta" />
    <div class="texto">Voltar</div>
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
.containerSeta {
  @include botao-header;
  display: inline-flex;
  flex-direction: row;
}

#imagemSeta {
  aspect-ratio: 4/3;
  width: clamp(25px, 32px, 5vmin);
  height: auto;
  margin-right: clamp(10px, 2vmin, 50px);
}

.texto {
  position: relative;
  font-size: $fonte-header;
  color: #fff;
  font-weight: normal;
}
</style>
