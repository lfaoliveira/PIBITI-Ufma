<template>
  <HeaderSistema :activeIndex="4" />
  <h1 class="page-title">Etapa {{ this.cont }} de 3: {{ this.tituloAtual }}</h1>
  <OverlayAviso
    :eventoAviso="erroOverlay"
    :titulo="msgErro"
    :subtexto="'Tente novamente!'"
    :srcImg="'src/assets/alert_circle.png'"
  />
  <main class="secao-main">
    <figure class="overlay">
      <section class="progresso">
        <div class="progresso-barra">
          <div class="progresso-barra barra-menor"></div>
        </div>
        <div class="progresso-texto">{{ parseInt(this.percent) }}% Completo</div>
      </section>
    </figure>
  </main>

  <Rodape class="rodape"></Rodape>
</template>

<script>
import Rodape from "../auxiliares/Rodape.vue";
import axios from "axios";
import HeaderSistema from "../auxiliares/HeaderSistema.vue";
import OverlayAviso from "../auxiliares/OverlayAviso.vue";

import emitter from "../../eventBus";

const erroOverlay = "erroServidor";

export default {
  name: "loading",
  components: {
    Rodape,
    HeaderSistema,
    OverlayAviso,
  },
  created() {},
  data() {
    return {
      percent: 0,
      cont: 2,
      tituloAtual: "Carregando Vídeo",
      objResposta: null,
      msgErro: "",
    };
  },
  props: {
    //estimativa em milisegundos
    estimativaTotal: 30 * 1000,
  },
  methods: {
    moverBarra() {
      const barraAtual = document.querySelector(".barra-menor");
      if (barraAtual) barraAtual.style.width = `${this.percent}%`;
    },
    async mudarLoading() {
      this.cont += 1;
      this.tituloAtual = "Processando Vídeo";
      this.percent = 50;
      document.dispatchEvent(new Event("update"));
      const formData = new FormData();
      formData.append("id_diag", this.objResposta.id_diag);
      formData.append("filename", String(this.objResposta.filename));

      console.log(`RES: ${this.objResposta} CONT: ${this.cont}`);
      try {
        const res = await axios.post(this.$store.getters.getAnalise, formData, {
          withCredentials: true,
        });
        this.objResposta = res.data;
        let startTime = Date.now();
        let interval = setInterval(() => {
          document.dispatchEvent(new Event("update"));
          let elapsedTime = Date.now() - startTime;
          this.percent = Math.min(
            (elapsedTime / this.estimativaTotal) * 100,
            99.9
          ).toFixed(2);
          if (elapsedTime >= this.estimativaTotal) {
            clearInterval(interval);
          }
        }, 15);
      } catch {
        emitter.emit(erroOverlay);
      }
    },
  },
  async mounted() {
    this.objResposta = this.$store.getters.getAnalResponseData;

    console.log("MOUNTED RESPONSE: ", this.objResposta);
    document.addEventListener("update", this.moverBarra);
    const a = await this.mudarLoading();
  },
};
</script>

<style scoped>
.page-title {
  color: #3a0d75;
  font-size: clamp(39px, 2.5em, 4vmin);
  margin: clamp(30px, 6vmin, 120px) auto 0px auto;
}

.secao-main {
  height: 80vmin;
}

.overlay {
  transition-duration: 4ms;
  background-color: black;
  width: auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.progresso {
  color: white;
  width: clamp(110px, 30vmin, 400px);
  height: auto;
}

.progresso-barra {
  background-color: #f0f0f0;
  height: clamp(10px, 2vmin, 20px);
  width: 100%;
  border-radius: 12px;
  margin: 10px 0;
}

.barra-menor {
  margin: 0px;
  padding: 0px;
  background-color: #792359;
  height: 100%;
  width: 2%;
  border-radius: 12px;
}

.progresso-texto {
  display: flex;
  justify-content: center;
}
</style>
