<template>
  <section class="secao-landing">
    <!-- TODO: AJEITAR HEADER E SECAO INICIAL -->
    <headerHome />
    <div class="conteudo-secao">
      <div id="div-video-home">
        <!-- ADICIONAR AUTOPLAY E LOOP PRA TER O RESULTADO FINAL -->
        <div class="overlay"></div>
        <video alt="Header background" class="video-background" autoplay loop  src="../assets/video-oftalmo.mp4"/>
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
*{
  --height-video: 100%;
}

.secao-landing {
  display: flex;
  align-items: center;
  width: 100%;
  height: var(--height-video);
  justify-content: center;
  margin-top: 0px;
  align-self: center;
  flex-wrap: wrap;
  margin: 0px;
  max-width: 100%;

}

#div-video-home {
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

.overlay{
  width: 100%;
  height: 100%;
  position: absolute;
  z-index: 4;
  background-color: rgba(68,68,68.1,0.51);
}



.video-background {
  width: 100%;
  height: var(--height-video);
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
  width: 98%;
  height: 98vh;
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
  width: clamp(290px,59ch, 100%);
  margin: 0vmin auto;
  margin-top: clamp(10vmin, 13vmin, 17vmin);
  --fonte-titulo: clamp(14px, 5.33vmin, 41px);
}

#titulo {
  color: #fff;
  font-weight: 600;
  font-size: var(--fonte-titulo);
  text-align: start;
  width: auto;
  margin: 0vmin auto;
}

.cntr-cta {
  margin: clamp(30px, 8vmin, 80px) auto 0vmin auto;
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
  font-size: clamp(1.5vmin, 5vmin, 22px);
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
  margin: 10vmin auto 0vmin auto;
  align-self: flex-start;
  width: clamp(54px, 10vmin,120px);
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
  width: clamp(50px, 8vmin, 10vmin);
  margin-top: -5vh;
  margin-bottom: clamp(0vh, 0vh, 3vh);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.seta-baixo {
  margin: auto;
  width: 100%;
}

</style>