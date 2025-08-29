<template>
    <HeaderSistema :activeIndex="4" />
    <h1 class="page-title">Etapa {{ this.cont }} de 3: {{ this.tituloAtual }}</h1>
    <OverlayAviso
        class="overlay-aviso"
        :eventoAviso="this.erroOverlay"
        :titulo="msgErro"
        :subtexto="'Tente novamente!'"
        :srcImg="'src/assets/alert_circle.png'"
        :rota="'/ficha'"
    />
    <main class="secao-main">
        <figure class="overlay">
            <section class="progresso">
                <div class="progresso-barra">
                    <!-- <div
                        class="progresso-barra barra-menor"
                        :style="{ width: `${percent}%` }"
                    ></div> -->
                    <div
                        role="status"
                        aria-label="Carregando"
                        class="flex items-center justify-center"
                    >
                        <div
                            class="w-12 h-12 border-4 border-[#792359] border-t-transparent rounded-full animate-spin"
                        />
                        <span class="sr-only">Carregando...</span>
                    </div>
                </div>
                <div class="progresso-texto">{{ parseInt(this.percent) }}% Completo</div>
            </section>
        </figure>
    </main>

    <Rodape class="rodape"></Rodape>
</template>

<script>
import Rodape from "../layout/Rodape.vue";
import axios from "axios";
import HeaderSistema from "../layout/HeaderSistema.vue";
import OverlayAviso from "../layout/OverlayAviso.vue";

import emitter from "../../eventBus";

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
            erroOverlay: "erroServidor",
            estimativaTotal: 30 * 1000, //estimativa em milissegundos
        };
    },
    props: {},
    methods: {
        async progressoIntervaloMs(tempoTotalms, targetPercent, signal) {
            return new Promise((resolve, reject) => {
                const startTime = Date.now();
                const initialPercent = Number(this.percent);
                const percentDifference = Number(targetPercent) - initialPercent;

                const interval = setInterval(() => {
                    const elapsedTime = Date.now() - startTime;
                    const progress = Math.min(elapsedTime / Number(tempoTotalms), 1);
                    if (progress >= 1) {
                        clearInterval(interval);
                        resolve();
                    } else if (signal.aborted) {
                        this.percent = targetPercent;
                        reject();
                    }
                    this.percent = Number(initialPercent + progress * percentDifference);
                }, (1 / 200) * tempoTotalms);
                // Listen for the abort event
                signal.addEventListener("abort", () => {
                    reject();
                });
            });
        },

        async mudarLoading(controller) {
            this.cont += 1;
            this.tituloAtual = "Processando Vídeo";
            //
            // document.dispatchEvent(new Event("update"));
            const formData = new FormData();
            formData.append("id_diag", this.objResposta.id_diag);
            formData.append("filename", String(this.objResposta.filename));
            formData.append("nome_input", String(this.objResposta.nome_input));

            axios
                .put(this.$store.getters.getAnalise, formData, {
                    withCredentials: true,
                })
                .then((res) => {
                    this.objResposta = res.data;
                    console.log(this.objResposta);
                    controller.abort();
                    this.$router.push({
                        name: "analiseVideo",
                        query: {
                            id_diag: this.objResposta.id_diag,
                            responseStringJson: JSON.stringify(res.data), // Add response data to query
                        },
                    });
                })
                .catch((error) => {
                    this.msgErro = error.response.data;
                    emitter.emit(this.erroOverlay);
                    console.error(error, " Requisicao de analise falhou");
                });
        },
    },
    async mounted() {
        // TODO: adaptar pra nova estrutura de backend
        // NOTE: precisa modificar toda a estrutura de estilização pra usar roda de carregamento do tailwind
        const formDiag = this.$store.getters.getFormDiag;
        console.log("FORM: ", formDiag, typeof formDiag);

        const controller = new AbortController();
        const signal = controller.signal;

        let res = "None";

        const promiseEnviaDiag = axios.post(this.$store.getters.getDiag, formDiag, {
            withCredentials: true,
        });

        try {
            res = await Promise.all([
                // this.progressoIntervaloMs(tempoLoad, 50, signal),
                promiseEnviaDiag,
            ]);
            this.objResposta = res[1].data;
            console.log("RESPOSTA BEM SUCEDIDA: ");
        } catch (error) {
            this.msgErro = res.data; //data eh mensagem de erro vindo do servidor
            emitter.emit(this.erroOverlay);
        }

        console.log("MOUNTED RESPONSE: ", this.objResposta);
        //logica de barra de progresso e req de analise
        this.mudarLoading(controller);
        //1 MB = 1s
        await this.progressoIntervaloMs(
            this.estimativaTotal - tempoLoad + sizeMB,
            100,
            signal
        );
    },
};
</script>

<style scoped>
@tailwind base;
@tailwind components;
@tailwind utilities;

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
.overlay-aviso {
    margin: 2vmin 0vmin;
    align-self: center;
    background: white;
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
    transition: width 0.3s ease-out;
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
