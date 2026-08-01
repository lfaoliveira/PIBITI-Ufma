<template>
    <HeaderSistema :activeIndex="5" :urlPDF="pdfURL" />
    <main class="z-30 w-full bg-white flex flex-col items-center overflow-x-hidden overflow-y-auto">
        <!-- Loading screen -->
        <div
            v-if="!resPronto"
            class="fixed inset-[10%] bg-black/75 flex items-center justify-center z-10"
        >
            <div class="bg-white p-8 rounded-lg shadow-xl flex flex-col items-center">
                <div
                    class="w-12 h-12 border-4 border-purple-700 border-t-transparent rounded-full animate-spin"
                ></div>
                <p class="text-gray-700 text-lg font-semibold mt-4">Carregando análise...</p>
            </div>
        </div>

        <!-- Main content -->
        <template v-else>
            <h1 class="text-[#3a0d75] text-[clamp(35px,52px,70px)] max-[1000px]:text-[clamp(1.8rem,2rem,4rem)] max-[600px]:text-[clamp(1.2rem,1.4rem,4rem)] mt-[clamp(30px,6vmin,120px)] mx-auto mb-0 text-center font-bold">
                Análise de Paralisia
            </h1>

            <div class="grid grid-rows-[repeat(auto-fill,minmax(40vmin,2fr))] grid-cols-[repeat(auto-fit,minmax(85vmin,1fr))] gap-[clamp(2%,20px,4vmin)] w-[97%] mt-[2%]">
                <div class="rounded-[13px] bg-white shadow-[0_0_5px_4px_rgba(0,0,0,0.21)] text-black w-full flex flex-col justify-self-center overflow-x-hidden">
                    <h2 class="text-[#6113C6] font-semibold text-[clamp(14px,4vmin,22px)] my-[clamp(3%,20px,50px)] mx-[4%]">Diagnóstico: {{ olho_doente }}</h2>
                    <p class="font-semibold text-[clamp(14px,4vmin,22px)] my-[clamp(3%,20px,50px)] mx-[4%]">
                        Diferença de Velocidade: {{ percentDif }} %
                    </p>
                    <p class="font-semibold text-[clamp(14px,4vmin,22px)] my-[clamp(3%,20px,50px)] mx-[4%]">Olho Direito: {{ velD }} mm/s</p>
                    <p class="font-semibold text-[clamp(14px,4vmin,22px)] my-[clamp(3%,20px,50px)] mx-[4%]">
                        Olho Esquerdo: {{ velE }} mm/s
                    </p>
                </div>
                <div class="flex w-full aspect-[464/200] rounded-[10px] shadow-[0_0_7px_rgba(0,0,0,0.5)] overflow-x-hidden">
                    <img
                        ref="imgGraf"
                        :src="graficoURL"
                        class="object-contain w-full"
                        alt="Analysis graph"
                        draggable="false"
                    />
                </div>
            </div>
            <VideoPlayer :videoSource="videoSource" :mimeVideo="mimeVideo" />
            <Rodape class="mt-auto"></Rodape>
        </template>
    </main>
</template>

<!-- Rest of the code remains the same -->

<script>
import Rodape from "../layout/Rodape.vue";
import VideoPlayer from "./VideoPlayer.vue";
import HeaderSistema from "../layout/HeaderSistema.vue";
import TesteOverlay from "../layout/TesteOverlay.vue";
import axios from "axios";

export default {
    // COMPONENTE QUE VAI IMPORTAR COMPONENTES DE ANALISE
    name: "Analise de Video",
    components: {
        VideoPlayer,
        Rodape,
        HeaderSistema,
    },
    created() {},
    data() {
        return {
            videoSource: "",
            graficoURL: "",
            pdfURL: "",
            mimeVideo: "video/mp4",
            resPronto: false,
            olho_doente: "",
            percentDif: "",
            velD: "",
            velE: "",
            responseData: null,
        };
    },
    props: {
        uuid: null,
    },
    async mounted() {
        try {
            if (this.uuid != null) {
                const res = await axios.post(
                    `${this.$store.getters.getVerAnalise}/${this.uuid}`,
                    {
                        withCredentials: true,
                    }
                );
                this.responseData = res.data;
                console.log("DADOS CARREGADOS!: " + JSON.stringify(this.responseData));
            } else {
                throw Error("SEM UUID!");
            }
        } catch (err) {
            console.error("ERRO AO TENTAR CARREGAR ANALISE: " + err);
            throw err;
        }

        console.log("REPONSE DATA: ", this.responseData);
        this.parseResult();

        const urls = await Promise.all([
            this.downloadFile(this.responseData.video),
            this.downloadFile(this.responseData.graficoURL),
        ]);
        this.videoSource = urls[0];
        console.log("URL VIDEO: " + String(this.videoSource));
        this.graficoURL = urls[1];
        console.log("URL GRAFICO: " + String(this.graficoURL));

        this.pdfURL = this.responseData.pdfURL;
        console.log("\n\nTHIS.PDF: ", this.pdfURL);
        this.resPronto = true;
        // this.$refs.imgGraf.src = this.graficoURL;
    },
    methods: {
        addFocusClass() {
            // Manually add the 'focus' class to the label
            const label = document.querySelector(".custom-file-upload");
            label.classList.add("focus");
        },
        removeFocusClass() {
            // Manually remove the 'focus' class from the label
            const label = document.querySelector(".custom-file-upload");
            label.classList.remove("focus");
        },
        async downloadFile(url) {
            console.log("URL: ", url);
            // TODO: TESTAR SE LOGICA DE STREAMING DEU CERTO
            const response = await axios.get(url, { responseType: "blob" });

            const blob = response.data;
            console.log("RESPONSE DATA: ", response.data);
            const blobURL = URL.createObjectURL(blob);

            console.log(`Blob URL created: ${blobURL}`);
            return blobURL;
        },
        parseResult() {
            // Set velocity values
            this.velE = parseFloat(this.responseData.velE).toFixed(2);
            this.velD = parseFloat(this.responseData.velD).toFixed(2);
            this.percentDif = (parseFloat(this.responseData.percentDif) * 100).toFixed(2);

            // Set diagnosis
            const diag = this.responseData.olho_doente;
            if (diag === "false+false") {
                this.olho_doente = "Olhos Saudáveis";
            } else if (diag === "true+false") {
                this.olho_doente = "Olho Esquerdo Possivelmente Doente";
            } else if (diag === "false+true") {
                this.olho_doente = "Olho Direito Possivelmente Doente";
            } else {
                this.olho_doente = "Ambos os Olhos Possivelmente Doentes";
            }
        },
    },
    computed: {
        // controlStyle() {
        //     return {
        //         height: `${videoplayer.videoHeight / window.innerHeight}%`,
        //         width: `${videoplayer.videoWidth / window.innerWidth}%`,
        //     };
        // },
        estiloUpload() {
            return {
                // COR E FONTE
                borderRadius: `51px`,
                border: `none`,
                color: `black`,
                //TAMANHO
                position: `relative`,
                //POSICIONAMENTO
                whiteSpace: `nowrap`,
                letterSpacing: `0`,
                alignItems: `center`,
                display: `flex`,
                justifyContent: `center`,
                textAlign: `center`,
            };
        },
    },
};
</script>

<style scoped>
/* Estilos de customização do video.js mantidos via CSS global */
</style>
