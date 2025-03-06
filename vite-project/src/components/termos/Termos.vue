<template>
  <header class="div-header">
    <Voltar class="seta" :onclick="fnVoltar"></Voltar>
  </header>
  <main>
    <div>asdadadwadwddwaddadwdawdawdadwadadadd adwda adawda adawd awd</div>
  </main>
</template>

<script>
import Voltar from "../icons/Voltar.vue";

export default {
  name: "termosComp",
  components: {
    Voltar,
  },
  created() {},
  data() {
    return {};
  },
  props: {},
  methods: {
    fnVoltar() {
      this.$router.push({ name: "cad" });
    },
  },
};
</script>

<style lang="scss" scoped>
* {
  --alt-butao: clamp(40px, 5vmin, 77px);
  --raio-butao: clamp(10px, 40%, 20px);
  font-family: "Montserrat", "Inter";
  border: 0px;
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
}
</style>
