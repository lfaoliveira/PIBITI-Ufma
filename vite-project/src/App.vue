<template>
  <router-view></router-view>
</template>

<script>

export default {
  name:"App",
  props: {  },
  data() {
    return {
      _: 0,
    };
  },
  mounted(){
    var docWidth = document.documentElement.offsetWidth;

    [].forEach.call(
      document.querySelectorAll('*'),
      function(el) {
        if (el.offsetWidth > docWidth) {
          console.log(el);
          console.log("Afaef");
        }
      }
);
  },

};
</script>

<style scoped>


</style>