<template>
  <div class="div-menu-hamburguer" :style="styleHamburguer">
    <img :src="this.path_hamburg" :style="styleImagem" id="imagemHamburguer" alt="Imagem Menu">
    <div class="wrapper">
      <label for="botao-demo" ref="" class="custom-file-upload" :style="estiloUpload">
        Analisar Vídeo
      </label>
      <button class="botao-demo"> </button>
    </div>
  </div>
  <!--ADICIONAR ABA DE CONFIGURACOES -->
</template>

<script>
import path from "path";

export default {
  name: "MenuLateral",
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
    styleHamburguer() {
      return {
        width: `${12}%`,
        height: `${10}%`,
        left: `${30}vw`,
        top: `${25}vh`,
      };
    },
    styleImagem() {
      return {
        aspectRatio: `${1/1}`,
        width: `auto`,
        height: `auto`,
        left: `${3}vw`,
        top: `${25}vh`,
      };
    },
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
.botao-demo{
  border-radius: 51px;
  border: none;
  color: black;        
  position: relative;
  white-space: nowrap;
  letter-spacing: 0;
  align-items: center;
  display: flex;
  justify-content: center;
  text-align: center;
  width: 100%;
  height: 100%;
}

.div-menu-hamburguer {
  display: inline-flex;
  position: absolute;
  flex-direction: row;
}

</style>



