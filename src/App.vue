<template>
  <menuLateral />
  <h1> Bem-Vindo!</h1>
    <!--label para estilizar butao upload -->
    <label for="fileInput" class="custom-file-upload" :style="estiloUpload">
      Upload
    </label>
    <input type="file" id="fileInput" accept="video/*" @change="handleFileUpload">

</template>

<script>
import menuLateral from "./components/MenuLateral.vue";

export default {
  components: {
    menuLateral,
  },
  props: {},
  data() {
    return {
      time: 0,
      videoURL: '',
    };
  },
  methods: {
   enchelinguica() {return 1*2;},
   handleFileUpload($evt){
      console.log("UPLOAD FEITO")
      const file = $evt.target.files[0];
      if (file) {
        this.videoFile = file;
        this.videoURL =  URL.createObjectURL(this.videoFile) // filename = path relativo
      }
    }
  },
  computed: {
    estiloUpload(){
      return {
        // COR E FONTE
        backgroundColor: `#43C3DD`,
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
        marginBottom: `1.2vh`,
        marginTop: `1vh`,
        textAlign: `center`,
      }
    }
  },
  mounted(){
    window.addEventListener('resize', this.resizeVideo);
  },

};
</script>

<style scoped>
input[type="file"] {
  display: none;
}

.custom-file-upload{
  --butao-height: 6vmin;
  --butao-width: 30vmin;
  height: clamp(4rem, var(--butao-height), 6rem);
  width: clamp(6rem, var(--butao-width), 10rem);
  font-size: clamp(2rem, 4vmin, 6rem );
}
.custom-file-upload:hover{
  --butao-height: 6vmin;
  --butao-width: 30vmin;
  height: clamp(4rem + 2rem, var(--butao-height) + 2 vmin, 6rem + 2rem);
  width: clamp(6rem, var(--butao-width), 10rem);
  font-size: clamp(2rem, 4vmin, 6rem );
}

h1 {
  --header-font-size: 4rem;
  font-family: 'Roboto Serif', serif !important;   
  font-size: clamp(1rem, var(--header-font-size), 10vmin);
  color: #001B2C;
  line-height: 1;
  display: flex;
  position: absolute;
  top: 0rem;
  /* Stick to the top */
  left: auto;
  /* Align to the left */
  justify-content: center;
  align-items: center;
  /* Horizontal center */
  /*  width: 50rem; Full width to cover the entire page width     */
  height: calc(var(--header-font-size) + 1rem);
  width: calc(var(--header-font-size)*10);
  margin-top: 1vmin; 
  margin-bottom: 0vmin;
  border: none;
}


</style>
