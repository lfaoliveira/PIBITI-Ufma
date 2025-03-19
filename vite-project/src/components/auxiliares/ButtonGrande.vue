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
  mounted() {},
};
</script>

<style lang="scss" scoped>
$tam-fonte-botao: clamp(18px, 3vmin, 22px);
$peso-fonte-butao: 600;

.button-container {
  width: 100%;
  /* display: flex;
    flex-direction: column;
    align-items: center; */
  display: inline-block;
  text-align: center;
  padding: 1vmin;
}

.button {
  justify-content: center;
  align-items: center;
  display: inline-block;
  text-align: center;
  /* width: 261px;
    height: 74px; */
  width: 100%;
  height: 2.6lh;
  border: none;
  border-radius: 40px;
  padding: 1vmin;
  font-size: 24px;
  font-weight: $peso-fonte-butao;
  color: white;
  cursor: pointer;

  /* FONTE */
  font-size: $fonte-but-medio;
  font-style: normal;

  transition: all 0.3s ease-out 0s;
}

.button:enabled:hover {
  background-color: hsl(267, 77%, 46%);
  transform: scale(1.08); // Increase size by 10% on hover
}
.button:disabled {
  cursor: default;
}

.classeAtivo {
  background-color: hsl(267, 81%, 37%);
}

.classeInativo {
  background-color: #d0a7f6;
}
</style>
