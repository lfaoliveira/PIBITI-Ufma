<template>
  <section class="secao-landing">
    <!-- TODO: AJEITAR HEADER E SECAO INICIAL -->
    <headerHome />
    <div class="conteudo-secao">
      <div id="div-imagem">
        <img alt="Header background" class="img-background" src="https://cdn.builder.io/api/v1/image/assets/TEMP/f3ca9b3d261c46282ed04ff940f4cc22606eb7e3ebb989886eb51637d0e210fe?placeholderIfAbsent=true&apiKey=8b29090e827e422ea4601ed102c7c8ec"/>
      </div>
      <div class="div-titulo">
        <h1 class="section-title" id="titulo">
          Software de Análise de Vídeos de Paralisia do Sexto Nervo Óptico
        </h1>
      </div>
      <div class="cntr-cta">
        <input type="file" id="fileInput" accept="video/*" />
        <label for="fileInput" ref="" class="label-cta"> Analisar Vídeo </label>
      </div>
      <div class="div-mouse-animado">
        <img
          src="https://cdn.builder.io/api/v1/image/assets/TEMP/ae6f73a5d07025b884e2d477e8c31f66eac96b6f490dead53be2a993c4e98f4a?placeholderIfAbsent=true&apiKey=8b29090e827e422ea4601ed102c7c8ec"
          class="mouse-animado"
        />
      </div>
      <div class="div-seta-baixo">
        <img
          src="https://cdn.builder.io/api/v1/image/assets/TEMP/7ad9eb0a053b1dfcf3e7e3fa37d9161add87b3e60570b5405f7e6d1c6c7a7f28?placeholderIfAbsent=true&apiKey=8b29090e827e422ea4601ed102c7c8ec"
          alt="Decorative element"
          class="seta-baixo"
        />
      </div>
    </div>
  </section>
</template>


<script>
import headerHome  from "./HeaderHomepage.vue";
export default {
  name:"Landing",
  components: {
    headerHome,
  },
  props: {  },
  data() {
    return {
      _: 0,
    };
  }
}
</script>
<style scoped>

.secao-landing {
  display: flex;
  align-items: center;
  width: 100%;
  height: 100%;
  justify-content: center;
  margin-top: 0px;
  align-self: center;
  flex-wrap: wrap;
  margin: 0px;
  max-width: 100%;

}

#div-imagem {
  position: absolute;
  width: clamp( 92%, 95%, 98%);
  display: flex;
  align-self: center;
  height: 100%;
  /* margin: 5vmin 0vmin 0vmin 0vmin; */
  top: 0px;
  flex-wrap: wrap;
  justify-content: start;

}

.img-background {
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
  align-self: center;  
}


/* MUDAR CONTAINER PRA GRID */
.conteudo-secao {
  align-self: center;
  display: flex;
  flex-wrap: wrap;
  flex-flow: column wrap;
  width: 75%;
  height: 90vh;
  margin-top: 10vmin;
  justify-content: space-between;
  align-content: center;
}

.div-titulo {
  margin: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  height: auto;
  width: 42%;
  margin: 0vmin auto 1vmin auto;
}

#titulo {
  color: #fff;
  font-weight: 700;
  font-size: clamp(20px, 35px, 60px);
  text-align: start;
  width: auto;
  margin: 0vmin auto;
}

.cntr-cta {
  margin: 35vmin auto 0vmin auto;
  background-color: #6113c6;
  position: relative;
  display: flex;
  border-radius: 59px;
  align-items: center;
  justify-content: center;
  box-shadow: 0px 0.45vmin 8px 0px rgba(0, 0, 0, 0.59);
  padding: clamp(1px, 4px, 10px) clamp(6px, 19px, 22px);
}

.label-cta {
  border: none;
  font-size: clamp(2vmin, 18px, 20px);
  font-family: MontSerrat, Bold;
  color: #fff;
  cursor: pointer;
  width: auto;
}

input {
  display: none;
}

.div-mouse-animado {
  aspect-ratio: 4/3;
  display: flex;
  align-items: center;
  justify-items: center;
  margin: auto;
  margin-top: 10vmin;
  margin-bottom: 0vmin;
  align-self: flex-start;
  width: 66px;
  height: auto;
  position: relative;
}

.mouse-animado {
  aspect-ratio: 4/3;
  width: 100%;
  height: auto;
  position: relative;
}
.div-seta-baixo {
  margin: auto;
  align-self: center;
  margin-top: -1vh;
  margin-bottom: 0px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.seta-baixo {
  margin: auto;
  width: 8vmin;
}

</style>