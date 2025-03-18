<template>
  <div class="button-container">
    <button v-if="ativo" class="button classeAtivo">{{ texto }}</button>
    <button v-if="!ativo" class="button classeInativo">{{ texto }}</button>
  </div>
</template>

<script>
export default {
  name: "botaoPequeno",
  methods: {},
  props: {
    ativo: false,
    texto: "",
  },
  created() {},
};
</script>

<style lang="scss" scoped>
.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.button {
  width: 300px;
  height: 80px;
  border: none;
  border-radius: 40px;
  font-size: 24px;
  font-weight: bold;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.classeAtivo {
  background-color: #5c1ab5;
}

.classeInativo {
  background-color: #d0a7f6;
}
</style>
