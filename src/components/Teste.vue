<template>
<div>
  <video :src="videoURL" controls autoplay:true class="videoPessoa" :style="videoStyle"></video>
  <input type="file" form="videoUploadForm" accept="video/*" @change="handleFileUpload">

</div>

</template>

<script lang="js">
export default{
  name: "Teste",
  data() {
    return {
      videoFile: null,
      videoURL: '',
    }
    
  },
  methods: {
    handleFileUpload($evt){
      const file = $evt.target.files[0];
      if (file) {
        this.videoFile = file;
        this.videoURL =  URL.createObjectURL(this.videoFile) // filename = path relativo
        console.log(this.videoURL)
      }
    },
    resizeVideo() {
      const aspectRatio = 16 / 9; // Assuming a standard aspect ratio of 16:9
      const maxWidth = window.innerWidth * 0.8; // 90% of the window width
      const maxHeight = window.innerHeight * 0.8; // 90% of the window height

      if (maxWidth / aspectRatio <= maxHeight) {
        this.videoWidth = maxWidth;
        this.videoHeight = maxWidth / aspectRatio;
      } else {
        this.videoHeight = maxHeight;
        this.videoWidth = maxHeight * aspectRatio;
      }
    },

  },
  computed: {
    videoStyle() {
      return {
        width: `${this.videoWidth}px`,
        height: `${this.videoHeight}px`,
      };
    },
  },
  mounted() {
    window.addEventListener('resize', this.resizeVideo);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeVideo);
  },
};

</script>

<style scoped>
video {
  margin-top: 20px;
  max-width: 100%;
  max-height: 100%;
}
</style>