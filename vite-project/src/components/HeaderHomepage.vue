<template>
  <div class="div-menu-hamburguer" :style="styleHamburguer">
    <img :src="this.path_hamburg" :style="styleImagem" id="imagemHamburguer" alt="Imagem Menu">
    <div class="text-wrapper" :style="styleTexto">Menu</div>
    <div class="botao-demo"> Demonstração</div>
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
        left: `${3}vw`,
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
.div-menu-hamburguer {
  display: inline-flex;
  position: absolute;
  flex-direction: row;
}

.text-wrapper{
  --menu-font-size: 2rem;
  color: #001B2C;
  justify-content: center;
  align-items: center;
  font-size: clamp(1rem, var(--menu-font-size), 10vmin);
  font-weight: 600;
  display: inline-flex;
  letter-spacing: 0;
  line-height: normal; 
  position: relative;
}
</style>



