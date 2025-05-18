<template>
  <div class="button-container">
    <button
      :type="type"
      @click="handleClick"
      v-if="ativo == true"
      class="button classeAtivo"
      enabled
    >
      {{ texto }}
    </button>
    <button :type="type" v-if="ativo == false" class="button classeInativo" disabled>
      {{ texto }}
    </button>
  </div>
</template>

<script>
export default {
  name: "botaoPequeno",
  methods: {
    handleClick() {
      this.$emit("click");
      if (this.type == "submit") {
        this.$emit("submit");
      }
    },
  },
  props: {
    ativo: true,
    texto: "",
    type: "button",
  },
  created() {},
  mounted() {
    // console.log("ATIVO PEQUNO: ", this.ativo);
  },
};
</script>

<style lang="scss" scoped>
$tam-fonte-botao: clamp(16px, 3vmin, 20px);
$peso-fonte-butao: 600;
$alt-botao: clamp(2lh, 7.5vmin, 3lh);

.button-container {
  @include container-botoes;
  .button {
    @include botao-acao($escala: 1.05, $height: $alt-botao);
    font-weight: $peso-fonte-butao;
    font-size: $fonte-but-medio;
    color: white;
  }
}
</style>
