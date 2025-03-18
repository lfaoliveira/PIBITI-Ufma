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
  //   @include mix-botao-header;
  padding: clamp(10px, 2%, 20px);
  border-radius: var(--raio-butao);
  background: none;
  display: inline-block;
  text-align: center;
  justify-content: center;
  /* gap: clamp(4vmin, 4.5vmin, 5vmin); */
  align-items: center;
  width: fit-content;
  height: var(--alt-butao);
  box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.29);
  margin: auto 0px;

  cursor: pointer;
}

.containerSeta:hover {
  .texto {
    font-size: calc($fonte-header * 1.1);
  }
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
