<template>
  <nav class="nav-bar">
    <ul class="header lado-esquerdo">
      <img class="img-logo" src="../../assets/dummy-image-square 1.png" />
      <!-- Para cada item dentro de menuItens, so ativa quem tiver indice igual a activeIndex -->
      <li class="nav-item" v-for="(item, index) in itensEsquerdo" :key="index">
        <a :class="{ active: activeIndex === index }" @click="setActive(item)">
          {{ item }}
        </a>
      </li>
    </ul>
    <ul class="lado-direito">
      <template v-if="this.logado && this.telaPequena">
        <li class="div-hamburguer">
          <button class="button-hamburguer" @click="this.clickMenu">
            <img class="img-hamburguer" src="../../assets/menu-sanduiche.png" />
          </button>
          <div ref="opcoes" class="lista-opcoes" v-if="this.isOpen">
            <div class="nav-item" v-if="this.logado">
              <a :class="{ active: activeIndex === 6 }" @click="setActive('Perfil')"
                >Perfil</a
              >
            </div>
            <div class="nav-item" v-if="this.logado">
              <Salvar :modo="this.modoSalvar"></Salvar>
            </div>
          </div>
        </li>
      </template>
      <template v-else>
        <li v-if="!this.logado" class="nav-item">
          <a
            :class="{ active: activeIndex === itensEsquerdo.length }"
            @click="setActive('Acessar Sistema')"
            >Acessar Sistema</a
          >
        </li>
        <li class="nav-item" v-if="this.logado">
          <a :class="{ active: activeIndex === 6 }" @click="setActive('Perfil')"
            >Perfil</a
          >
        </li>
        <li class="nav-item" v-if="this.logado">
          <Salvar :modo="this.modoSalvar"></Salvar>
        </li>
      </template>
    </ul>
  </nav>
</template>

<script>
import Salvar from "../icons/Salvar.vue";
import Voltar from "../icons/Voltar.vue";

export default {
  name: "HeaderSistema",
  components: {
    Salvar,
    Voltar,
  },
  data() {
    return {
      itensEsquerdo: ["Início", "Método", "Sobre", "Como Funciona?", "Fazer Análise"],
      emAnalise: false,
      logado: false,
      telaPequena: false,
      isOpen: true,
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
    this.emAnalise = this.$route.path === "/analise";
    this.mostrarHamburguer();
    this.clickMenu();

    window.addEventListener("resize", () => {
      this.mostrarHamburguer();
      this.$forceUpdate();
    });
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
    mostrarHamburguer() {
      this.telaPequena = window.innerWidth < 940 || window.innerHeight < 940;
    },
    clickMenu() {
      if (this.$refs.opcoes) {
        if (this.isOpen) {
          this.isOpen = false;
          this.$refs.opcoes.style.display = "none";
          this.$refs.opcoes.style.marginLeft = "8vmin";
        } else {
          this.isOpen = true;
          this.$refs.opcoes.style.display = flex;
        }
      }
    },
  },
  computed: {
    modoSalvar() {
      if (this.emAnalise == true) {
        return "on";
      } else return "off";
    },
  },
};
</script>

<style lang="scss" scoped>
.nav-bar {
  display: flex;
  width: clamp(100%, 100%, 100%);
  z-index: 1;
  background: #0e0021;
  .img-logo {
    aspect-ratio: 320/200;
    height: 100%;
  }
  &:has(.div-hamburguer) {
    max-height: 10vmin;

    .button-hamburguer {
      background: red;
      cursor: pointer;
    }

    .lista-opcoes {
      display: flex;
      flex-direction: column;
    }

    .div-hamburguer {
      display: flex;
      position: absolute;
      right: 0%;
      flex-direction: column;
      align-items: flex-start;
      background: red;
      .img-hamburguer {
        width: 5vmin;
        aspect-ratio: 219/200;
      }
    }
  }
}

.header {
  list-style: none;
  display: flex;
  height: $alt-headers;
  padding: clamp(0.2%, 10px, 1%) 0px;
  margin: 0px 2% 0% 1%;
  align-items: center;
  gap: 3vmin;
  flex: 1 0 0;
  align-self: stretch;
}

.lado-direito {
  list-style: none;
  margin: 0vmin 7vmin;
  padding: 0px;
  width: clamp(200px, 36vmin, 320px);
  display: flex;
  align-items: center;
  gap: 3vmin;
}

.nav-item a {
  @include botao-header($escala: 1.1);
}

.nav-item a.active {
  cursor: pointer;
  font-weight: 800;
  text-decoration: underline;
}
</style>
