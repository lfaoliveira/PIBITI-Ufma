<template>
  <div class="frame-pagina">
    <HeaderSistema tipo="outro" />
    <h1>Termos e Condições</h1>
    <main>
      <h1>Título dos Termos e Condições</h1>
      <!-- TODO: BOTAR REATIVIDADE DO VUE COM STRINGS PRA PREENCHER ESSA PORRA -->
      <ol class="texto-termos">
        <li class="subsecao-termos" v-for="(obj, index) in termos">
          <h2>{{ `${index + 1}. ${obj.titulo}` }}</h2>
          <p>{{ obj.p }}</p>
        </li>
      </ol>
    </main>
  </div>
</template>

<script>
import Voltar from "../icons/Voltar.vue";
import HeaderSistema from "../analise/HeaderSistema.vue";

export default {
  name: "termosComp",
  components: {
    Voltar,
    HeaderSistema,
  },
  created() {},
  data() {
    return {
      termos: [
        { titulo: "a", p: "a1" },
        { titulo: "b", p: "a2" },
        { titulo: "c", p: "a3" },
        { titulo: "d", p: "a4" },
        { titulo: "e", p: "a5" },
      ],
    };
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
.frame-pagina {
  @include frame-pagina($gap: 5vmin);
  height: max-content;
}
h1 {
  text-align: center;
}

main {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.texto-termos {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 0vmin 4vmin;
  align-items: flex-start;
}

.subsecao-termos {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
