<template>
  <nav class="navbar">
    <ul class="nav-list">
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
      const mapa = { 0: fnSistema, 1: fnMétodo, 2: fnAutores, 3: fnDuvidas };
      const func = mapa[index];
      if (typeof func !== "function") {
        console.error(`Handler for type "${tipo}" is not defined`);
        return null;
      }
      func();
      this.activeIndex = index;
    },
  },
};
</script>

<style scoped>
.navbar {
  width: 100%;
  position: absolute;
  top: 0px;
  z-index: 1;
  background-color: #12071c;
  display: flex;
  height: 8vmin;
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

.nav-item a {
  color: white;
  font-size: 18px;
  font-weight: normal;
  text-decoration: none;
  transition: font-weight 0.3s;
}

.nav-item a.active {
  font-weight: 800;
}
</style>
