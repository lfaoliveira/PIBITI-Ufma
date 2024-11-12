<template>
    <div class="div-header">
    <Seta></Seta>
    <button class="salvar">
      <img  class="icone-download" alt="Save icon" src="../assets/download.png" />
      <p class="texto-salvar">Salvar Resultado</p>
    </button>
  </div>
</template>

<script>
import Seta from "./icons/Seta.vue"
export default {
  name: "Test",
  components: {
    Seta,
  },
  created() {},
  data() {
    return {};
  },
  props: {},
  methods: {},
};
</script>

<style scoped>
*{
  --alt-butao: clamp(40px, 50px, 70px);
  --raio-butao: clamp(10px, 28%, 16px);
  font-family: 'Montserrat', 'Inter';
  border: 0px;
}
input{
  display:none;
}

.div-header {
  max-width: 80%;
  position: absolute;
  margin: 1vmin auto 0 auto;
  height: auto;
  width: max-content;
  gap: clamp(10%, 200px, 50%);
  z-index: 1;
  display: grid;
  align-items: center;
  grid-template-rows: 1fr;
  grid-template-columns: 1fr 1fr;
}


.salvar{
  background-color: #6113c6;
  display: grid;
  justify-content: center;
  align-items: center;
  margin: auto;
  width: min-content;
  height: var(--alt-butao);

  grid-template-rows: 1fr;
  grid-template-columns: 1fr 1fr;
  border-radius: var(--raio-butao);
  box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.39);
  cursor: pointer;
}

.icone-download{
  border-radius: clamp(10px, 3%, 15px);
  width: clamp(5vmin, 45px, 11vmin);
  height: auto;

  /* box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.59); */
  justify-self: start;
  margin-left: clamp(2px, 5px, 2vmin);
  margin-right: clamp(15px, 20px, 28px);
  padding: clamp(3px, 4px, 6px);
}

.texto-salvar{
  color: #fff;
  font-weight: 800;
  margin: auto;
  margin-right: 2vmin;

  
  font-size: clamp(10px, 18px, 22px);
  justify-self: start;
  width: max-content;

}
</style>