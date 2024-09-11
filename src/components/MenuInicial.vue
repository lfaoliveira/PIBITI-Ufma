<template>
  <div class="div-menu-hamburguer" :style="styleHamburguer">
    <svg id="imagemHamburguer" width="74" height="80" viewBox="0 0 74 80" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M9.25 60V53.3333H64.75V60H9.25ZM9.25 43.3333V36.6667H64.75V43.3333H9.25ZM9.25 26.6667V20H64.75V26.6667H9.25Z" fill="#FFF9FF"/>
    </svg>
    <div class="text-wrapper" :style="styleTexto">Menu</div>
  </div>
</template>

<script>
import path from "path";

export default {
  name: "MenuInicial",

  data() {
    return {
      path_hamburg: path.join(".", "src", "assets", "menu-sanduiche.svg"),
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
      const divMenuHamburguer = document.getElementsByClassName("div-menu-hamburguer");
      
      return {
        width: `${10}%`,
        height: `${10}%`,
        left: `${3}vw`,
        top: `${25}vh`,
      };
    },
    styleTexto(){
      return {
        top: `${25}%`,
        left: `${2}vmin`,
        width: `${50}%`,
        height: `${50}%`,
      };
    },
  },
  mounted() {
    window.addEventListener('resize', this.styleHamburguer);
    const svg = document.getElementById('imagemHamburguer');
    svg.setAttribute('viewBox', `0 0 ${100 / this.scaleFactor} ${100 / this.scaleFactor}`);
    
  }
};
</script>

<style scoped>
.div-menu-hamburguer {
  display: inline-flex;
  position: absolute;
  flex-direction: row;
  width: 50%;
  height: auto;
}

#imagemHamburguer{
  width: 50%;
}

.text-wrapper{
  color: #ffffff;
  font-family: "Inter-Black", Helvetica;
  justify-content: center;
  align-items: center;
  font-size: 3vmin;
  font-weight: 700;
  display: inline-flex;
  letter-spacing: 0;
  line-height: normal; 
  position: relative;
}
</style>



