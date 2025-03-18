<template>
  <div class="button-container">
    <button v-if="ativo" class="button classeAtivo">{{ texto }}</button>
    <button v-if="!ativo" class="button classeInativo">{{ texto }}</button>
  </div>
</template>

<script>
export default {
  name: "botaoMedio",
  methods: {},
  props: {
    ativo: true,
    texto: "",
  },
  created() {},
};
</script>

<style lang="scss" scoped>
$tam-fonte-botao: clamp(18px, 3vmin, 22px);
$peso-fonte-butao: 600;

.button-container {
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
  width: 37vmin;
  height: 10vmin;
  border: none;
  border-radius: 40px;
  padding: 1vmin;
  font-size: 24px;
  font-weight: $peso-fonte-butao;
  color: white;
  cursor: pointer;

  /* FONTE */
  font-size: $tam-fonte-botao;
  font-style: normal;

  transition: all 0.3s ease-out 0s;
}

.button:hover {
  background-color: hsl(267, 82%, 50%);
  transform: scale(1.08); // Increase size by 10% on hover
}

@media (max-width: 450px) {
  .button {
    $tam-fonte-botao: clamp(14px, 2.5vmin, 19px);
    font-size: $tam-fonte-botao;
  }
}

.classeAtivo {
  background-color: hsla(267, 81%, 37%, 0.776);
}

.classeInativo {
  background-color: #d0a7f6;
}
</style>
