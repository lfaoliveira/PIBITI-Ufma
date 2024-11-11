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
  font-family: Montserrat, 'Inter';
  border: 0px;
}
input{
  display:none;
}

.div-header {
  max-width: 80%;
  margin: 0 auto 0 auto;
  height: auto;
  top: 0%;
  left: 0px;
  z-index: 1;
  gap: clamp(80vmin, 90vmin, 100vmin);
  display: grid;
  align-items: center;
  grid-template-rows: 50% ;
  grid-template-columns: 1fr 1fr;
}


.salvar{
  background-color: #6113c6;
  display: grid;
  justify-content: center;
  align-items: center;
  margin: auto;
  width: auto;
  height: auto;

  grid-template-rows: 1fr ;
  grid-template-columns: 1fr 1fr;
  border-radius: clamp(10px, 10%, 16px);
  box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.29);
}

.icone-download{
  border-radius: clamp(10px, 3%, 15px);
  width: clamp(5vmin, 60px, 11vmin);
  height: auto;

  /* box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.59); */
  justify-self: start;
  margin-left: 0px;
  padding: clamp(3px, 4px, 6px);
}

.texto-salvar{
  color: #fff;
  font-weight: 800;
  margin: auto;
  
  font-size: clamp(1rem, 3vmin, 10vmin);
  justify-self: start;
  width: max-content;

}
</style>