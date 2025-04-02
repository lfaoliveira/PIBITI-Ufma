<template>
  <HeaderAnal></HeaderAnal>
  <h1 class="page-title">Análise de Paralisia</h1>

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

//estimativa em milisegundos
let estimativaTotal = 20 * 1000;

export default {
  name: "Test",
  components: {
    Rodape,
  },
  created() {},
  data() {
    return {
      percent: 0,
    };
  },
  props: {
    idAnalise: "",
  },
  methods: {
    moverBarra() {
      const barraAtual = document.querySelector(".barra-menor");
      if (barraAtual) barraAtual.style.width = `${this.percent}%`;
    },
  },
  async mounted() {
    await this.$nextTick();
    document.addEventListener("update", this.moverBarra);

    let startTime = Date.now();
    let interval = setInterval(() => {
      document.dispatchEvent(new Event("update"));
      let elapsedTime = Date.now() - startTime;
      this.percent = Math.min((elapsedTime / estimativaTotal) * 100, 99.9).toFixed(2);

      if (elapsedTime >= estimativaTotal) {
        clearInterval(interval);
      }
    }, 15);
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
