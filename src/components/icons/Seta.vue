<template>
  <div class="containerSeta">
    <img :src="this.path_seta" alt="Imagem Seta" id="imagemSeta"> 
    <div class="texto">Voltar</div>
  </div>
</template>

<script>
import path from "path";

export default {
  name: "Seta",
  created() {},
  data() {
    return {
      path_seta: path.join("src", "assets", "arrow.png")
    };
  },
  props: {},
};
</script>

<style scoped>
#imagemSeta{
  aspect-ratio: 4/3;
  width: 6vmin;
  height:auto;
}
#imagemSeta:hover{
  width: 8vmin;
  height: auto;
}

.texto{
  --seta-font-size: 2vmin;
  position:relative;
  left: 4vmin;
  font-size: clamp(1rem, var(--seta-font-size), 10vmin);
  color: #001B2C;
  font-weight: 700;

}

.containerSeta{
  display: flex;
  justify-content: center;
  align-items: center;
  width: max-content;
}

</style>