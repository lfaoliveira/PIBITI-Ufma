<template>
    <section class="flex flex-col items-center gap-5 w-full overflow-x-hidden">
        <HeaderSistema :activeIndex="4" />

        <h1 class="text-[#3a0d75] text-xl sm:text-4xl w-max m-0 text-center self-center font-normal">Ficha do Diagnóstico</h1>

        <main class="w-fit mx-auto flex flex-col items-start gap-5">
            <p
                v-if="!this.$store.getters.getLogado"
                class="text-[#792359] text-xl sm:text-2xl font-normal"
            >
                Aviso! A Análise Avulsa não salvará nenhuma informação dos pacientes
            </p>

            <form
                @keyup.enter="$emit('submit')"
                ref="form"
                class="flex flex-col gap-[2vmin] w-full"
                @submit.prevent="enviaDiag"
            >
                <div class="flex flex-col gap-[5px]">
                    <label class="text-lg sm:text-2xl font-semibold">Nome do Paciente</label>
                    <input
                        @input="checkNome"
                        type="text"
                        v-model="this.nomePac"
                        required="true"
                        class="w-full p-[1%] h-2lh text-base border-2 border-[#b3b3b3] rounded-[1vmin] bg-white outline-none transition-colors duration-300 focus:border-[#444] placeholder-[#757575]"
                    />
                </div>
                <div class="flex flex-col gap-[5px]">
                    <label class="text-lg sm:text-2xl font-semibold">Possui Paralisia?</label>
                    <span class="flex gap-[2vmin]">
                        <div class="flex items-center gap-[1vmin]">
                            <input
                                type="radio"
                                v-model="this.paralisia"
                                value="Sim"
                                name="paralisia"
                                class="appearance-none border-[calc(30vmin/100)] solid black rounded-full h-[2.8vmin] w-[2.8vmin] p-0 cursor-pointer accent-[#3a0d75]"
                            />
                            <label>Sim</label>
                        </div>
                        <div class="flex items-center gap-[1vmin]">
                            <input
                                type="radio"
                                @input="
                                    () => {
                                        this.olhoEsquerdo = 'false'
                                        this.olhoDireito = 'false'
                                    }
                                "
                                v-model="this.paralisia"
                                value="Nao"
                                name="paralisia"
                                class="appearance-none border-[calc(30vmin/100)] solid black rounded-full h-[2.8vmin] w-[2.8vmin] p-0 cursor-pointer accent-[#3a0d75]"
                            />
                            <label>Não</label>
                        </div>
                        <div class="flex items-center gap-[1vmin]">
                            <input
                                type="radio"
                                v-model="this.paralisia"
                                value="Inconclusivo"
                                name="paralisia"
                                class="appearance-none border-[calc(30vmin/100)] solid black rounded-full h-[2.8vmin] w-[2.8vmin] p-0 cursor-pointer accent-[#3a0d75]"
                            />
                            <label>Inconclusivo</label>
                        </div>
                    </span>
                </div>

                <div class="flex flex-col gap-[5px]">
                    <label class="text-lg sm:text-2xl font-semibold">Olho Paralítico</label>
                    <span class="flex gap-[2vmin]">
                        <div class="flex items-center gap-[1vmin]"
                            :class="{ 'opacity-50 pointer-events-none': this.paralisia !== 'Sim' }"
                        >
                            <input
                                :disabled="this.paralisia !== 'Sim'"
                                type="checkbox"
                                v-model="this.olhoEsquerdo"
                                id="leftEye"
                                value="esquerdo"
                                class="accent-[#3a0d75] w-[2.5vmin]"
                            />
                            <label id="leftEyeLabel" for="leftEye">Esquerdo</label>
                        </div>
                        <div class="flex items-center gap-[1vmin]"
                            :class="{ 'opacity-50 pointer-events-none': this.paralisia !== 'Sim' }"
                        >
                            <input
                                :disabled="this.paralisia !== 'Sim'"
                                type="checkbox"
                                v-model="this.olhoDireito"
                                id="rightEye"
                                value="direito"
                                class="accent-[#3a0d75] w-[2.5vmin]"
                            />
                            <label for="rightEye">Direito</label>
                        </div>
                    </span>
                </div>

                <div class="flex flex-col gap-[5px]">
                    <div class="gap-[2vmin] flex items-center">
                        <label
                            for="videoUpload"
                            class="bg-gradient-to-br from-[#d2d2d2] to-[#e5e5e5] w-max rounded-[5vmin] border border-[rgb(180,179,179)] px-[2%] py-[1%] text-[2vmin] font-normal hover:border-[rgb(97,97,97)] focus:border-[rgb(97,97,97)] cursor-pointer max-[560px]:font-semibold"
                        >Enviar Vídeo</label>
                        <input
                            @change="getVideo"
                            type="file"
                            id="videoUpload"
                            name="video"
                            accept="video/*"
                            required
                            class="hidden"
                        />
                        <p v-if="this.videoObj != null">Vídeo Carregado</p>
                    </div>
                </div>

                <div class="flex flex-col gap-[5px]">
                    <label for="patientDescription" class="text-lg sm:text-2xl font-semibold">Descrição (opcional)</label>
                    <textarea
                        v-model="this.desc"
                        id="patientDescription"
                        name="description"
                        rows="4"
                        placeholder="Descrição curta do paciente e do porquê de seu diagnóstico"
                        class="w-full p-[1%] h-8ch text-base border-2 border-[#b3b3b3] rounded-[1vmin] bg-white outline-none transition-colors duration-300 focus:border-[#444] placeholder-[#757575]"
                    ></textarea>
                </div>

                <Button
                    class="relative mx-[2vmin]"
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
import { mapActions, mapState } from "vuex"

import HeaderSistema from "../layout/HeaderSistema.vue"
import Button from "../navigation/Button.vue"
import Rodape from "../layout/Rodape.vue"
import TesteOverlay from "../layout/TesteOverlay.vue"
import emitter from "../../eventBus"

import axios from "axios"
// const eventoFormatoErrado = "formatoErrado";
// const eventoTamanhoErrado = "tamanhoErrado";

//em bytes
const MAX_FILE_SIZE = 50 * 1024 * 1024

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
        }
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
            )
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
            )
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
            })
        },
        openOverlay(props) {
            this.$store.dispatch("modal/openModal", {
                name: "overlay",
                content: {
                    component: "Teste",
                    props: { ...props },
                },
            })
        },

        async enviaDiag() {
            //envia dados pro back comecar processamento
            const formData = new FormData()
            formData.append("video", this.videoObj)
            formData.append("nomePaciente", this.nomePac)
            formData.append("stringOlhos", `${this.olhoEsquerdo}+${this.olhoDireito}`)
            formData.append("desc", this.desc)
            console.log("video", this.videoObj)
            console.log("nomePaciente", this.nomePac)
            console.log("stringOlhos", `${this.olhoEsquerdo}+${this.olhoDireito}`)
            console.log("desc", this.desc)

            // const formDiag = this.$store.getters.getFormDiag;
            console.log("FORM: ${JSON.stringify(formData)}")

            const promiseEnviaDiag = axios.post(
                this.$store.getters.getAnaliseWS,
                formData,
                {
                    withCredentials: true,
                }
            )

            let res = "None"
            //lida com falha no envio
            try {
                res = await promiseEnviaDiag
                this.objEnviaDiag = res.data
                console.log(
                    "UPLOAD FEITO COM SUCESSO!: " + JSON.stringify(this.objEnviaDiag)
                )
                const mensagemOK = {
                    titulo: "Vídeo enviado com sucesso!",
                    subtexto: `Uma notificação chegará quando estiver tudo pronto.`,
                    srcImg: "src/assets/check_circle.png",
                }
                this.openOverlay(mensagemOK)
            } catch (error) {
                this.msgErro = res.data //data eh mensagem de erro vindo do servidor
                console.error("DEU RUIM: " + JSON.stringify(this.msgErro))
                const msgErro = {
                    titulo: "Formato de vídeo não suportado!",
                    subtexto: `Formatos aceitos: ${this.extensoes}`,
                    srcImg: "src/assets/alert_circle.png",
                }
                this.openOverlay(msgErro)
                throw error
            }

            console.log("MOUNTED RESPONSE: ", this.objEnviaDiag)
            const taskId = this.objEnviaDiag?.task_id
            this.taskId = this.objEnviaDiag?.task_id

            const urlWS = `${this.$store.getters.getWSBackend}/ws`
            console.log(`URL WS: ${urlWS}`)

            try {
                this.$store.dispatch("handleWebSocket", {
                    wsURL: urlWS,
                    taskId: taskId,
                })
                console.log("CONEXAO COM WEBSOCKET OK")
            } catch (err) {
                console.error("Falha ao estabelecer a conexão WebSocket:", err)
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
            const file = $evt.target.files[0]
            if (file.size > MAX_FILE_SIZE) {
                emitter.emit(eventoTamanhoErrado)
                this.videoObj = null
                const props = {
                    titulo: "Vídeo muito grande!",
                    subtexto: `Tamanho máximo: 50MB`,
                    srcImg: "src/assets/alert_circle.png",
                }
                console.log("\nARQUIVO GRANDE DEMAIS!!!\n\n")
                this.openOverlay(props)
                return
            }
            if (file) {
                const filename = String(file.name).toLowerCase()
                const partes = filename.split(".")
                const ext = partes[partes.length - 1]
                console.log(`EXTENSAO: ${filename}\n`)
                if (this.extensoes.includes(`${ext}`)) {
                    this.videoObj = file
                } else {
                    const props = {
                        titulo: "Formato de vídeo não suportado!",
                        subtexto: `Formatos aceitos: ${this.extensoes}`,
                        srcImg: "src/assets/alert_circle.png",
                    }
                    console.log("\nFORMATO INVALIDO< ABRINDO OVERLAY!\n\n")
                    this.openOverlay(props)
                    this.videoObj = null
                    console.log("DEPOIS DE ABRIR OVERLAY!")
                }
            }
        },
    },
    mounted() {
        // listener pra quando fileInput recebe mudança
        // document.getElementById("fileInput").onchange = this.handleFileUpload;
    },
}
</script>

<style scoped>
/* Estilos substituídos por Tailwind */
</style>
