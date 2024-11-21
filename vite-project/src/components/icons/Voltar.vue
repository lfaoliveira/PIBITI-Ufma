<template>
  <button class="containerSeta">
    <img src="../../assets/seta.png" alt="Seta" id="imagemSeta"> 
    <div class="texto">Voltar</div>
  </button>
</template>

<script>

export default {
  name: "seta",
  created() {},
  data() {
    return {}
  },
  props: {},
};
</script>

<style scoped>
.containerSeta{
  padding: clamp(10px, 2%, 20px);
  border-radius: var(--raio-butao);
  background-color: var(--sec-color);
  display: flex;
  justify-content: center;
  /* gap: clamp(4vmin, 4.5vmin, 5vmin); */
  align-items: center;
  width: auto;
  height: var(--alt-butao);
  box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.29);
  margin: auto 0px;

  cursor: pointer;
}


#imagemSeta{
  aspect-ratio: 4/3;
  width: clamp(25px, 32px, 5vmin);
  height:auto;
  margin-right: clamp(10px,2vmin, 50px);
}

.texto{
  
  position:relative;
  font-size: clamp(10px, 20px, 4vmin);
  color: #fff;
  font-weight: 800;

}



</style>