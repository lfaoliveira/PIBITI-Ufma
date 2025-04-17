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
    <ul ref="ladoDireito" class="lado-direito">
      <template v-if="this.logado && this.telaPequena">
        <li class="div-hamburguer">
          <button class="button-hamburguer" @click="this.clickMenu">
            <img
              class="img-hamburguer"
              :src="
                this.isOpen ? 'src/assets/close.png' : 'src/assets/menu-sanduiche.png'
              "
            />
          </button>
        </li>
      </template>
      <transition name="slide">
        <li ref="opcoes" class="lista-opcoes" v-show="this.isOpen || !this.telaPequena">
          <div v-if="!this.logado" class="nav-item">
            <a
              :class="{ active: activeIndex === itensEsquerdo.length }"
              @click="setActive('Acessar Sistema')"
              >Acessar Sistema</a
            >
          </div>
          <div class="nav-item" v-if="this.logado">
            <a :class="{ active: activeIndex === 6 }" @click="setActive('Perfil')"
              >Perfil</a
            >
          </div>
          <div class="nav-item" v-if="this.logado">
            <Salvar :modo="this.modoSalvar"></Salvar>
          </div>
        </li>
      </transition>
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
      isOpen: false,
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
    // this.clickMenu();

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
      if (this.telaPequena) {
        // tem menu
        this.$refs.ladoDireito.classList.add("dir-peq");
        this.$refs.ladoDireito.classList.remove("dir-grande");
        this.$refs.ladoDireito.classList.add("opcoes-peq");
        this.$refs.ladoDireito.classList.remove("opcoes-grande");
      } else {
        // nao tem menu
        this.$refs.ladoDireito.classList.add("dir-grande");
        this.$refs.ladoDireito.classList.remove("dir-peq");
        this.$refs.ladoDireito.classList.add("opcoes-grande");
        this.$refs.ladoDireito.classList.remove("opcoes-peq");
      }
    },
    clickMenu() {
      if (this.isOpen) {
        this.isOpen = false;
      } else {
        this.isOpen = true;
        this.$refs.ladoDireito.style.alignItems = "flex-end";
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
    max-height: 8vmin;

    .button-hamburguer {
      background: none;
      cursor: pointer;
    }

    .div-hamburguer {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      background: none;
      .img-hamburguer {
        width: 5vmin;
        aspect-ratio: 219/200;
      }
    }
  }
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease-out 0s;
}

.slide-enter-from {
  transform: translateX(-100%);
}
.slide-enter-to {
  transform: translateX(0);
}
.slide-leave-from {
  transform: translateX(0);
}
.slide-leave-to {
  transform: translateX(-200%);
}

/* .slide-enter-from,
  .slide-leave-to {
  transition: all 0.2s ease-in-out 0s;
} */

.lista-opcoes {
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.3s, opacity 0.1s;
}

.opcoes-peq {
  flex-direction: column;
  align-items: flex-end;
}
.opcoes-grande {
  flex-direction: row;
  align-items: center;
  gap: 3vmin;
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
  margin: 0vmin 0vmin 0vmin 1vmin;
  background: #0e0021;
  height: max-content;
  padding: 0px;
  width: clamp(200px, 36vmin, 320px);
  display: flex;
  align-items: flex-end;
  gap: 3vmin;
}

.dir-grande {
  flex-direction: row;
}
.dir-peq {
  flex-direction: column;
  width: fit-content;
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
