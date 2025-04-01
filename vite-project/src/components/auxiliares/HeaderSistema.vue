<template>
  <nav class="nav-bar">
    <ul class="header lado-esquerdo">
      <img src="../../assets/dummy-image-square 1.png" />
      <!-- Para cada item dentro de menuItens, so ativa quem tiver indice igual a activeIndex -->
      <li class="nav-item" v-for="(item, index) in itensEsquerdo" :key="index">
        <a :class="{ active: activeIndex === index }" @click="setActive(item)">
          {{ item }}
        </a>
      </li>
    </ul>
    <ul class="lado-direito">
      <li v-if="!this.logado" class="nav-item">
        <a
          :class="{ active: activeIndex === itensEsquerdo.length }"
          @click="setActive('Acessar Sistema')"
          >Acessar Sistema</a
        >
      </li>
      <li class="nav-item" v-if="this.logado">
        <a :class="{ active: activeIndex === 6 }" @click="setActive('Perfil')">Perfil</a>
      </li>
      <li class="nav-item" v-if="this.logado">
        <Salvar :modo="this.emAnalise ? 'on' : 'off'"></Salvar>
      </li>
    </ul>
  </nav>
</template>

<script>
import HeaderInicio from "../inicio/HeaderInicio.vue";
import Salvar from "../icons/Salvar.vue";
import Voltar from "../icons/Voltar.vue";

export default {
  name: "HeaderSistema",
  components: {
    HeaderInicio,
    Salvar,
    Voltar,
  },
  data() {
    return {
      itensEsquerdo: ["Início", "Método", "Sobre", "Como Funciona?", "Fazer Análise"],
      emAnalise: false,
      logado: false,
    };
  },
  props: {
    activeIndex: 0,
  },
  created() {
    this.$store.subscribe((mutation, state) => {
      if (mutation.type === "setLogado") {
        this.logado = state.logado;
      }
    });
  },
  mounted() {
    //executar checagem se esta logado
    this.logado = this.$store.getters.getLogado;
    console.log(`NO HEADER: ${this.logado}`);
  },
  methods: {
    setActive(nome) {
      this.$emit("update:activeIndex", nome);

      const mapa = {
        Início: "/",
        Método: "/metodo",
        Sobre: "/equipe",
        "Como Funciona?": "/duvidas",
        "Fazer Análise": "/ficha",
        "Acessar Sistema": "/acesso",
        Perfil: "/perfil",
      };
      const rota = mapa[nome];
      this.$router.push(rota);
    },

    salvarResultado() {
      // lógica para salvar resultado
      console.log("Resultado salvo");
    },
  },
};
</script>

<style lang="scss" scoped>
.nav-bar {
  display: flex;
  width: 100%;
  z-index: 1;
  background: #0e0021;
}
.header {
  list-style: none;
  display: flex;
  height: $alt-headers;
  padding: 10px;
  margin: 0px;
  align-items: center;
  gap: 20px;
  flex: 1 0 0;
  align-self: stretch;
}

.lado-direito {
  list-style: none;

  display: flex;
  align-items: center;
  gap: 30px;
}

.nav-item a {
  @include botao-header($escala: 1.1);
}

.nav-item a.active {
  cursor: pointer;
  font-weight: 800;
  text-decoration: underline;
}
.ativo {
  background: red;
}
.butSalvar {
  margin: 0px;
  display: inline-flex;
  flex-direction: row;
}
</style>
