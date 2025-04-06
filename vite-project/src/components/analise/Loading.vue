<template>
  <HeaderAnal></HeaderAnal>
  <h1 class="page-title">Etapa {{ this.cont }} de 3: {{ this.tituloAtual }}</h1>

  <main class="secao-main">
    <figure class="overlay">
      <section class="progresso">
        <div class="progresso-barra">
          <div class="progresso-barra barra-menor"></div>
        </div>
        <div class="progresso-texto">{{ parseInt(this.percent) }}% Completo</div>
      </section>
    </figure>
    <p>{{ responseData }}</p>
  </main>

  <Rodape class="rodape"></Rodape>
</template>

<script>
import Rodape from "../auxiliares/Rodape.vue";
import axios from "axios";

export default {
  name: "Test",
  components: {
    Rodape,
  },
  created() {},
  data() {
    return {
      percent: 0,
      cont: 2,
      tituloAtual: "Carregando Vídeo",
    };
  },
  props: {
    responseData: {
      required: true,
    },
    //estimativa em milisegundos
    estimativaTotal: 30 * 1000,
  },
  watch: {
    responseData: {
      async handler(newVal) {
        if (newVal) {
          if (this.cont === 2) {
            this.percent = 50;
            document.dispatchEvent(new Event("update"));
            const formData = new FormData();
            formData.append("id_diag", newVal.id_diag);
            formData.append("filename", String(newVal.filename));

            console.log(`RES: ${this.responseData} CONT: ${this.cont}`)
            
            const res = await axios.post(
              this.$store.getters.getAnalise,
              formData,
              {
                withCredentials: true,
              }
            );
            this.responseData = res.data;
            this.cont += 1;
        } else if (this.cont === 3) {
            let startTime = Date.now();
            let interval = setInterval(() => {
                document.dispatchEvent(new Event("update"));
                let elapsedTime = Date.now() - startTime;
                this.percent = Math.min(
                    (elapsedTime / estimativaTotal) * 100,
                    99.9
                ).toFixed(2);
              if (elapsedTime >= estimativaTotal) {
                clearInterval(interval);
              }
            }, 15);
          }
          
        }
      },
      immediate: true,
    },
  },
  methods: {
    moverBarra() {
      const barraAtual = document.querySelector(".barra-menor");
      if (barraAtual) barraAtual.style.width = `${this.percent}%`;
    },
  },
  async mounted() {
    console.log("MOUNTED RESPONSE: ", this.responseData)
    document.addEventListener("update", this.moverBarra);
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
