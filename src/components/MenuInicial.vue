<template>
  <div class="div-menu-hamburguer" :style="styleHamburguer">
    <img :src="path_hamburg" alt="MENU HAMBURGUER" />
    <div class="text-wrapper">Menu</div>
  </div>
</template>

<script>
import path from "path";

export default {
  data() {
    return {
      path_hamburg: path.join(".", "src", "assets", "menu-sanduiche.svg"),
    };
  },
  computed: {
    styleHamburguer(){
      const divMenuHamburguer = document.getElementsByClassName("div-menu-hamburguer");
      const con_w = window.innerWidth;
      const con_h = window.innerHeight;
      const pos_h = (con_w - divMenuHamburguer.offsetWidth) * 0.01;
      const pos_v = (con_h - divMenuHamburguer.offsetHeight) * 0.1;
      return {
        left: `${pos_h}%`,
        top: `${pos_v}%`,
        width: `$ 10%`,
        height: `$ 10%`,
        lineHeight: `10%`,

      };
    },
  },
};
</script>

<style scoped>
.div-menu-hamburguer {
  position: absolute;
  flex: 0.01;


}
.text-wrapper{
  color: #ffffff;
  font-family: "Inter-Black", Helvetica;
  font-size: 32px;
  font-weight: 700;
  left: 5rem;
  letter-spacing: 0;
  line-height: normal;
  position: absolute;
  top: 1.35rem;
}
</style>
