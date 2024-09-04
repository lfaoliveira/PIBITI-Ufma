<template>
<div>
  <video controls autoplay:true class="videoplayer">
    <source :src="fileName">
  </video>

  <form id="videoUploadForm">
    <input type="file" form="videoUploadForm" id="videoFile" accept="video/*" @change="handleFileUpload">
    <!-- <button form="videoUploadForm" type="submit">Upload Video</button> -->
  </form>
  
</div>

</template>


<script lang="js">

export default{
  name: "Teste",
  data(){
    return{
      videoFile: null,
      fileName: '',
    }
    
  },
  methods: {
    handleFileUpload(event){
      const file = event.target.files[0];
      if (file) {
        this.videoFile = file;
        this.fileName = file.name; // filename = path relativo
        console.log(this.fileName)
      }

    }
  }
}


</script>