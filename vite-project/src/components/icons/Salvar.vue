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
  display: flex;
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
  margin: 0px 0px clamp(2px, 0.5vmin, 10px) 0px;
  /* margin-right: clamp(15px, 20px, 28px); */
  padding: clamp(1px, 3px, 6px);
}

.texto-salvar{
  color: #fff;
  font-weight: 800;
  margin: auto;
  /* margin: 0px 0px 0px clamp(2px, 4px, 10px) ; */
  width: clamp(8ch, 9.92vmax, 14ch);
  padding: 0px 0.5ch;
  font-size: clamp(8px, 4vmin, 16px);
  justify-self: start;
  align-self: start;
}
</style>