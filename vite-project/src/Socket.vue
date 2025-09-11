<template>
    <section class="frame-pagina">
        <HeaderSistema :activeIndex="4" />
        <!-- <button class="relative bg-amber-500 m-5 mr-5" @click.self="openPopup">
            ABRIR
        </button>
         -->
        <button @click="teste_WS">TESTE WS</button>
        <button @click="cancelar_task">FECHAR TASK</button>
        <h1 class="h1-text">Ficha do Diagnóstico</h1>

        <!-- <TesteOverlay
            class="overlay-aviso"

        ></TesteOverlay>
        <TesteOverlay
            class="overlay-aviso"
            :eventoAviso="'tamanhoErrado'"
            :titulo="'Vídeo muito grande!'"
            :subtexto="`Tamanho máximo: 50MB`"
            :srcImg="'src/assets/alert_circle.png'"
        ></TesteOverlay> -->
        <main>
            <p
                v-if="!this.$store.getters.getLogado"
                class="sm:text-2xl"
                id="aviso-avulso"
            >
                Aviso! A Análise Avulsa não salvará nenhuma informação dos pacientes
            </p>

            <form
                @keyup.enter="$emit('submit')"
                ref="form"
                class="form-cadastro"
                @submit.prevent="enviaDiag"
            >
                <div class="form-group">
                    <label>Nome do Paciente</label>

                    <input
                        @input="checkNome"
                        type="text"
                        v-model="this.nomePac"
                        required="true"
                    />
                </div>
                <div class="form-group grupo-paralisia">
                    <label>Possui Paralisia?</label>
                    <span class="opcoes">
                        <div class="label-input">
                            <input
                                type="radio"
                                v-model="this.paralisia"
                                value="Sim"
                                name="paralisia"
                            />
                            <label>Sim</label>
                        </div>
                        <div class="label-input">
                            <input
                                type="radio"
                                @input="
                                    () => {
                                        this.olhoEsquerdo = 'false';
                                        this.olhoDireito = 'false';
                                    }
                                "
                                v-model="this.paralisia"
                                value="Nao"
                                name="paralisia"
                            />
                            <label>Não</label>
                        </div>
                        <div class="label-input">
                            <input
                                type="radio"
                                v-model="this.paralisia"
                                value="Inconclusivo"
                                name="paralisia"
                            />
                            <label>Inconclusivo</label>
                        </div>
                    </span>
                </div>

                <div class="form-group grupo-olho">
                    <label>Olho Paralítico</label>
                    <span class="opcoes">
                        <div class="label-input">
                            <input
                                :enabled="this.paralisia === 'Sim'"
                                :disabled="this.paralisia !== 'Sim'"
                                type="checkbox"
                                v-model="this.olhoEsquerdo"
                                id="leftEye"
                                value="esquerdo"
                            />
                            <label id="leftEyeLabel" for="leftEye">Esquerdo</label>
                        </div>
                        <div class="label-input">
                            <input
                                :enabled="this.paralisia === 'Sim'"
                                :disabled="this.paralisia !== 'Sim'"
                                type="checkbox"
                                v-model="this.olhoDireito"
                                id="rightEye"
                                value="direito"
                            />
                            <label for="rightEye">Direito</label>
                        </div>
                    </span>
                </div>

                <div class="form-group">
                    <div id="div-lateral">
                        <label id="label-upload" for="videoUpload">Enviar Vídeo</label>
                        <input
                            @change="getVideo"
                            type="file"
                            id="videoUpload"
                            name="video"
                            accept="video/*"
                            required
                        />
                        <p v-if="this.videoObj != null">Vídeo Carregado</p>
                    </div>
                </div>

                <div class="form-group">
                    <label for="patientDescription">Descrição (opcional)</label>
                    <textarea
                        v-model="this.desc"
                        id="patientDescription"
                        name="description"
                        rows="4"
                        placeholder="Descrição curta do paciente e do porquê de seu diagnóstico"
                    ></textarea>
                </div>

                <Button
                    class="but-cadastro"
                    type="submit"
                    :ativo="checkCampos"
                    texto="Analisar"
                ></Button>
            </form>
        </main>
        <Rodape />
    </section>
</template>

<script>
import { mapActions, mapState } from "vuex";

import HeaderSistema from "./components/layout/HeaderSistema.vue";
import Button from "./components/navigation/Button.vue";
import Rodape from "./components/layout/Rodape.vue";
import TesteOverlay from "./components/layout/TesteOverlay.vue";
import emitter from "./eventBus";

import axios from "axios";
import { v4 as uuidv4 } from "uuid";
import crypto from "crypto";
const eventoFormatoErrado = "formatoErrado";
const eventoTamanhoErrado = "tamanhoErrado";

//em bytes
const MAX_FILE_SIZE = 50 * 1024 * 1024;

export default {
    name: "fichaDiag",
    components: {
        HeaderSistema,
        Button,
        Rodape,
        TesteOverlay,
    },
    created() {},
    data() {
        return {
            nomePac: "",
            paralisia: "",
            olhoEsquerdo: "false",
            olhoDireito: "false",
            desc: "",
            videoObj: null,
            taskId: null,
            // "avi"
            extensoes: ["mpg", "mpeg", "webm", "mkv", "ogv", "ogg", "mp4", "avi"],
        };
    },
    props: {},
    computed: {
        checkCampos() {
            return (
                this.nomePac !== "" &&
                this.paralisia !== "" &&
                this.videoObj != null &&
                this.videoObj != undefined &&
                (Boolean(this.olhoEsquerdo) != false ||
                    Boolean(this.olhoDireito) != false)
            );
        },
    },
    methods: {
        ...mapActions("modals", ["openModal"]),
        ...mapActions(["handleWebSocket"]),
        cancelar_task() {
            axios.post(
                this.$store.getters.getUrlBackend + `/cancelar-task/${this.taskId}`,
                {
                    withCredentials: true,
                }
            );
        },

        openPopup() {
            this.$store.dispatch("modal/openModal", {
                name: "popup",
                content: {
                    component: "Popup",
                    props: {
                        titulo: "Popup Aberto!",
                        subtexto: "Você abriu via Button.vue!",
                        srcImg: "src/assets/alert_circle.png",
                        link: "https://google.com",
                    },
                },
            });
        },
        openOverlay(props) {
            this.$store.dispatch("modal/openModal", {
                name: "overlay",
                content: {
                    component: "Teste",
                    props: { ...props },
                },
            });
        },

        async teste_WS() {
            this.objEnviaDiag = { task_id: 2 };
            console.log("MOUNTED RESPONSE: ", this.objEnviaDiag);
            const taskId = this.objEnviaDiag?.task_id;

            const urlWS = `${this.$store.getters.getWSBackend}/ws`;
            console.log(`URL WS: ${urlWS}`);

            try {
                await this.$store.dispatch("handleWebSocket", { wsURL: urlWS, taskId });
                console.log("CONEXAO COM WEBSOCKET OK");
            } catch (err) {
                console.error("Falha ao estabelecer a conexão WebSocket:", error);
            }
        },
        async enviaDiag() {
            //envia dados pro back comecar processamento
            const formData = new FormData();
            formData.append("video", this.videoObj);
            formData.append("nomePaciente", this.nomePac);
            formData.append("stringOlhos", `${this.olhoEsquerdo}+${this.olhoDireito}`);
            formData.append("desc", this.desc);

            // const formDiag = this.$store.getters.getFormDiag;
            console.log("FORM: ", formData, typeof formData);

            const promiseEnviaDiag = axios.post(
                this.$store.getters.getAnaliseWS,
                formData,
                {
                    withCredentials: true,
                }
            );

            let res = "None";
            //lida com falha no envio
            try {
                res = await promiseEnviaDiag;
                this.objEnviaDiag = res.data;
                console.log(
                    "UPLOAD FEITO COM SUCESSO!: " + JSON.stringify(this.objEnviaDiag)
                );
            } catch (error) {
                this.msgErro = res.data; //data eh mensagem de erro vindo do servidor
                console.log("DEU RUIM: " + JSON.stringify(this.msgErro));
                const msgErro = {
                    titulo: "Formato de vídeo não suportado!",
                    subtexto: `Formatos aceitos: ${this.extensoes}`,
                    srcImg: "src/assets/alert_circle.png",
                };
                this.openOverlay(msgErro);
            }

            console.log("MOUNTED RESPONSE: ", this.objEnviaDiag);
            const taskId = this.objEnviaDiag?.task_id;
            this.taskId = this.objEnviaDiag?.task_id;

            const urlWS = `${this.$store.getters.getWSBackend}/ws`;
            console.log(`URL WS: ${urlWS}`);

            try {
                await this.$store.dispatch("handleWebSocket", {
                    wsURL: urlWS,
                    taskId: taskId,
                });
                console.log("CONEXAO COM WEBSOCKET OK");
            } catch (err) {
                console.error("Falha ao estabelecer a conexão WebSocket:", err);
            }

            // const ws = new WebSocket(`${this.$store.getters.getWSBackend}/ws`);
            // console.log(`NOVO SOCKET: ${JSON.stringify(ws)}`);

            // const funSendWS = (taskId) => {
            //     return JSON.stringify({ taskId: taskId });
            // };

            // const funGetResBackend = (evt) => {
            //     console.log("WS got:", evt.data);
            // };
            // const funError = (evt) => {
            //     ws.onerror = (evt) => console.error(`WEBSOCKET: ${evt.data}`);
            // };
            // const funClose = (evt) => {
            //     console.log(`WEBSOCKET FECHADO!\n`);
            // };

            // ws.onopen = () => ws.send(funSendWS(taskId));
            // ws.onmessage = funGetResBackend(evt);
            // ws.onerror = (evt) => console.error(`WEBSOCKET: ${evt.data}`);

            // ws.onclose = (evt) => console.log(`WEBSOCKET FECHADO!\n`);

            // this.$router.push({ name: "PaginaCarregando" });
        },
        getVideo($evt) {
            //checagem por tipos de video e tamanho
            const file = $evt.target.files[0];
            if (file.size > MAX_FILE_SIZE) {
                emitter.emit(eventoTamanhoErrado);
                this.videoObj = null;
                const props = {
                    titulo: "Vídeo muito grande!",
                    subtexto: `Tamanho máximo: 50MB`,
                    srcImg: "src/assets/alert_circle.png",
                };
                console.log("\nFORMATO INVALIDO< ABRINDO OVERLAY!\n\n");
                this.openOverlay(props);
                return;
            }
            if (file) {
                const filename = String(file.name).toLowerCase();
                const ext = filename.split(".")[1];

                if (this.extensoes.includes(`${ext}`)) {
                    this.videoObj = file;
                } else {
                    const props = {
                        titulo: "Formato de vídeo não suportado!",
                        subtexto: `Formatos aceitos: ${this.extensoes}`,
                        srcImg: "src/assets/alert_circle.png",
                    };
                    console.log("\nFORMATO INVALIDO< ABRINDO OVERLAY!\n\n");
                    this.openOverlay(props);
                    this.videoObj = null;
                    console.log("DEPOIS DE ABRIR OVERLAY!");
                }
            }
        },
    },
    mounted() {
        // listener pra quando fileInput recebe mudança
        // document.getElementById("fileInput").onchange = this.handleFileUpload;
    },
};
</script>

<style lang="scss" scoped>
$font-size-labels: clamp(16px, 2.2vmin, 19px);

.frame-pagina {
    @include frame-pagina($gap: 5vmin);
    height: 100vh;
}

h1 {
    color: #3a0d75;

    width: max-content;
    margin: 0px;
    text-align: center;
    align-self: center;
    font-weight: 400;
    line-height: normal;
}

.overlay-aviso {
    top: calc($alt-headers * 1.05);
}

main {
    width: fit-content;
    margin: auto;
    display: flex;
    align-items: flex-start;
    flex-direction: column;
    justify-content: center;
    gap: 20px;
    flex: 1 0 0;

    #aviso-avulso {
        color: #792359;
        @apply .h1-text
        font-size: 1.8rem;
        font-weight: 400;
        line-height: normal;
    }
}

form {
    display: flex;
    flex-direction: column;
    gap: 2vmin;
    width: 100%;
    .form-group {
        display: flex;
        flex-direction: column;
        gap: 5px;

        .opcoes {
            display: flex;
            gap: 2vmin;
            #leftEyeLabel {
                margin-right: 1vmin;
            }
            .label-input:has(input[type="checkbox"]:disabled) {
                filter: brightness(0.5) opacity(0.5);
                pointer-events: none;
            }
        }

        #div-lateral {
            gap: 2vmin;
            display: flex;
            align-items: center;
        }

        label {
            // font-size: $font-size-labels;
            @apply campos-ficha
            font-weight: 600;
        }
        input,
        textarea {
            width: 100%;
            padding: 1%;
            height: 2lh;
            font-size: $form-fonte-peq;
            border: 2px solid #b3b3b3;
            border-radius: 1vmin;
            background-color: white;
            outline: none;
            transition: border-color 0.3s ease-in-out;

            &::placeholder {
                color: #757575;
            }

            &:focus {
                border-color: #444444;
            }
        }
        #patientDescription {
            height: 8ch;
        }
    }

    .grupo-olho {
        input[type="checkbox"] {
            accent-color: #3a0d75;
            width: 2.5vmin;
        }
    }

    .grupo-paralisia {
        display: flex;
        gap: 2vmin;
        input {
            width: 1.25em;
            padding: 1%;
        }
    }

    .label-input {
        display: flex;
        align-items: center;
        gap: 1vmin;
        input[type="radio"] {
            appearance: none;
            -moz-appearance: none; /* Ensure Firefox support */
            border: calc(30vmin / 100) solid black; /* Outer circle */
            border-radius: 100%;
            height: 2.8vmin;
            width: 2.8vmin;
            padding: 0px;
            margin: auto;

            display: inline-block;
            justify-content: center;
            align-items: flex-start;
            position: relative;
            cursor: pointer;

            &::before {
                content: "";
                aspect-ratio: 1/1;
                width: 59%;
                height: 59%;
                background-color: $sec-color;
                border-radius: 1000%;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) scale(0);
                transition: all 0.1s ease-in;
            }
            /* Show inner circle when checked */
            &:checked {
                border-color: $sec-color;

                &::before {
                    transform: translate(-50%, -50%) scale(1);
                }
            }
        }
    }

    #label-upload {
        background: linear-gradient(98deg, #d2d2d2 4.6%, #e5e5e5 56.86%);
        width: max-content;
        height: auto;
        border-radius: 5vmin;
        border: 1px solid rgb(180, 179, 179);
        padding: 1% 2%;
        font-size: 2vmin;
        font-weight: 400;
        @media (max-width: 560px), (max-height: 560px) {
            font-weight: 600;
        }
        &:hover,
        &:focus {
            border-color: rgb(97, 97, 97);
        }
    }
}
</style>
