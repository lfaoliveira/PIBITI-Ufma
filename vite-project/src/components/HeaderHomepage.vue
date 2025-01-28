<template>
  <div class="div-header">
    <img :src="this.path_hamburg" id="imagemHamburguer" alt="Imagem Menu" />
    <div class="cntr-demo">
      <!--  -->
      <button @click="this.clickDemo" id="demo" class="botao-demo">Demonstração</button>
    </div>
  </div>
</template>

<style scoped>
input {
  display: none;
}

.div-header {
  max-width: 80%;
  width: 97vmin;
  position: absolute;
  margin: 0 auto 0 auto;
  height: auto;
  top: 1%;
  z-index: 3;
  gap: 0px;
  display: grid;
  align-items: center;
  grid-template-rows: 50%;
  grid-template-columns: 1fr 1fr;
}

.cntr-demo {
  position: relative;
  text-align: center;
  background-color: #6113c6;
  display: flex;
  width: auto;
  height: 75%;
  align-items: center;
  justify-content: center;
  border-radius: 0.75rem;
  box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.59);
  margin: auto;
  margin-right: 0px;
  align-self: center;
  justify-self: center;
  padding: 0vmin clamp(0%, 3%, 5%);
}

.botao-demo {
  border: none;
  color: white;
  background-color: #6113c6;
  font-family: MontSerrat, Medium;
  position: relative;
  white-space: nowrap;
  font-size: clamp(1.5vmin, 5vmin, 22px);
  font-weight: 500;
  letter-spacing: 0;
  align-items: center;
  display: flex;
  justify-content: center;
  text-align: center;
  width: 100%;
  height: 100%;

  cursor: pointer;
}

#imagemHamburguer {
  background-color: #6113c6;
  border-radius: clamp(10px, 3%, 15px);
  width: clamp(5vmin, 60px, 11vmin);
  height: auto;
  margin: auto;
  box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.59);
  justify-self: center;
  margin-left: 0px;
  padding: clamp(10px, 2%, 20px);
}
</style>

<script>
import path from "path";

export default {
  name: "HeaderHomepage",
  data() {
    return {
      path_hamburg: path.join(".", "src", "assets", "menu-sanduiche.png"),
    };
  },
  methods: {
    clickDemo() {
      this.$router.push({
        name: "analiseVideo",
        query: { idVideoAnalise: -1 },
      });
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
    styleTexto() {
      return {
        top: `${25}%`,
        left: `${10}%`,
        width: `${50}%`,
        height: `${50}%`,
      };
    },
  },
  mounted() {
    window.addEventListener("resize", this.styleHamburguer);
  },
};
</script>
