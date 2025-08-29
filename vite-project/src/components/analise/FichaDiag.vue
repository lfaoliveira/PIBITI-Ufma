<template>
  <section class="frame-pagina">
    <HeaderSistema :activeIndex="4" />
    <h1>Etapa 1 de 3: Ficha do Diagnóstico</h1>

    <OverlayAviso
      class="overlay-aviso"
      :eventoAviso="'formatoErrado'"
      :titulo="'Formato de vídeo não suportado!'"
      :subtexto="`Formatos aceitos: ${this.extensoes}`"
      :srcImg="'src/assets/alert_circle.png'"
    ></OverlayAviso>
    <OverlayAviso
      class="overlay-aviso"
      :eventoAviso="'tamanhoErrado'"
      :titulo="'Vídeo muito grande!'"
      :subtexto="`Tamanho máximo: 50MB`"
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
import axios from "axios";
import mime from "mime-types";
import HeaderSistema from "../layout/HeaderSistema.vue";
import Button from "../navigation/Button.vue";
import Rodape from "../layout/Rodape.vue";
import OverlayAviso from "../layout/OverlayAviso.vue";
import emitter from "../../eventBus";

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
    OverlayAviso,
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
        (Boolean(this.olhoEsquerdo) != false || Boolean(this.olhoDireito) != false)
      );
    },
  },
  methods: {
    async enviaDiag() {
      //envia dados pro banco de dados e comeca logica de processamento
      const formData = new FormData();
      formData.append("video", this.videoObj);
      formData.append("nomePaciente", this.nomePac);
      formData.append("stringOlhos", `${this.olhoEsquerdo}+${this.olhoDireito}`);
      formData.append("desc", this.desc);
      this.$store.commit("setFormDiag", formData);
      this.$router.push({ name: "PaginaCarregando" });
    },
    getVideo($evt) {
      //checagem por tipos de video e tamanho
      const file = $evt.target.files[0];
      if (file.size > MAX_FILE_SIZE) {
        emitter.emit(eventoTamanhoErrado);
        this.videoObj = null;
        return;
      }
      if (file) {
        const filename = String(file.name).toLowerCase();
        const ext = filename.split(".")[1];

        if (this.extensoes.includes(`${ext}`)) {
          this.videoObj = file;
        } else {
          emitter.emit(eventoFormatoErrado);
          this.videoObj = null;
        }
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

    #div-lateral {
      gap: 2vmin;
      display: flex;
      align-items: center;
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
