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
.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.button {
  display: flex;

  justify-content: center;
  align-items: center;

  width: 261px;
  height: 74px;
  border: none;
  border-radius: 40px;
  font-size: 24px;
  font-weight: bold;
  color: white;
  cursor: pointer;

  /* FONTE */
  font-size: clamp(18px, 3vmin, 22px);
}

.classeAtivo {
  background-color: #5c1ab5;
}

.classeInativo {
  background-color: #d0a7f6;
}
</style>
