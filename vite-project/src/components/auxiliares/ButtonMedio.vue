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

<style scoped>
* {
  --tam-fonte-botao: clamp(18px, 3vmin, 22px);
}

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
  font-weight: 600;
  color: white;
  cursor: pointer;

  /* FONTE */
  font-size: var(--tam-fonte-botao);
  font-style: normal;
}

.button:hover {
  font-size: calc(var(--tam-fonte-botao) * 1.08);
  background-color: hsl(267, 82%, 50%);
  transition: all 0.3s ease-out, transform 0.9s cubic-bezier(0.17, 0.67, 0.76, 0.93);
  height: 12vmin;
  width: 40vmin;
}

.classeAtivo {
  background-color: hsla(267, 81%, 37%, 0.776);
}

.classeInativo {
  background-color: #d0a7f6;
}
</style>
