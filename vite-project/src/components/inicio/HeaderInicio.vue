<template>
  <nav class="navbar">
    <ul class="nav-list">
      <a><Voltar v-if="activeIndex == 3" class="nav-item"></Voltar></a>

      <!-- Para cada item dentro de menuItens, so ativa quem tiver indice igual a activeIndex -->
      <li class="nav-item" v-for="(item, index) in menuItems" :key="index">
        <a :class="{ active: activeIndex === index }" @click="setActive(index)">
          {{ item }}
        </a>
      </li>
    </ul>
  </nav>
</template>

<script>
import Voltar from "../icons/Voltar.vue";

export default {
  data() {
    return {
      menuItems: ["Sistema", "Método", "Autores", "Dúvidas?"],
    };
  },
  components: {
    Voltar,
  },
  props: {
    activeIndex: 0,
  },
  created() {},

  methods: {
    setActive(index) {
      this.$emit("update:activeIndex", index);
      const mapa = {
        0: "/",
        1: "/metodo",
        2: "/equipe",
        3: "/duvidas",
      };
      const rota = mapa[index];
      this.$router.push(rota);
    },
  },
};
</script>

<style lang="scss" scoped>
.navbar {
  width: clamp(100%, 100%, 100%);
  z-index: 1;
  background-color: #12071c;
  display: flex;
  height: min-content;
  padding: 10px;
  align-items: center;
  gap: 30px;
  flex-shrink: 0;
}

.nav-list {
  display: flex;
  list-style: none;
  justify-content: flex-start;
  gap: 20px;
  margin: 0;
  padding: 0;
}

.nav-item {
  display: flex;
  width: max-content;
  /* Add these properties */
  font-style: normal;
  word-spacing: 4%;
  align-items: center;
  justify-content: center;
}

.nav-item a {
  @include mix-botao-header($escala: 1.1);
}

.nav-item a.active {
  cursor: pointer;
  font-weight: 800;
}
</style>
