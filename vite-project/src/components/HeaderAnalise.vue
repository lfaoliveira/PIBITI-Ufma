<template>
    <div class="div-header">
    <Seta></Seta>
    <Salvar></Salvar>
  </div>
</template>

<script>
import Seta from "./icons/Seta.vue"
import Salvar from "./icons/Salvar.vue";
export default {
  name: "headerAnalise",
  components: {
    Seta,
    Salvar,
  },
  created() {},
  data() {
    return {};
  },
  props: {},
  methods: {},
};
</script>

<style scoped>
*{
  --alt-butao: clamp(40px, 5vmin, 77px);
  --raio-butao: clamp(10px, 40%, 20px);
  font-family: 'Montserrat', 'Inter';
  border: 0px;
}
input{
  display:none;
}

.div-header {
  max-width: 95%;
  position: absolute;
  margin: 1vmin 0px 0px 0px;
  height: auto;
  width: clamp(90vmin, 85%, 95%);
  z-index: 1;
  display: flex;
  align-items: center;
  /* grid-template-rows: 1fr;
  grid-template-columns: 1fr 1fr; */
}


</style>