<template>
  <nav class="nav-bar">
    <ul v-if="this.tipo === 'default'" class="header">
      <li class="nav-item" @click="setActive(0)">Início</li>
      <li class="nav-item" @click="setActive(1)">Método</li>
      <li class="nav-item" @click="setActive(2)">Autores</li>
      <li class="nav-item" @click="setActive(3)">Dúvidas?</li>
    </ul>

    <div v-else-if="this.tipo === 'salvar'" class="header">
      <Voltar></Voltar>
      <button>Dúvidas?</button>
      <div class="ladoDireito">
        <Salvar modo="on"></Salvar>
      </div>
    </div>
    <div v-else-if="this.tipo === 'salvaroff'" class="header">
      <Voltar></Voltar>
      <button>Dúvidas?</button>
      <div class="ladoDireito">
        <Salvar modo="off"></Salvar>
      </div>
    </div>
    <div v-else class="header">
      <Voltar></Voltar>
      <button>Dúvidas?</button>
    </div>
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
  props: {
    tipo: {
      type: String,
      required: true,
      default: "default",
    },
  },
  methods: {
    setActive(index) {
      const mapa = {
        0: "/",
        1: "/metodo",
        2: "/equipe",
        3: "/duvidas",
      };
      const rota = mapa[index];
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
.header {
  display: flex;
  width: 100%;
  height: $alt-headers;
  padding: 10px;
  align-items: center;
  gap: 30px;
  flex-shrink: 0;
}
.nav-bar {
  background: #0e0021;
}

.ladoDireito {
  flex: 1 0 0;
  display: flex;
  padding: 9px 20px;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
}

.nav-item {
  @include mix-botao-header($escala: 1.1);
}
</style>
