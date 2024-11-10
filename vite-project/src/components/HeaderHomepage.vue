<template>
  <div class="div-header">
    <img :src="this.path_hamburg" id="imagemHamburguer" alt="Imagem Menu">
    <div class="cntr-demo">
      <input type="file" id="fileInput" accept="video/*">
      <label for="fileInput" ref="" class="botao-demo">
        Demonstração
      </label>
    </div>    
  </div>
</template>

<script>
import path from "path";

export default {
  name: "HeaderHomepage",
  data() {
    return {
      path_hamburg: path.join(".", "src", "assets", "menu-sanduiche.png"),
      scaleFactor:  1,
    };
  },
  methods: {
    getScalFactor(){
      return this.scaleFactor;
    },
    setScaleFactor(valor){
      this.scaleFactor = valor;
    },
  },
  computed: {
  /*  styleImagem() {
      return {
        aspectRatio: `${1/1}`,
        width: `auto`,
        height: `auto`,
        left: `${3}vw`,
        top: `${25}vh`,
      };
    }, */ 
    styleTexto(){
      return {
        top: `${25}%`,
        left: `${10}%`,
        width: `${50}%`,
        height: `${50}%`,
      };
    },
  },
  mounted() {
    window.addEventListener('resize', this.styleHamburguer);
    
  }
};
</script>

<style scoped>
input{
  display:none;
}

.div-header {
  max-width: 90%;
  width: auto;
  position: absolute;
  margin: 0 auto 0 auto;
  height: auto;
  top: 0%;
  z-index: 1;
  display: flex;
  gap: 50vw;
  justify-content: space-between;
  align-items: center;
  flex-direction: row;
  justify-self: center;
}

.cntr-demo{
  margin: auto;
  margin-right: 0%;
  position: relative;
  text-align: center;
  background-color: #6113c6;
  display: flex;
  width: clamp(50px, 200px, 200px);
  height: auto;
  align-items: center;
  justify-content: center;
  border-radius: 0.75rem;
  box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.59);
}

.botao-demo{
  border: none;
  color: white;
  position: relative;
  white-space: nowrap;
  font-size: 20px;
  letter-spacing: 0;
  align-items: center;
  display: flex;
  justify-content: center;
  text-align: center;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

#imagemHamburguer{
  background-color: #6113c6;
  border-radius: 0.5rem;
  width: 45px;
  height: auto;
  margin: auto;
  margin-top: 0px;
  margin-bottom: 0px;
  margin-left: 0vmin;
  box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.59);
}

</style>



