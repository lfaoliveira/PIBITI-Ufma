<template>
  <button class="salvar">
    <img  class="icone-download" alt="Save icon" src="../../assets/download.png" />
    <p class="texto-salvar">Salvar Resultado</p>
  </button>
</template>

<script>
export default {
  name: "salvar",
  created() {},
  data() {
    return {};
  },
  props: {},
  methods: {},
};
</script>

<style scoped>

.salvar{
  background-color: #6113c6;
  display: grid;
  justify-content: center;
  align-items: center;
  margin: auto;
  max-width: 50%;
  width: clamp(110px, 30vmin, 203px);
  height: var(--alt-butao);
  margin-right: 0px;
  grid-template-rows: 1fr;
  grid-template-columns: 1fr 1fr;
  border-radius: var(--raio-butao);
  box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.39);
  cursor: pointer;
}

.icone-download{
  border-radius: clamp(10px, 3%, 15px);
  width: clamp(30px, 5vmin, 8vmin);
  height: auto;

  /* box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.59); */
  justify-self: start;
  margin-left: clamp(3px, 15px, 2vmin);
  /* margin-right: clamp(15px, 20px, 28px); */
  padding: clamp(1px, 3px, 6px);
}

.texto-salvar{
  color: #fff;
  font-weight: 800;
  margin: auto;
  margin-right: 2vmin;
  font-size: clamp(10px, 16px, 4vmin);
  justify-self: start;
  width: clamp(8ch, 27vmin, 14ch);
}
</style>