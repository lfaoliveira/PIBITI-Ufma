<template>
    <HeaderSistema :activeIndex="4" />
    <h1 class="page-title">Etapa {{ this.cont }} de 3: {{ this.tituloAtual }}</h1>
    <OverlayAviso
        class="overlay-aviso"
        :eventoAviso="this.erroOverlay"
        :titulo="msgErro"
        :subtexto="'Tente novamente!'"
        :srcImg="'src/assets/alert_circle.png'"
        :rota="'/teste'"
    />
    <main class="secao-main">
        <figure class="overlay">
            <section class="progresso">
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
                        class="w-14 h-14 border-3 border-[#792359] border-t-transparent rounded-full animate-spin"
                    />
                </div>
                <div class="progresso-texto">Carregando...</div>
            </section>
            <Estrela></Estrela>
        </figure>
    </main>

    <Rodape class="rodape"></Rodape>
</template>

<script>
import Rodape from "../layout/Rodape.vue";
import axios from "axios";
import HeaderSistema from "../layout/HeaderSistema.vue";
import OverlayAviso from "../layout/OverlayAviso.vue";
import Estrela from "../icons/Estrela.vue";

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
        //BUG: Uncaught (in promise) SyntaxError: Unexpected token 'T', "Task compl"... is not valid JSON
        //AJEITAR ISSO PRA CONTINUAR DESENVOLVENDO!!!!!!!!!!!!!
        async checkTaskStatus(taskId, intervaloMS) {
            return new Promise((resolve, reject) => {
                const interval = setInterval(async () => {
                    try {
                        const res = await fetch(
                            this.$store.getters.getTaskStatus + `${taskId}`
                        );
                        const response = await res.json();
                        const codigo = res.status;

                        // Task completed successfully
                        if (codigo === 200 && response.message == "SUCCESS") {
                            clearInterval(interval);
                            resolve(response); // {status: "SUCCESS", result: ...}
                        }

                        // Task still pending
                        else if (codigo === 304) {
                            // do nothing, keep polling
                            console.log("ESPERANDO");
                        }

                        // Task failed
                        else if (codigo === 500 || response.message === "FAILURE") {
                            clearInterval(interval);
                            const err = new Error(response.error || "Task failed");
                            console.log("ERRO " + String(err));
                            reject(err);
                        }

                        //  Task ID not found
                        else if (codigo === 404) {
                            clearInterval(interval);
                            console.log("ERRO " + String(err));
                            const err = new Error("Task not found");
                            reject(err);
                        }

                        //  Unexpected status
                        else {
                            clearInterval(interval);
                            const err = new Error(
                                `Unexpected response: ${JSON.stringify(response)}`
                            );
                            console.log("ERRO " + String(err));
                            reject(err);
                        }
                    } catch (err) {
                        clearInterval(interval);
                        console.log("ERRO " + String(err));
                        reject(err);
                    }
                }, intervaloMS); // poll every X ms
            });
        },

        async esperarUploadVideo(taskId) {
            const intervalo = 500; //500ms
            console.log("BOTANDO PRA ESPERAR");
            const res = await this.checkTaskStatus(taskId, intervalo);
            console.log("DEU CERTO");
            //retorna tag dados retornada pelo servidor
            return res.dados;
        },

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
        // const signal = controller.signal;

        let res = "None";

        const promiseEnviaDiag = axios.post(this.$store.getters.getDiag, formDiag, {
            withCredentials: true,
        });

        try {
            res = await promiseEnviaDiag;
            this.objResposta = res.data;
            console.log(
                "TAREFA INICIADA COM SUCESSO!: " + JSON.stringify(this.objResposta)
            );
        } catch (error) {
            this.msgErro = res.data; //data eh mensagem de erro vindo do servidor
            console.log("DEU MERDA: " + JSON.stringify(this.msgErro));
            emitter.emit(this.erroOverlay);
        }

        console.log("MOUNTED RESPONSE: ", this.objResposta);
        const taskId = this.objResposta?.task_id;
        await this.esperarUploadVideo(taskId);
        console.log("MANDANDO PRA ANALISE");
        //logica de barra de progresso e req de analise
        // this.mudarLoading(controller);
        //1 MB = 1s
        /* await this.progressoIntervaloMs(
            this.estimativaTotal - tempoLoad + sizeMB,
            100,
            signal
        ); */
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
