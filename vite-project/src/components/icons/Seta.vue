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
  border-radius: clamp(10px, 10%, 16px);
  margin-left: 0px;
  background-color: var(--sec-color);
  display: flex;
  justify-content: center;
  gap: clamp(4vmin, 4.5vmin, 5vmin);

  align-items: center;
  width: auto;
  box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.29);
  margin: auto;
  cursor: pointer;
}


#imagemSeta{
  aspect-ratio: 4/3;
  width: 6vmin;
  height:auto;
}

.texto{
  
  position:relative;
  font-size: clamp(1rem, 3vmin, 10vmin);
  color: #fff;
  font-weight: 800;

}



</style>