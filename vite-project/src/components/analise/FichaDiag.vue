<template>
  <div class="cntr-cta">
    <input type="file" id="fileInput" accept="video/*" />
    <label for="fileInput" ref="" class="label-cta"> Analisar Vídeo </label>
  </div>
</template>

<script>
import db from "../../db.js";
import axios from "axios";
import mime from "mime-types";

export default {
  name: "Test",
  created() {},
  data() {
    return {};
  },
  props: {},
  methods: {
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
  },
  mounted() {
    // listener pra quando fileInput recebe mudança
    document.getElementById("fileInput").onchange = this.handleFileUpload;
  },
};
</script>

<style lang="scss" scoped></style>
