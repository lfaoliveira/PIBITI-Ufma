<template>
  <menuLateral />
    <h1 @click="sendData"> Bem-Vindo!</h1>
      <!--label para estilizar butao upload -->
      <div class="wrapper">
        <label for="fileInput" ref="" class="custom-file-upload" :style="estiloUpload">
          Upload
        </label>
        <input type="file" id="fileInput" accept="video/*" @change="handleFileUpload" 
        @focus="addFocusClass" @blur="removeFocusClass">
      </div>    
</template>

<script>
import menuLateral from "./MenuLateral.vue";
import { mapActions } from 'vuex';

export default {
  name: "Homepage",
  components: {
    menuLateral,
  },
  created() {},
  methods: {
    ...mapActions(['updateSharedData']),
    sendData() {
      this.updateSharedData({ message: 'Hello from HomePage' });
      this.$router.push('/teste');
    },

    handleFileUpload($evt){
      console.log("UPLOAD FEITO")
      const file = $evt.target.files[0];
      if (file) {
        this.videoFile = file;
        this.videoURL =  URL.createObjectURL(this.videoFile); // filename = path relativo
        this.$router.push('/teste');
      }
    },
    addFocusClass() {
      // Manually add the 'focus' class to the label
      const label = document.querySelector('.custom-file-upload');
      label.classList.add('focus');
      
    },
    removeFocusClass() {
      // Manually remove the 'focus' class from the label
      const label = document.querySelector('.custom-file-upload');
      label.classList.remove('focus');
    },
  },
  computed: {
    estiloUpload(){
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
      }
    }
  },
  data() {
    return {
      videoURL: '',
    };
  },
  mounted(){
    window.addEventListener('resize', this.resizeVideo);
  },
  props: {},
};
</script>

<style scoped>
input {
  display: none;
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

.custom-file-upload{
  background-color: #43C3DD;
  --butao-height: 6vmin;
  --butao-width: 30vmin;
  height: clamp(4rem, var(--butao-height), 6rem);
  width: clamp(6rem, var(--butao-width), 10rem);
  font-size: clamp(2rem, 4vmin, 6rem );
}

.custom-file-upload:focus{
  background-color: #ffffff;
  height: clamp(4vmin + 1vmin, var(--butao-height) + 2 vmin, var(--butao-height)+ 4vmin);
  width: clamp(6rem, var(--butao-width), 10rem);
  font-size: clamp(2rem, 4vmin, 6rem );
}

.custom-file-upload:hover{
  background-color: #39abc2;
  --butao-height: 8vmin;
  --butao-width: 30vmin;
  height: clamp(2vmin + 4vmin, var(--butao-height) + 4vmin, var(--butao-height)+ 12vmin);
  width: clamp(6rem, var(--butao-width), 10rem);
  font-size: clamp(3vmin, 5vmin, 7vmin);
}
</style>