<template>
  <nav class="navbar">
    <ul class="nav-list">
      <!-- Para cada item dentro de menuItens, so ativa quem tiver indice activeIndex -->
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
      activeIndex: 0,
    };
  },
  methods: {
    setActive(index) {
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
      this.activeIndex = index;
    },
    fnSistema() {
      this.$router.push("/sistema");
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

<style scoped>
* {
  --font-size-buts: clamp(2vmin, 20px, 22px);
}

.navbar {
  width: 100%;
  position: absolute;
  top: 0px;
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
  padding: 5px; /* Add some padding around the item */
}

.nav-item a {
  cursor: pointer;
  color: white;
  font-size: var(--font-size-buts);
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
  font-size: calc(var(--font-size-buts) * 1.07);
  /* Remove the padding here as it's now handled by the parent */
}

.nav-item a.active {
  cursor: pointer;
  font-weight: 800;
}
</style>
