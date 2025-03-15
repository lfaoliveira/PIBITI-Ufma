<template>
  <nav class="navbar">
    <ul class="nav-list">
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
export default {
  data() {
    return {
      menuItems: ["Sistema", "Método", "Autores", "Dúvidas?"],
    };
  },
  props: {
    activeIndex: 0,
  },

  methods: {
    setActive(index) {
      this.$emit("update:activeIndex", index);
      const mapa = {
        0: this.fnSistema,
        1: this.fnMetodo,
        2: this.fnAutores,
        3: this.fnDuvidas,
      };
      const func = mapa[index];
      if (typeof func !== "function") {
        console.error(`Handler for type "${tipo}" is not defined`);
        return null;
      }
      func();
    },
    fnSistema() {
      this.$router.push("/");
    },
    fnMetodo() {
      this.$router.push("/metodo");
    },
    fnAutores() {
      this.$router.push("/equipe");
    },
    fnDuvidas() {
      this.$router.push("/duvidas");
    },
  },
};
</script>

<style lang="scss" scoped>
$font-size-buts: clamp(2vmin, 16px, 20px);

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
  cursor: pointer;
  color: white;
  font-size: $font-size-buts;
  width: fit-content;
  font-weight: normal;
  text-decoration: none;
  transition: all 0.3s; /* Change to all to animate both font-size and padding */
  padding: 1vmin;
  /* Add this to prevent layout shift */
  display: inline-block;
  text-align: center;
}

.nav-item a:hover {
  font-size: calc($font-size-buts * 1.05);
  /* Remove the padding here as it's now handled by the parent */
}

@media (max-width: 500px) {
  .nav-item a {
    $font-size-buts: clamp(1vmin, 12px, 16px);
    font-size: $font-size-buts;
  }
}

.nav-item a.active {
  cursor: pointer;
  font-weight: 800;
}
</style>
