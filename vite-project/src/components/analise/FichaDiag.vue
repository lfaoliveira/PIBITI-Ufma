<template>
  <section class="frame-pagina">
    <HeaderSistema :activeIndex="4" />
    <h1>Etapa 1 de 3: Ficha do Diagnóstico</h1>

    <OverlayAviso
      class="overlay-aviso"
      :eventoAviso="'videoErrado'"
      :titulo="'Formato de vídeo não suportado!'"
      :subtexto="`Formatos aceitos: ${this.extensoes}`"
      :srcImg="'src/assets/alert_circle.png'"
    ></OverlayAviso>
    <main>
      <p v-if="!this.$store.getters.getLogado" id="aviso-avulso">
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

          <input @input="checkNome" type="text" v-model="this.nomePac" required="true" />
        </div>
        <div class="form-group grupo-paralisia">
          <label>Possui Paralisia?</label>
          <span class="opcoes">
            <div class="label-input">
              <input type="radio" v-model="this.paralisia" value="Sim" name="paralisia" />
              <label>Sim</label>
            </div>
            <div class="label-input">
              <input type="radio" v-model="this.paralisia" value="Nao" name="paralisia" />
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
          <label id="label-upload" for="videoUpload">Enviar Vídeo</label>
          <input
            @change="getVideo"
            type="file"
            id="videoUpload"
            name="video"
            accept="video/*"
            required
          />
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
import axios from "axios";
import mime from "mime-types";
import HeaderSistema from "../auxiliares/HeaderSistema.vue";
import Button from "../auxiliares/Button.vue";
import Rodape from "../auxiliares/Rodape.vue";
import OverlayAviso from "../auxiliares/OverlayAviso.vue";
import emitter from "../../eventBus";

const eventoVideoErrado = "videoErrado";

export default {
  name: "fichaDiag",
  components: {
    HeaderSistema,
    Button,
    Rodape,
    OverlayAviso,
  },
  created() {},
  data() {
    return {
      nomePac: "",
      paralisia: "",
      olhoEsquerdo: "",
      olhoDireito: "",
      desc: "",
      videoObj: null,
      extensoes: [".mkv", ".mp4"],
    };
  },
  props: {},
  computed: {
    checkCampos() {
      return (
        this.nomePac !== "" &&
        this.paralisia !== "" &&
        this.videoObj !== null &&
        (Boolean(this.olhoEsquerdo) != false || Boolean(this.olhoDireito) != false)
      );
    },
  },
  methods: {
    async enviaDiag() {
      //envia dados pro banco de dados e comeca logica de processamento
      const formData = new FormData();
      console.log(`${this.videoObj}, TYPE: ${typeof this.videoObj}`);
      formData.append("video", this.videoObj);
      formData.append("nomePaciente", this.nomePac);
      formData.append("stringOlhos", `${this.olhoEsquerdo}+${this.olhoDireito}`);
      formData.append("desc", this.desc);
      const res = await axios.post(this.$store.getters.getDiag, formData, {
        withCredentials: true,
      });
      this.$router.push({ name: "PaginaCarregando", params: { responseData: res.data } });
    },
    getVideo($evt) {
      //checagem por tipos de video
      const file = $evt.target.files[0];

      if (file) {
        const filename = String(file.name);
        const ext = filename.split(".")[1];

        if (this.extensoes.includes(`.${ext}`)) {
          this.videoObj = file;
        } else {
          emitter.emit(eventoVideoErrado);
          this.videoObj = null;
        }
      }
    },
    async handleFileUpload($evt) {
      const file = $evt.target.files[0];

      if (file) {
        // AQUI ENTRA LOGICA DE PROCESSAMENTO DE VIDEO
        const urlServer = "http://localhost:5000/analise"; // Replace with your server URL
        const formData = new FormData();
        formData.append("file", file); // 'file' is the key used for the file on the server

        (async () => {
          try {
            const result = await axios.post(urlServer, formData, {
              headers: { "Content-Type": "multipart/form-data" },
            });
            console.log(`RESULTADO`, result);
            const resultJSON = result.data;
            const strResult = resultJSON.string;
            const grafico_base64 = resultJSON.grafico;
            const video_base64 = resultJSON.video;
            console.log("VIDEO RECEBIDO: ", typeof video_base64);
            const extension = resultJSON.extVideo;

            const mimeVar = mime.lookup(extension);
            // TODO: MUDAR LOGICA DE ARMAZENAMENTO DE DADOS
            await db.open();
            const videoData = {
              string: strResult,
              video: video_base64,
              grafico: grafico_base64,
              mimeVideo: mimeVar,
            };
            console.log(videoData);
            let constId = await db.add(videoData);
            console.log(constId + " " + typeof constId);

            alert(constId);
            console.log("VIDEO PROCESSADO");
            this.$router.push({
              name: "analiseVideo",
              query: { idVideoAnalise: constId },
            });
          } catch (error) {
            console.error(error + "An error occurred while uploading the file.");
          }
        })();
      }
    },
    estiloCheckBox() {
      return {
        "checkBox--disabled": this.paralisia !== "Sim",
        "checkBox--enabled": this.paralisia === "Sim",
      };
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
    width: 28ch;
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

    label {
      font-size: $font-size-labels;
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
