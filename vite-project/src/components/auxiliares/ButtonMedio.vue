<template>
  <div class="button-container">
    <button
      :type="type"
      @click="$emit('click', $event)"
      v-if="ativo == true"
      class="button classeAtivo"
      enabled
    >
      {{ texto }}
    </button>
    <button
      :type="type"
      @click="$emit('click', $event)"
      v-if="ativo == false"
      class="button classeInativo"
      disabled
    >
      {{ texto }}
    </button>
  </div>
</template>

<script>
export default {
  name: "botaoMedio",
  methods: {},
  props: {
    ativo: true,
    texto: "",
    type: "button",
  },
  created() {},
  mounted() {
    console.log("ATIVO MEDIO: ", this.ativo);
  },
};
</script>

<style lang="scss" scoped>
$tam-fonte-botao: clamp(18px, 3vmin, 22px);
$peso-fonte-butao: 600;

.button-container {
  @include container-botoes;
  .button {
    @include botao-acao($escala: 1.08, $height: 2.6lh);
    font-weight: $peso-fonte-butao;
    font-size: $fonte-but-medio;
    color: white;
  }
}
</style>
